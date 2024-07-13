from PySide6.QtCore import Qt, Signal, QObject, QPointF
from PySide6.QtGui import QTextCursor

from core.editor.text_editor.text_document_layout import TextDocumentLayout, HitResult, Hit


class MovementComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor, document_layout: TextDocumentLayout) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor
        self.__document_layout: TextDocumentLayout = document_layout

    def moveToPoint(self, point: QPointF, mode: QTextCursor.MoveMode) -> None:
        hit_result: HitResult = self.__document_layout.pointTest(point)
        if hit_result.hit != Hit.NoHit and self.__cursor.position() != hit_result.position:
            self.__cursor.setPosition(hit_result.position, mode)
            self.repaintRequest.emit()

    def moveToPosition(self, position: int, mode: QTextCursor.MoveMode) -> None:
        if self.__cursor.position() != position:
            self.__cursor.setPosition(position, mode)
            self.repaintRequest.emit()

    def moveByKey(self, key: int | Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        mode: QTextCursor.MoveMode | None = None
        operation: QTextCursor.MoveOperation | None = None

        if Qt.KeyboardModifier.ShiftModifier in modifiers:
            mode = QTextCursor.MoveMode.KeepAnchor
        else:
            mode = QTextCursor.MoveMode.MoveAnchor

        if Qt.KeyboardModifier.ControlModifier in modifiers:
            match key:
                case Qt.Key.Key_Left:
                    operation = QTextCursor.MoveOperation.WordLeft
                case Qt.Key.Key_Right:
                    operation = QTextCursor.MoveOperation.WordRight
                case Qt.Key.Key_Up:
                    operation = QTextCursor.MoveOperation.PreviousBlock
                case Qt.Key.Key_Down:
                    operation = QTextCursor.MoveOperation.NextBlock
                case Qt.Key.Key_Home:
                    operation = QTextCursor.MoveOperation.StartOfBlock
                case Qt.Key.Key_End:
                    operation = QTextCursor.MoveOperation.EndOfBlock
        else:
            match key:
                case Qt.Key.Key_Left:
                    operation = QTextCursor.MoveOperation.Left
                case Qt.Key.Key_Right:
                    operation = QTextCursor.MoveOperation.Right
                case Qt.Key.Key_Up:
                    operation = QTextCursor.MoveOperation.Up
                case Qt.Key.Key_Down:
                    operation = QTextCursor.MoveOperation.Down
                case Qt.Key.Key_Home:
                    operation = QTextCursor.MoveOperation.StartOfLine
                case Qt.Key.Key_End:
                    operation = QTextCursor.MoveOperation.EndOfLine

        if mode is not None and operation is not None:
            self.__cursor.movePosition(operation, mode)
            self.repaintRequest.emit()
