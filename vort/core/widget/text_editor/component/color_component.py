from PySide6.QtGui import QTextCharFormat, QColor

from core.widget.text_editor.component.component import Component


class ColorComponent(Component):
    def setForegroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setForeground(color)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setBackgroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(color)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()
