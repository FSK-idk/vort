from PySide6.QtGui import QTextDocument

from core.widget.text_editor.component.component import Component


class HistoryComponent(Component):
    def undo(self) -> None:
        text_document: QTextDocument = self.text_cursor.document()
        text_document.undo(self.text_cursor)
        self.applied.emit()

    def redo(self) -> None:
        text_document: QTextDocument = self.text_cursor.document()
        text_document.redo(self.text_cursor)
        self.applied.emit()
