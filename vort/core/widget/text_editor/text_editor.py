from PySide6.QtCore import Qt, Signal, QMimeData, QObject, Slot, QRectF
from PySide6.QtWidgets import QWidget, QGraphicsScene, QApplication, QFrame, QGraphicsItem
from PySide6.QtGui import (
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
)

from util import PointF, RectF

from core.widget.text_editor.text_editor_ui import TextEditorUI

from core.widget.text_editor.component.font_component import FontComponent
from core.widget.text_editor.component.format_component import FormatComponent
from core.widget.text_editor.component.color_component import ColorComponent
from core.widget.text_editor.component.indent_component import IndentComponent
from core.widget.text_editor.component.copy_paste_component import CopyPasteComponent
from core.widget.text_editor.component.select_component import SelectComponent
from core.widget.text_editor.component.history_component import HistoryComponent

from core.widget.text_editor.canvas import Canvas

# text editor only supports one cursor at a time


class TextEditor(QObject):
    # font

    fontFamilySelected = Signal(str)
    fontSizeSelected = Signal(int)

    # format

    boldTurned = Signal(bool)
    italicTurned = Signal(bool)
    underlinedTurned = Signal(bool)

    # color

    foregroundColorSelected = Signal(QColor)
    backgroundColorSelected = Signal(QColor)

    # indent

    firstLineIndentTurned = Signal(bool)

    # page

    pageCountChanged = Signal(int)

    # status

    characterCountChanged = Signal(int)

    # internal

    cursorPositionChanged = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.document: QTextDocument = QTextDocument()
        self.text_cursor: QTextCursor = QTextCursor(self.document)

        self.scene: QGraphicsScene = QGraphicsScene(parent)
        self.ui: TextEditorUI = TextEditorUI(parent)
        self.ui.setScene(self.scene)
        self.ui.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.canvas: Canvas = Canvas()
        self.scene.addWidget(self.canvas)
        self.canvas.setTextContext(self.document, self.text_cursor)

        self.ui.horizontalScrollBar().setPageStep(int(self.canvas.pageWidth()))
        self.ui.verticalScrollBar().setPageStep(int(self.canvas.pageHeight()))

        # component

        self.font_component: FontComponent = FontComponent(self.text_cursor)
        self.font_component.applied.connect(self.repaintViewport)

        self.format_component: FormatComponent = FormatComponent(self.text_cursor)
        self.format_component.applied.connect(self.repaintViewport)

        self.color_component: ColorComponent = ColorComponent(self.text_cursor)
        self.color_component.applied.connect(self.repaintViewport)

        self.indent_component: IndentComponent = IndentComponent(self.text_cursor)
        self.indent_component.applied.connect(self.repaintViewport)

        self.copy_paste_component: CopyPasteComponent = CopyPasteComponent(self.text_cursor)
        self.copy_paste_component.applied.connect(self.repaintViewport)

        self.select_component: SelectComponent = SelectComponent(self.text_cursor)
        self.select_component.applied.connect(self.repaintViewport)

        self.history_component: HistoryComponent = HistoryComponent(self.text_cursor)
        self.history_component.applied.connect(self.repaintViewport)

        # signal

        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseMoved.connect(self.onMouseMoved)

        self.canvas.sizeChanged.connect(self.onCanvasSizeChanged)
        self.canvas.characterCountChanged.connect(self.characterCountChanged.emit)

        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

    # TODO: DEBUG
    def test(self) -> None:
        print("test")
        pass

    def onCanvasSizeChanged(self, size: PointF) -> None:
        self.scene.setSceneRect(QRectF(0, 0, size.xPosition(), size.yPosition()))

    def onCursorPositionChanged(self, position: int) -> None:
        char_format: QTextCharFormat = self.text_cursor.charFormat()
        block_format: QTextBlockFormat = self.text_cursor.blockFormat()

        # font

        font_family: str = char_format.font().family()
        self.fontFamilySelected.emit(font_family)

        font_size: int = char_format.font().pointSize()
        self.fontSizeSelected.emit(font_size)

        # format

        is_bold = char_format.fontWeight() == QFont.Weight.Bold
        self.boldTurned.emit(is_bold)

        is_italic = char_format.fontItalic()
        self.italicTurned.emit(is_italic)

        is_underlined = char_format.fontUnderline()
        self.underlinedTurned.emit(is_underlined)

        # color

        foreground_color = char_format.foreground().color()
        self.foregroundColorSelected.emit(foreground_color)

        background_color = char_format.background().color()
        self.backgroundColorSelected.emit(background_color)

        # indent

        is_indent = block_format.textIndent() != 0
        self.firstLineIndentTurned.emit(is_indent)

    def onMousePressed(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
            position = self.canvas.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
                self.cursorPositionChanged.emit(self.text_cursor.position())
                self.ui.viewport().repaint()

            self.mouse_pressed = True

    def onMouseMoved(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
            position = self.canvas.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
                self.cursorPositionChanged.emit(self.text_cursor.position())
                self.ui.viewport().repaint()

    def onKeyPressed(self, event: QKeyEvent) -> None:
        self.handleNavigationInput(event)
        self.handleTextInput(event)

    def handleNavigationInput(self, event: QKeyEvent) -> None:
        move_mode = None
        move_operation = None

        if Qt.KeyboardModifier.ShiftModifier in event.modifiers():
            move_mode = QTextCursor.MoveMode.KeepAnchor
        else:
            move_mode = QTextCursor.MoveMode.MoveAnchor

        if Qt.KeyboardModifier.ControlModifier in event.modifiers():
            match event.key():
                case Qt.Key.Key_Left:
                    move_operation = QTextCursor.MoveOperation.WordLeft
                case Qt.Key.Key_Right:
                    move_operation = QTextCursor.MoveOperation.WordRight
                case Qt.Key.Key_Up:
                    move_operation = QTextCursor.MoveOperation.PreviousBlock
                case Qt.Key.Key_Down:
                    move_operation = QTextCursor.MoveOperation.NextBlock
                case Qt.Key.Key_Home:
                    move_operation = QTextCursor.MoveOperation.StartOfBlock
                case Qt.Key.Key_End:
                    move_operation = QTextCursor.MoveOperation.EndOfBlock
        else:
            match event.key():
                case Qt.Key.Key_Left:
                    move_operation = QTextCursor.MoveOperation.Left
                case Qt.Key.Key_Right:
                    move_operation = QTextCursor.MoveOperation.Right
                case Qt.Key.Key_Up:
                    move_operation = QTextCursor.MoveOperation.Up
                case Qt.Key.Key_Down:
                    move_operation = QTextCursor.MoveOperation.Down
                case Qt.Key.Key_Home:
                    move_operation = QTextCursor.MoveOperation.StartOfLine
                case Qt.Key.Key_End:
                    move_operation = QTextCursor.MoveOperation.EndOfLine

        if move_mode and move_operation:
            self.text_cursor.movePosition(move_operation, move_mode)
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

    def handleTextInput(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.text():
            match event.key():
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete if not self.text_cursor.hasSelection():
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor)
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case _:
                    return
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier] and event.text():
            match event.key():
                case Qt.Key.Key_Enter:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertBlock()
                    self.text_cursor.setPosition(self.text_cursor.block().position())
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Escape:
                    return  # ignore
                case _:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertText(event.text())
                    self.text_cursor.endEditBlock()
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

    @Slot()
    def repaintViewport(self):
        pass
        self.ui.viewport().repaint()
