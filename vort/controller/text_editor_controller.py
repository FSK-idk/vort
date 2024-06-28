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
)
from PySide6.QtCore import Qt, Signal

from utils import PointF, RectF

from view.widget.text_editor_view import TextEditorView

from controller.controller import Controller


class TextEditorController(Controller):
    cursorPositionChanged = Signal(int)
    fontWeightChanged = Signal(QFont.Weight)

    def __init__(self, controller: Controller, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: TextEditorView = TextEditorView(controller=self, parent=parent)

        self.document: QTextDocument = QTextDocument()
        self.ui.setDocument(self.document)

        self.text_cursor: QTextCursor = QTextCursor(self.document)

        # signal

        self.cursorPositionChanged.connect(self.onCursorPositionChanged)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.resized.connect(self.onResized)
        self.ui.painted.connect(self.onPainted)

    def setBold(self, is_bold) -> None:
        font_weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(font_weight)
        self.text_cursor.mergeCharFormat(format)
        self.ui.repaint()

    def onCursorPositionChanged(self, position) -> None:
        format: QTextCharFormat = self.ui.characterFormat(position)
        self.fontWeightChanged.emit(format.fontWeight())

    # TODO: DEBUG
    def test(self) -> None:
        # format_: QTextFrameFormat = self.text_edit.document().rootFrame().frameFormat()
        # print("Root Frame Format:")
        # print("width:", format_.width().rawValue())
        # print("height:", format_.height().rawValue())
        # print("margin:", format_.margin())
        # print("padding:", format_.padding())
        pass

    def onMousePressed(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.ui.horizontalScrollBar().value()
            screen_y = self.ui.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.ui.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
                self.ui.repaint()

                self.cursorPositionChanged.emit(position)

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

                self.ui.repaint()
                self.cursorPositionChanged.emit(position)

    def onKeyPressed(self, event: QKeyEvent) -> None:
        self.handleNavigationInput(event)
        self.handleHotkeys(event)
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
            self.ui.repaint()

    def handleHotkeys(self, event: QKeyEvent) -> None:
        used = True

        if Qt.KeyboardModifier.ControlModifier in event.modifiers():
            match event.key():
                case Qt.Key.Key_X if self.text_cursor.hasSelection():
                    selected_text = self.text_cursor.selectedText()
                    QApplication.clipboard().setText(selected_text)
                    self.text_cursor.removeSelectedText()
                case Qt.Key.Key_C if self.text_cursor.hasSelection():
                    selected_text = self.text_cursor.selectedText()
                    QApplication.clipboard().setText(selected_text)
                case Qt.Key.Key_V:
                    copied_text = QApplication.clipboard().text()
                    self.text_cursor.insertText(copied_text)
                case Qt.Key.Key_A:
                    self.text_cursor.select(QTextCursor.SelectionType.Document)
                case Qt.Key.Key_Z:
                    self.document.undo(self.text_cursor)
                case Qt.Key.Key_Y:
                    self.document.redo(self.text_cursor)
                case _:
                    used = False

        if used:
            self.ui.repaint()

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
            elif event.key() == Qt.Key.Key_Delete:
                self.text_cursor.beginEditBlock()
                self.text_cursor.deleteChar()
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Escape:
                pass  # ignore
            else:
                self.text_cursor.beginEditBlock()
                self.text_cursor.insertText(event.text())
                self.text_cursor.endEditBlock()

            self.ui.repaint()

    def onResized(self, event: QResizeEvent) -> None:
        self.ui.resize(PointF(event.size().width(), event.size().height()))

    def onPainted(self, event: QPaintEvent) -> None:
        rect = RectF.fromQRect(event.rect())

        self.ui.paint(rect, self.text_cursor)
