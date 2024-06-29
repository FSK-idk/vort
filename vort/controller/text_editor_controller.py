from PySide6.QtWidgets import (
    QWidget,
    QApplication,
)
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
    QTextDocumentFragment,
    QColor,
)
from PySide6.QtCore import Qt, Signal, QMimeData

from utils import PointF, RectF

from view.widget.text_editor_view import TextEditorView

from controller.controller import Controller


class TextEditorController(Controller):
    cursorPositionChanged = Signal(int)
    fontChanged = Signal(str)
    sizeChanged = Signal(int)
    boldTurned = Signal(bool)
    italicTurned = Signal(bool)
    underlinedTurned = Signal(bool)
    colorSelected = Signal(QColor)

    pageCountChanged = Signal(int)
    characterCountChanged = Signal(int)

    def __init__(self, controller: Controller, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: TextEditorView = TextEditorView(controller=self, parent=parent)

        self.document: QTextDocument = QTextDocument()
        self.ui.setDocument(self.document)

        self.text_cursor: QTextCursor = QTextCursor(self.document)
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(10)
        # self.text_cursor.mergeCharFormat(format)

        # signal

        self.cursorPositionChanged.connect(self.onCursorPositionChanged)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.resized.connect(self.onResized)
        self.ui.paintedDocument.connect(self.onPaintedDocument)

        self.ui.pageCountChanged.connect(self.pageCountChanged.emit)
        self.ui.characterCountChanged.connect(self.characterCountChanged.emit)

    # TODO: DEBUG
    def test(self) -> None:
        pass
        # self.text_cursor.setBlockCharFormat(self.text_cursor.charFormat())
        # print(self.text_cursor.position())

    def setSize(self, font_size: int) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(font_size)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def setFont(self, font_family: str) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamily(font_family)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def turnBold(self, is_bold: bool) -> None:
        bold = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(bold)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def turnItalic(self, is_italic: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontItalic(is_italic)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def turnUnderlined(self, is_underline: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontUnderline(is_underline)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def selectColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setForeground(color)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def onCursorPositionChanged(self, position: int) -> None:
        format: QTextCharFormat = self.text_cursor.charFormat()

        self.fontChanged.emit(format.font().family())
        self.sizeChanged.emit(format.font().pointSize())
        self.boldTurned.emit(format.fontWeight() == QFont.Weight.Bold)
        self.italicTurned.emit(format.fontItalic())
        self.underlinedTurned.emit(format.fontUnderline())
        self.colorSelected.emit(format.foreground().color())

    def undo(self) -> None:
        self.document.undo(self.text_cursor)
        self.ui.viewport().repaint()

    def redo(self) -> None:
        self.document.redo(self.text_cursor)
        self.ui.viewport().repaint()

    def cut(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.text_cursor.removeSelectedText()
            self.ui.viewport().repaint()

    def copy(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.ui.viewport().repaint()

    def paste(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        if mime_data.hasHtml():
            self.text_cursor.insertFragment(QTextDocumentFragment.fromHtml(mime_data.html()))
        else:
            self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.ui.viewport().repaint()

    def pastePlain(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.ui.viewport().repaint()

    def selectAll(self) -> None:
        self.text_cursor.select(QTextCursor.SelectionType.Document)
        self.ui.viewport().repaint()

    def onMousePressed(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.ui.horizontalScrollBar().value()
            screen_y = self.ui.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.ui.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
                self.cursorPositionChanged.emit(self.text_cursor.position())
                self.ui.viewport().repaint()

            self.mouse_pressed = True

    def onMouseMoved(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.ui.horizontalScrollBar().value()
            screen_y = self.ui.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.ui.hitTest(point_position)

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
        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier] and event.text():
            if event.key() == Qt.Key.Key_Enter:
                self.text_cursor.beginEditBlock()
                self.text_cursor.insertBlock()
                self.text_cursor.setPosition(self.text_cursor.block().position())
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Backspace:
                self.text_cursor.beginEditBlock()
                self.text_cursor.deletePreviousChar()
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Delete and not self.text_cursor.hasSelection():
                self.text_cursor.beginEditBlock()
                self.text_cursor.deleteChar()
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Escape:
                return  # ignore
            else:
                self.text_cursor.beginEditBlock()
                self.text_cursor.insertText(event.text())
                self.text_cursor.endEditBlock()
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

    def onResized(self, event: QResizeEvent) -> None:
        self.ui.resize(PointF(event.size().width(), event.size().height()))

    def onPaintedDocument(self, event: QPaintEvent) -> None:
        rect = RectF.fromQRect(event.rect())
        self.ui.paint_document(rect, self.text_cursor)
