from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QGuiApplication

from core.text_editor.component.component import Component
from core.text_editor.layout.text_document_layout import HitResult, Hit


class MoveComponent(Component):
    def pointPress(self, result: HitResult) -> None:
        if result.hit != Hit.NoHit:
            self._text_cursor.setPosition(result.position, QTextCursor.MoveMode.MoveAnchor)
            self.applied.emit()

    def pointMove(self, result: HitResult) -> None:
        if result.hit != Hit.NoHit:
            self._text_cursor.setPosition(result.position, QTextCursor.MoveMode.KeepAnchor)
            self.applied.emit()

    def keyPress(self, key: int | Qt.Key) -> None:
        move_mode = None
        move_operation = None

        if Qt.KeyboardModifier.ShiftModifier in QGuiApplication.keyboardModifiers():
            move_mode = QTextCursor.MoveMode.KeepAnchor
        else:
            move_mode = QTextCursor.MoveMode.MoveAnchor

        if Qt.KeyboardModifier.ControlModifier in QGuiApplication.keyboardModifiers():
            match key:
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
            match key:
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

        if move_mode is not None and move_operation is not None:
            self._text_cursor.movePosition(move_operation, move_mode)
            self.applied.emit()
