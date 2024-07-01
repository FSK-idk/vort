from PySide6.QtGui import QTextDocument

from core.widget.text_editor.component.component import Component


class HistoryComponent(Component):
    def undo(self) -> None:
        document: QTextDocument = self.text_cursor.document()
        document.undo(self.text_cursor)
        self.applied.emit()

    def redo(self) -> None:
        document: QTextDocument = self.text_cursor.document()
        document.redo(self.text_cursor)
        self.applied.emit()
