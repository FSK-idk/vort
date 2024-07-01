from PySide6.QtGui import QFont, QTextCharFormat

from core.widget.text_editor.component.component import Component


class FormatComponent(Component):
    def turnBold(self, is_bold: bool) -> None:
        font_weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(font_weight)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def turnItalic(self, is_italic: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontItalic(is_italic)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def turnUnderlined(self, is_underlined: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontUnderline(is_underlined)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()
