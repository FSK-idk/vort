from PySide6.QtGui import QTextBlockFormat, QTextCursor

from core.widget.text_editor.component.component import Component


class IndentComponent(Component):
    def __init__(self, text_cursor: QTextCursor) -> None:
        super().__init__(text_cursor)
        self.__first_line_indent = 48
        self.__paragraph_indent = 48

    def turnFirstLineIndent(self, is_indent) -> None:
        new_indent = self.__first_line_indent if is_indent else 0
        format: QTextBlockFormat = QTextBlockFormat()
        format.setTextIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def indentParagraphRight(self) -> None:
        new_indent: int = self.text_cursor.blockFormat().indent() + self.__paragraph_indent
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def indentParagraphLeft(self) -> None:
        new_indent: int = self.text_cursor.blockFormat().indent() - self.__paragraph_indent
        if new_indent < 0:
            return
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()
