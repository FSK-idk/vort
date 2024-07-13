from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QTextBlockFormat, QTextCursor


class ParagraphComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def alignment(self) -> Qt.AlignmentFlag:
        return self.__cursor.blockFormat().alignment()

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        if self.alignment() == alignment:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setAlignment(alignment)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def firstLineIndent(self) -> float:
        return self.__cursor.blockFormat().textIndent()

    def setFirstLineIndent(self, indent: float) -> None:
        if self.firstLineIndent() == indent:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setTextIndent(indent)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def indent(self) -> int:
        return self.__cursor.blockFormat().indent()

    def setIndent(self, indent: int) -> None:
        if self.indent() == indent:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def indentRight(self) -> None:
        indent = self.__cursor.blockFormat().indent() + 1
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def indentLeft(self) -> None:
        if self.indent() < 1:
            return

        indent = self.__cursor.blockFormat().indent() - 1
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(indent)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def lineSpacing(self) -> float:
        return self.__cursor.blockFormat().lineHeight()

    def setLineSpacing(self, spacing) -> None:
        if self.lineSpacing() == spacing:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setLineHeight(spacing, 1)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def topMargin(self) -> float:
        return self.__cursor.blockFormat().topMargin()

    def setTopMargin(self, margin) -> None:
        if self.topMargin() == margin:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setTopMargin(margin)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def bottomMargin(self) -> float:
        return self.__cursor.blockFormat().bottomMargin()

    def setBottomMargin(self, margin) -> None:
        if self.bottomMargin() == margin:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setBottomMargin(margin)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def leftMargin(self) -> float:
        return self.__cursor.blockFormat().leftMargin()

    def setLeftMargin(self, margin) -> None:
        if self.leftMargin() == margin:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setLeftMargin(margin)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()

    def rightMargin(self) -> float:
        return self.__cursor.blockFormat().rightMargin()

    def setRightMargin(self, margin) -> None:
        if self.rightMargin() == margin:
            return

        format: QTextBlockFormat = QTextBlockFormat()
        format.setRightMargin(margin)
        self.__cursor.mergeBlockFormat(format)
        self.repaintRequest.emit()
