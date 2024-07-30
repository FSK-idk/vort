from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextBlockFormat


class FormattingComponent(QObject):
    applied: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()

        self.__cursor: QTextCursor = cursor

        self.__alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter

        self.__font_family: str = ""
        self.__font_size: int = 16

        self.__text_foreground_color: QColor = QColor("black")
        self.__text_background_color: QColor = QColor("transparent")

    def alignment(self) -> Qt.AlignmentFlag:
        return self.__alignment

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        if self.__alignment != alignment:
            self.__alignment = alignment
            self.formatDocument()

    def fontFamily(self) -> str:
        return self.__font_family

    def setFontFamily(self, family: str) -> None:
        if self.__font_family != family:
            self.__font_family = family
            self.formatDocument()

    def fontSize(self) -> int:
        return self.__font_size

    def setFontSize(self, size: int) -> None:
        if self.__font_size != size:
            self.__font_size = size
            self.formatDocument()

    def textForegroundColor(self) -> QColor:
        return self.__text_foreground_color

    def setTextForegroundColor(self, color: QColor) -> None:
        if self.__text_foreground_color != color:
            self.__text_foreground_color = color
            self.formatDocument()

    def textBackgroundColor(self) -> QColor:
        return self.__text_background_color

    def setTextBackgroundColor(self, color: QColor) -> None:
        if self.__text_background_color != color:
            self.__text_background_color = color
            self.formatDocument()

    def formatDocument(self) -> None:
        char_format: QTextCharFormat = QTextCharFormat()
        char_format.setFontFamilies([self.__font_family])
        char_format.setFontPointSize(self.__font_size)
        char_format.setBackground(self.__text_background_color)
        char_format.setForeground(self.__text_foreground_color)

        block_format: QTextBlockFormat = QTextBlockFormat()
        block_format.setAlignment(self.__alignment)

        self.__cursor.select(QTextCursor.SelectionType.Document)
        self.__cursor.setCharFormat(char_format)
        self.__cursor.setBlockCharFormat(char_format)
        self.__cursor.setBlockFormat(block_format)

        self.applied.emit()
