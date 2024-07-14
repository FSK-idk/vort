from PySide6.QtCore import Qt, Signal, QObject, Slot, QRectF, QTimer, QEvent, QPointF
from PySide6.QtWidgets import QWidget, QGraphicsScene, QToolTip
from PySide6.QtGui import (
    QGuiApplication,
    QKeyEvent,
    QMouseEvent,
    QFont,
    QKeyEvent,
    QTextCharFormat,
    QTextBlockFormat,
    QColor,
    QDesktopServices,
    QTextCursor,
)

from core.editor.document_editor.component.file_component import FileComponent

from core.editor.document_editor.document_editor_ui import DocumentEditorUI
from core.editor.document_editor.document_editor_context import DocumentEditorContext

from core.editor.text_editor.text_document_layout import HitResult, Hit

# text editor only supports one cursor at a time


class DocumentEditor(QObject):
    fontFamilyChanged: Signal = Signal(str)

    fontSizeChnaged: Signal = Signal(int)

    boldTurned: Signal = Signal(bool)
    italicTurned: Signal = Signal(bool)
    underlinedTurned: Signal = Signal(bool)

    foregroundColorChanged: Signal = Signal(QColor)
    backgroundColorChanged: Signal = Signal(QColor)

    alignmentChanged: Signal = Signal(Qt.AlignmentFlag)

    contentChanged: Signal = Signal()

    caseTurned: Signal = Signal(bool)
    wholeTurned: Signal = Signal(bool)
    regexTurned: Signal = Signal(bool)

    charCountChanged: Signal = Signal(int)
    zoomFactorSelected: Signal = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: DocumentEditorUI = DocumentEditorUI(parent)

        self.__scene: QGraphicsScene = QGraphicsScene(parent)
        self.ui.setScene(self.__scene)

        self.__context: DocumentEditorContext | None = None

        self.file_component: FileComponent = FileComponent()
        self.file_component.contextChanged.connect(self.onContextChanged)
        self.file_component.contextCleared.connect(self.onContextCleared)

        # mouse cursor

        self.__last_hit_result: HitResult = HitResult()
        self.__cursor_timer: QTimer = QTimer(self)
        self.__cursor_timer.setInterval(100)
        self.__cursor_timer.timeout.connect(self.updateCursorShape)
        self.__cursor_timer.start()

        # signal

        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseReleased.connect(self.onMouseReleased)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.mouseLeft.connect(self.onMouseLeft)
        self.ui.mouseDoubleClicked.connect(self.onMouseDoubleClicked)

        self.ui.zoomFactorChanged.connect(self.zoomFactorSelected.emit)

    def context(self) -> DocumentEditorContext | None:
        return self.__context

    @Slot()
    def updateCursorShape(self) -> None:
        if self.__last_hit_result.hit == Hit.Text:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        elif self.__last_hit_result.hit == Hit.Image:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        elif self.__last_hit_result.hit == Hit.Hyperlink:
            if Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers():
                QGuiApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
            else:
                QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        else:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    @Slot()
    def repaintViewport(self):
        self.ui.viewport().repaint()

    @Slot()
    def updateUI(self) -> None:
        if self.__context is None:
            return

        position: int = self.__context.text_editor.context().cursor.position()
        block_point: QPointF = self.__context.text_editor.context().layout.positionTest(position)
        self.ui.ensureVisible(block_point.x(), block_point.y(), 1, 1)

        char_format: QTextCharFormat = self.__context.text_editor.context().cursor.charFormat()
        block_format: QTextBlockFormat = self.__context.text_editor.context().cursor.blockFormat()

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

        is_underlined = char_format.underlineStyle() == QTextCharFormat.UnderlineStyle.SingleUnderline
        self.underlinedTurned.emit(is_underlined)

        # color

        foreground_color = char_format.foreground().color()
        self.foregroundColorChanged.emit(foreground_color)

        background_color = char_format.background().color()
        self.backgroundColorChanged.emit(background_color)

        # alignment

        alignment = block_format.alignment()
        self.alignmentChanged.emit(alignment)

    @Slot(QMouseEvent)
    def onMousePressed(self, event: QMouseEvent) -> None:
        if self.__context is None:
            return

        point = self.ui.mapToScene(event.position().toPoint())
        hit_result = self.__context.text_editor.context().layout.pointTest(point)
        self.__last_hit_result = hit_result

        if event.button() == Qt.MouseButton.LeftButton:
            if self.__last_hit_result.hit == Hit.NoHit:
                self.__context.text_editor.context().cursor.clearSelection()
                self.repaintViewport()
            self.__context.text_editor.context().movement_component.moveToPoint(
                hit_result.point, QTextCursor.MoveMode.MoveAnchor
            )

    @Slot(QMouseEvent)
    def onMouseReleased(self, event: QMouseEvent) -> None:
        if self.__context is None:
            return

        point: QPointF = self.ui.mapToScene(event.position().toPoint())
        hit_result: HitResult = self.__context.text_editor.context().layout.pointTest(point)
        self.__last_hit_result = hit_result

        if (
            hit_result.hit == Hit.Hyperlink
            and Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers()
        ):
            QDesktopServices.openUrl(hit_result.hyperlink)

    @Slot(QMouseEvent)
    def onMouseDoubleClicked(self, event: QMouseEvent) -> None:
        if self.__context is None:
            return

        point: QPointF = self.ui.mapToScene(event.position().toPoint())
        hit_result: HitResult = self.__context.text_editor.context().layout.pointTest(point)
        self.__last_hit_result = hit_result

        if hit_result.hit != Hit.NoHit and event.buttons() == Qt.MouseButton.LeftButton:
            self.__context.text_editor.context().selection_component.selectWord(hit_result.position)

    @Slot(QMouseEvent)
    def onMouseMoved(self, event: QMouseEvent) -> None:
        if self.__context is None:
            return

        point: QPointF = self.ui.mapToScene(event.position().toPoint())
        hit_result: HitResult = self.__context.text_editor.context().layout.pointTest(point)
        self.__last_hit_result = hit_result

        self.is_tool_tip_shown = False
        if hit_result.hit == Hit.Hyperlink and not self.is_tool_tip_shown:
            QToolTip.showText(event.globalPos(), hit_result.hyperlink)

        if hit_result.hit != Hit.Hyperlink:
            QToolTip.hideText()
            self.is_tool_tip_shown = False

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.__context.text_editor.context().movement_component.moveToPoint(
                hit_result.point, QTextCursor.MoveMode.KeepAnchor
            )

    @Slot(QEvent)
    def onMouseLeft(self, event: QEvent) -> None:
        if self.__context is None:
            return

        self.__last_hit_result = HitResult()

    @Slot(QKeyEvent)
    def onKeyPressed(self, event: QKeyEvent) -> None:
        if self.__context is None:
            return

        self.__context.text_editor.context().movement_component.moveByKey(event.key(), event.modifiers())

        if event.text():
            match event.key():
                case Qt.Key.Key_Enter:
                    pass
                case Qt.Key.Key_Escape:
                    pass
                case Qt.Key.Key_Delete:
                    self.__context.text_editor.context().input_component.delete(event.modifiers())
                case Qt.Key.Key_Backspace:
                    self.__context.text_editor.context().input_component.deletePrevious(event.modifiers())
                case _:
                    if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
                        self.__context.text_editor.context().input_component.insertText(event.text())

    def onContextChanged(self, context: DocumentEditorContext) -> None:
        self.__context = context
        if self.__context is None:
            return

        self.__context.text_editor.repaintRequest.connect(self.repaintViewport)
        self.__context.text_editor.updateUIRequest.connect(self.updateUI)
        self.__context.header_editor.repaintRequest.connect(self.repaintViewport)
        self.__context.footer_editor.repaintRequest.connect(self.repaintViewport)

        self.__context.page_layout.externalChanged.connect(self.onPageLayoutExternalChanged)

        is_case: bool = self.__context.text_editor.context().finder_component.isCaseTurned()
        self.caseTurned.emit(is_case)

        is_whole: bool = self.__context.text_editor.context().finder_component.isWholeTurned()
        self.wholeTurned.emit(is_whole)

        is_regex: bool = self.__context.text_editor.context().finder_component.isRegexTurned()
        self.regexTurned.emit(is_regex)

        self.__context.text_editor.charCountChanged.connect(self.charCountChanged.emit)

        self.__scene.addWidget(self.__context.canvas)
        self.ui.setScene(self.__scene)
        self.onPageLayoutExternalChanged()

        # try move this code up :)
        self.__context.canvas.setFixedSize(
            int(self.__context.page_layout.width()), int(self.__context.page_layout.height())
        )

        self.__context.text_editor.context().document.contentsChanged.connect(self.contentChanged.emit)

        self.updateUI()
        self.repaintViewport()

    def onContextCleared(self) -> None:
        self.__scene: QGraphicsScene = QGraphicsScene(self.parent())
        self.ui.setScene(self.__scene)
        self.__last_hit_result = HitResult()
        self.repaintViewport()

    @Slot()
    def onPageLayoutExternalChanged(self) -> None:
        if self.__context is None:
            return

        if (
            self.__context.canvas.width() != self.__context.page_layout.width()
            or self.__context.canvas.height() != self.__context.page_layout.height()
        ):
            self.__context.canvas.setFixedSize(
                int(self.__context.page_layout.width()), int(self.__context.page_layout.height())
            )
            self.__scene.setSceneRect(
                QRectF(0, 0, self.__context.page_layout.width(), self.__context.page_layout.height())
            )

        self.ui.horizontalScrollBar().setPageStep(int(self.__context.page_layout.pageWidth()))
        self.ui.verticalScrollBar().setPageStep(int(self.__context.page_layout.pageHeight()))
