from PySide6.QtCore import QTimerEvent, Qt, Signal, QMimeData, QObject, Slot, QRectF, QTimer
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

from core.widget.text_editor.text_canvas import TextCanvas
from core.widget.text_editor.text_document_layout import HitResult, Hit


# text editor only supports one cursor at a time

# TODO: DEBUG
count_img = 0


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

        self.text_document: QTextDocument = QTextDocument()
        self.text_cursor: QTextCursor = QTextCursor(self.text_document)

        self.scene: QGraphicsScene = QGraphicsScene(parent)
        self.ui: TextEditorUI = TextEditorUI(parent)
        self.ui.setScene(self.scene)
        self.ui.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.text_canvas: TextCanvas = TextCanvas()
        self.scene.addWidget(self.text_canvas)
        self.text_canvas.setTextContext(self.text_document, self.text_cursor)

        self.ui.horizontalScrollBar().setPageStep(int(self.text_canvas.pageWidth()))
        self.ui.verticalScrollBar().setPageStep(int(self.text_canvas.pageHeight()))

        self.last_hit_result: HitResult = HitResult()
        self.cursor_timer: QTimer = QTimer(self)
        self.cursor_timer.setInterval(100)
        self.cursor_timer.timeout.connect(self.updateCursorShape)
        self.cursor_timer.start()
        self.is_only_control_pressed = False

        # component

        self.history_component: HistoryComponent = HistoryComponent(self.text_cursor)
        self.history_component.applied.connect(self.repaintViewport)
        self.history_component.applied.connect(self.onCursorPositionChanged)

        self.history_component: HistoryComponent = HistoryComponent(self.text_cursor)
        self.history_component.applied.connect(self.repaintViewport)
        self.history_component.applied.connect(self.onCursorPositionChanged)

        self.select_component: SelectComponent = SelectComponent(self.text_cursor)
        self.select_component.applied.connect(self.repaintViewport)

        self.font_component: FontComponent = FontComponent(self.text_cursor)
        self.font_component.applied.connect(self.repaintViewport)

        self.format_component: FormatComponent = FormatComponent(self.text_cursor)
        self.format_component.applied.connect(self.repaintViewport)

        self.color_component: ColorComponent = ColorComponent(self.text_cursor)
        self.color_component.applied.connect(self.repaintViewport)

        self.spacing_component: SpacingComponent = SpacingComponent(self.text_cursor)
        self.spacing_component.applied.connect(self.repaintViewport)

        self.move_component: MoveComponent = MoveComponent(self.text_cursor, self.text_canvas)
        self.move_component.applied.connect(self.repaintViewport)
        self.move_component.applied.connect(self.onCursorPositionChanged)

        self.input_component: InputComponent = InputComponent(self.text_cursor)
        self.input_component.applied.connect(self.repaintViewport)
        self.input_component.applied.connect(self.onCursorPositionChanged)

        # signal

        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.keyReleased.connect(self.onKeyReleased)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseReleased.connect(self.onMouseReleased)
        self.ui.mouseMoved.connect(self.onMouseMoved)

        self.text_canvas.sizeChanged.connect(self.onCanvasSizeChanged)
        self.text_canvas.characterCountChanged.connect(self.characterCountChanged.emit)

        self.ui.zoomFactorChanged.connect(self.zoomFactorSelected.emit)

    # TODO: DEBUG
    def test(self) -> None:

        self.repaintViewport()
        pass

    def test2(self) -> None:

        self.repaintViewport()
        return

    def setZoomFactor(self, zoom_factor: float) -> None:
        self.ui.setZoomFactor(zoom_factor)

    @Slot(PointF)
    def onCanvasSizeChanged(self, size: PointF) -> None:
        self.scene.setSceneRect(QRectF(0, 0, size.xPosition(), size.yPosition()))

    @Slot()
    def onCursorPositionChanged(self) -> None:
        position: int = self.text_cursor.position()
        block_point: PointF = self.text_canvas.blockTest(position)
        self.ui.ensureVisible(block_point.xPosition(), block_point.yPosition(), 1, 1)

        char_format: QTextCharFormat = self.text_cursor.charFormat()
        block_format: QTextBlockFormat = self.text_cursor.blockFormat()

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
        hit_result = self.text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        if event.button() == Qt.MouseButton.LeftButton:
            self.move_component.pointPress(hit_result)

    @Slot(QMouseEvent)
    def onMouseReleased(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        if hit_result.hit == Hit.Hyperlink and self.is_only_control_pressed:
            QDesktopServices.openUrl(hit_result.data)

    @Slot(QMouseEvent)
    def onMouseMoved(self, event: QMouseEvent) -> None:
        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.text_canvas.hitTest(point)
        self.last_hit_result = hit_result

        self.is_tool_tip_shown = False
        if hit_result.hit == Hit.Hyperlink and not self.is_tool_tip_shown:
            QToolTip.showText(event.globalPos(), hit_result.data)

        if hit_result.hit != Hit.Hyperlink:
            QToolTip.hideText()
            self.is_tool_tip_shown = False

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move_component.pointMove(hit_result)

    @Slot(QKeyEvent)
    def onKeyPressed(self, event: QKeyEvent) -> None:
        self.is_only_control_pressed = Qt.KeyboardModifier.ControlModifier == event.modifiers()

        self.move_component.keyPress(event.key())
        self.input_component.input(event)

    @Slot(QKeyEvent)
    def onKeyReleased(self, event: QKeyEvent) -> None:
        self.is_only_control_pressed = Qt.KeyboardModifier.ControlModifier == event.modifiers()

    @Slot()
    def updateCursorShape(self) -> None:
        if self.last_hit_result.hit == Hit.Text:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        elif self.last_hit_result.hit == Hit.Image:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        elif self.last_hit_result.hit == Hit.Hyperlink:
            if self.is_only_control_pressed:
                QGuiApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
            else:
                QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        else:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    @Slot()
    def repaintViewport(self):
        self.ui.viewport().repaint()
