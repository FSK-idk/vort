from PySide6.QtGui import QTextCharFormat, QGuiApplication, QFont

from core.widget.text_editor.component.component import Component


class FontComponent(Component):
    def setFontFamily(self, font_family: str) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamily(font_family)
        self._text_cursor.mergeCharFormat(format)
        self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setFontSize(self, font_size: int) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(font_size)
        self._text_cursor.mergeCharFormat(format)
        self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()
