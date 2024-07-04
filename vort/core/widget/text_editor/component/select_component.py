from PySide6.QtGui import QTextCursor

from core.widget.text_editor.component.component import Component


class SelectComponent(Component):
    def selectAll(self) -> None:
        self._text_cursor.select(QTextCursor.SelectionType.Document)
        self.applied.emit()
