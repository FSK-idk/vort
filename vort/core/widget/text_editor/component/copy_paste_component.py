from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QTextDocumentFragment

from core.widget.text_editor.component.component import Component


class CopyPasteComponent(Component):
    def cut(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.text_cursor.removeSelectedText()
            self.applied.emit()

    def copy(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.applied.emit()

    def paste(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        if mime_data.hasHtml():
            self.text_cursor.insertFragment(QTextDocumentFragment.fromHtml(mime_data.html()))
        else:
            self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.applied.emit()

    def pastePlain(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.applied.emit()
