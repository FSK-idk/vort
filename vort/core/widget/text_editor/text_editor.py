from PySide6.QtCore import Qt, Signal, QMimeData, QObject, Slot, QRectF, QTimer, QEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QToolTip
from PySide6.QtGui import (
    QGuiApplication,
    QKeyEvent,
    QMouseEvent,
    QTextDocument,
    QTextCursor,
    QFont,
    QResizeEvent,
    QKeyEvent,
    QTextCharFormat,
    QPaintEvent,
    QTextBlockFormat,
    QClipboard,
    QPalette,
    QTextDocumentFragment,
    QColor,
    QTextImageFormat,
    QImage,
    QTextBlock,
    QTextFragment,
    QDesktopServices,
)

from util import PointF, RectF

from core.widget.text_editor.text_editor_ui import TextEditorUI

from core.widget.text_editor.component.history_component import HistoryComponent
from core.widget.text_editor.component.select_component import SelectComponent
from core.widget.text_editor.component.font_component import FontComponent
from core.widget.text_editor.component.format_component import FormatComponent
from core.widget.text_editor.component.color_component import ColorComponent
from core.widget.text_editor.component.spacing_component import SpacingComponent
from core.widget.text_editor.component.move_component import MoveComponent
from core.widget.text_editor.component.input_component import InputComponent

from core.widget.text_editor.layout.text_canvas import TextCanvas
from core.widget.text_editor.layout.text_document_layout import TextDocumentLayout, HitResult, Hit
from core.widget.text_editor.layout.page_layout import PageLayout


# text editor only supports one cursor at a time


class DocumentContext:
    def __init__(
        self,
        page_layout: PageLayout,
        text_document: QTextDocument,
        text_document_layout: TextDocumentLayout,
        text_cursor: QTextCursor,
    ) -> None:
        self.page_layout: PageLayout = page_layout
        self.text_documuent: QTextDocument = text_document
        self.text_document_layout: TextDocumentLayout = text_document_layout
        self.text_cursor: QTextCursor = text_cursor


class TextEditor(QObject):
    fontFamilyChanged = Signal(str)
    fontSizeChnaged = Signal(int)

    boldTurned = Signal(bool)
    italicTurned = Signal(bool)
    underlinedTurned = Signal(bool)

    foregroundColorChanged = Signal(QColor)
    backgroundColorChanged = Signal(QColor)

    firstLineIndentTurned = Signal(bool)

    pageCountChanged = Signal(int)

    characterCountChanged = Signal(int)
    zoomFactorSelected = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        text_document: QTextDocument = QTextDocument()
        page_layout: PageLayout = PageLayout()
        text_document_layout: TextDocumentLayout = TextDocumentLayout(text_document, page_layout)
        text_document.setDocumentLayout(text_document_layout)
        text_cursor: QTextCursor = QTextCursor(text_document)

        self.__document_context = DocumentContext(page_layout, text_document, text_document_layout, text_cursor)

        self.__scene: QGraphicsScene = QGraphicsScene(parent)

        self.ui: TextEditorUI = TextEditorUI(parent)
        self.ui.setScene(self.__scene)
        self.ui.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.__text_canvas: TextCanvas = TextCanvas(
            self.__document_context.page_layout,
            self.__document_context.text_document_layout,
            self.__document_context.text_cursor,
        )
        self.__scene.addWidget(self.__text_canvas)

        self.ui.horizontalScrollBar().setPageStep(int(self.__text_canvas.pageWidth()))
        self.ui.verticalScrollBar().setPageStep(int(self.__text_canvas.pageHeight()))

        self.last_hit_result: HitResult = HitResult()
        self.cursor_timer: QTimer = QTimer(self)
        self.cursor_timer.setInterval(100)
        self.cursor_timer.timeout.connect(self.updateCursorShape)
        self.cursor_timer.start()

        # component

        self.history_component: HistoryComponent = HistoryComponent(self.__document_context.text_cursor)
        self.history_component.applied.connect(self.repaintViewport)
        self.history_component.applied.connect(self.onCursorPositionChanged)

        self.history_component: HistoryComponent = HistoryComponent(self.__document_context.text_cursor)
        self.history_component.applied.connect(self.repaintViewport)
        self.history_component.applied.connect(self.onCursorPositionChanged)

        self.select_component: SelectComponent = SelectComponent(self.__document_context.text_cursor)
        self.select_component.applied.connect(self.repaintViewport)

        self.font_component: FontComponent = FontComponent(self.__document_context.text_cursor)
        self.font_component.applied.connect(self.repaintViewport)

        self.format_component: FormatComponent = FormatComponent(self.__document_context.text_cursor)
        self.format_component.applied.connect(self.repaintViewport)

        self.color_component: ColorComponent = ColorComponent(self.__document_context.text_cursor)
        self.color_component.applied.connect(self.repaintViewport)

        self.spacing_component: SpacingComponent = SpacingComponent(self.__document_context.text_cursor)
        self.spacing_component.applied.connect(self.repaintViewport)

        self.move_component: MoveComponent = MoveComponent(self.__document_context.text_cursor)
        self.move_component.applied.connect(self.repaintViewport)
        self.move_component.applied.connect(self.onCursorPositionChanged)

        self.input_component: InputComponent = InputComponent(self.__document_context.text_cursor)
        self.input_component.applied.connect(self.repaintViewport)
        self.input_component.applied.connect(self.onCursorPositionChanged)

        # signal

        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseReleased.connect(self.onMouseReleased)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.mouseLeft.connect(self.onMouseLeft)
        self.ui.mouseDoubleClicked.connect(self.onMouseDoubleClicked)

        self.__text_canvas.sizeChanged.connect(self.onCanvasSizeChanged)
        self.__text_canvas.characterCountChanged.connect(self.characterCountChanged.emit)

        self.ui.zoomFactorChanged.connect(self.zoomFactorSelected.emit)

    # TODO: DEBUG
    def test(self) -> None:
        self.repaintViewport()
        pass

    def test2(self) -> None:

        self.repaintViewport()
        return

    def setFooterShown(self, is_shown: bool) -> None:
        self.__text_canvas.setFooterShown(is_shown)
        self.repaintViewport()

    def setZoomFactor(self, zoom_factor: float) -> None:
        self.ui.setZoomFactor(zoom_factor)

    @Slot(PointF)
    def onCanvasSizeChanged(self, size: PointF) -> None:
        self.__scene.setSceneRect(QRectF(0, 0, size.xPosition(), size.yPosition()))

    @Slot()
    def onCursorPositionChanged(self) -> None:
        position: int = self.__document_context.text_cursor.position()
        block_point: PointF = self.__text_canvas.blockTest(position)
        self.ui.ensureVisible(block_point.xPosition(), block_point.yPosition(), 1, 1)

        char_format: QTextCharFormat = self.__document_context.text_cursor.charFormat()
        block_format: QTextBlockFormat = self.__document_context.text_cursor.blockFormat()

        # font

        font_family: str = char_format.font().family()
        self.fontFamilyChanged.emit(font_family)

        font_size: int = char_format.font().pointSize()
        self.fontSizeChnaged.emit(font_size)

        # format

        is_bold = char_format.fontWeight() == QFont.Weight.Bold
        self.boldTurned.emit(is_bold)

        is_italic = char_format.fontItalic()
        self.italicTurned.emit(is_italic)

        is_underlined = char_format.fontUnderline()
        self.underlinedTurned.emit(is_underlined)

        # color

        foreground_color = char_format.foreground().color()
        self.foregroundColorChanged.emit(foreground_color)

        background_color = char_format.background().color()
        self.backgroundColorChanged.emit(background_color)

        # indent

        is_indent = block_format.textIndent() != 0
        self.firstLineIndentTurned.emit(is_indent)

    @Slot(QMouseEvent)
    def onMousePressed(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        if event.button() == Qt.MouseButton.LeftButton:
            if self.last_hit_result.hit == Hit.NoHit:
                self.__document_context.text_cursor.clearSelection()
                self.repaintViewport()
            self.move_component.pointPress(hit_result)

    @Slot(QMouseEvent)
    def onMouseReleased(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        if (
            hit_result.hit == Hit.Hyperlink
            and Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers()
        ):
            QDesktopServices.openUrl(hit_result.data)

    @Slot(QMouseEvent)
    def onMouseDoubleClicked(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.select_component.selectWord(hit_result)

    @Slot(QMouseEvent)
    def onMouseMoved(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        self.is_tool_tip_shown = False
        if hit_result.hit == Hit.Hyperlink and not self.is_tool_tip_shown:
            QToolTip.showText(event.globalPos(), hit_result.data)

        if hit_result.hit != Hit.Hyperlink:
            QToolTip.hideText()
            self.is_tool_tip_shown = False

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move_component.pointMove(hit_result)

    @Slot(QEvent)
    def onMouseLeft(self, event: QEvent) -> None:
        self.last_hit_result = HitResult()

    @Slot(QKeyEvent)
    def onKeyPressed(self, event: QKeyEvent) -> None:
        self.move_component.keyPress(event.key())
        self.input_component.input(event)

    @Slot()
    def updateCursorShape(self) -> None:
        if self.last_hit_result.hit == Hit.Text:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        elif self.last_hit_result.hit == Hit.Image:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        elif self.last_hit_result.hit == Hit.Hyperlink:
            if Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers():
                QGuiApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
            else:
                QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        else:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    @Slot()
    def repaintViewport(self):
        self.ui.viewport().repaint()
