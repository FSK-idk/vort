from PySide6.QtGui import QTextCharFormat

from core.widget.text_editor.component.component import Component


class FontComponent(Component):
    def setFontFamily(self, font_family: str) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamily(font_family)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setFontSize(self, font_size: int) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(font_size)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()
