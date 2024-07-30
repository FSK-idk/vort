from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextCursor


class CharComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def fontFamily(self) -> str:
        if self.__cursor.charFormat().fontFamilies():
            return self.__cursor.charFormat().fontFamilies()[0]
        return ""

    def setFontFamily(self, family: str) -> None:
        if self.fontFamily() == family:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamilies([family])
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def fontSize(self) -> int:
        return int(self.__cursor.charFormat().fontPointSize())

    def setFontSize(self, size: int) -> None:
        if self.fontSize() == size:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(size)
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def foregroundColor(self) -> QColor:
        return self.__cursor.charFormat().foreground().color()

    def setForegroundColor(self, color: QColor) -> None:
        if self.foregroundColor() == color:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setForeground(color)
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def backgroundColor(self) -> QColor:
        return self.__cursor.charFormat().background().color()

    def setBackgroundColor(self, color: QColor) -> None:
        if self.backgroundColor() == color:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(color)
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def isBold(self) -> bool:
        return self.__cursor.charFormat().fontWeight() == QFont.Weight.Bold

    def setBold(self, is_bold: bool) -> None:
        if self.isBold == is_bold:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(QFont.Weight.Bold if is_bold else QFont.Weight.Normal)
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def isItalic(self) -> bool:
        return self.__cursor.charFormat().fontItalic()

    def setItalic(self, is_italic: bool) -> None:
        if self.isItalic() == is_italic:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setFontItalic(is_italic)
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def isUnderlined(self) -> bool:
        return self.__cursor.charFormat().underlineStyle() == QTextCharFormat.UnderlineStyle.SingleUnderline

    def setUnderlined(self, is_underlined: bool) -> None:
        if self.isUnderlined == is_underlined:
            return

        self.__cursor.beginEditBlock()

        format: QTextCharFormat = QTextCharFormat()
        format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline if is_underlined else QTextCharFormat.UnderlineStyle.NoUnderline)  # type: ignore
        self.__cursor.mergeCharFormat(format)

        self.fixup()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def fixup(self) -> None:
        selection_start: int = self.__cursor.selectionStart()

        if self.__cursor.hasSelection():
            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            if helper.atBlockStart():
                format = helper.charFormat()
                format.setAnchorHref("")
                format.setAnchor(False)
                helper.mergeBlockCharFormat(format)
        else:
            if self.__cursor.atBlockStart():
                format = self.__cursor.charFormat()
                format.setAnchorHref("")
                format.setAnchor(False)
                self.__cursor.mergeBlockCharFormat(format)
