from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QGuiApplication, QKeyEvent

from util.point_f import PointF

from core.widget.text_editor.component.component import Component
from core.widget.text_editor.text_canvas import TextCanvas


class InputComponent(Component):
    def input(self, event: QKeyEvent) -> None:
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
            self.applied.emit()

        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
            match event.key():
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Enter:
                    return  # ignore
                case Qt.Key.Key_Escape:
                    return  # ignore
                case _ if event.text():
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertText(event.text())
                    self.text_cursor.endEditBlock()
            self.applied.emit()
