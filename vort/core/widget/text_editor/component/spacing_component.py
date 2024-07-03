from PySide6.QtGui import QTextBlockFormat, QTextCursor, QGuiApplication

from core.widget.text_editor.component.component import Component


class SpacingComponent(Component):
    def __init__(self, text_cursor: QTextCursor) -> None:
        super().__init__(text_cursor)

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        # TODO: to config
        self.__default_first_line_indent: float = 10 * dpi / 25.4

    def isFirstLineIndentTurned(self) -> bool:
        return self.text_cursor.blockFormat().textIndent() != 0

    def turnFirstLineIndent(self, is_indent: bool) -> None:
        indent = self.__default_first_line_indent if is_indent else 0
        format: QTextBlockFormat = QTextBlockFormat()
        format.setTextIndent(indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def firstLineIndent(self) -> float:
        return self.text_cursor.blockFormat().textIndent()

    def setFirstLineIndent(self, indent: float) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setTextIndent(indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def indent(self) -> int:
        return self.text_cursor.blockFormat().indent()

    def setIndent(self, indent: int) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def indentRight(self) -> None:
        indent = self.text_cursor.blockFormat().indent() + 1
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def indentLeft(self) -> None:
        indent = max(self.text_cursor.blockFormat().indent() - 1, 0)
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def lineSpacing(self) -> float:
        return self.text_cursor.blockFormat().lineHeight()

    def setLineSpacing(self, spacing) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setLineHeight(spacing, 1)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def topMargin(self) -> float:
        return self.text_cursor.blockFormat().topMargin()

    def setTopMargin(self, margin) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setTopMargin(margin)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def bottomMargin(self) -> float:
        return self.text_cursor.blockFormat().bottomMargin()

    def setBottomMargin(self, margin) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setBottomMargin(margin)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def leftMargin(self) -> float:
        return self.text_cursor.blockFormat().leftMargin()

    def setLeftMargin(self, margin) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setLeftMargin(margin)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()

    def rightMargin(self) -> float:
        return self.text_cursor.blockFormat().rightMargin()

    def setRightMargin(self, margin) -> None:
        format: QTextBlockFormat = QTextBlockFormat()
        format.setRightMargin(margin)
        self.text_cursor.mergeBlockFormat(format)
        self.applied.emit()