import re

from PySide6.QtCore import (
    Signal,
    QObject,
    QRegularExpression,
    QRegularExpressionMatch,
    QRegularExpressionMatchIterator,
    Qt,
)
from PySide6.QtGui import QTextDocument, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QBrush, QColor, QFont


class SearchComponent(QSyntaxHighlighter):
    repaintRequest: Signal = Signal()
    updateUIRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__(cursor.document())

        self.__cursor: QTextCursor = cursor

        self.__search_data: str = ""

        self.__is_regex_turned: bool = False
        self.__is_case_turned: bool = False
        self.__is_whole_turned: bool = False

        self.__background_color: QColor = QColor("yellow")

        self.__expr: QRegularExpression = QRegularExpression()

    def isRegexTurned(self) -> bool:
        return self.__is_regex_turned

    def setRegexTurned(self, is_turned: bool) -> None:
        self.__is_regex_turned = is_turned
        self.updateExpr()

    def isCaseTurned(self) -> bool:
        return self.__is_case_turned

    def setCaseTurned(self, is_turned: bool) -> None:
        self.__is_case_turned = is_turned
        self.updateExpr()

    def isWholeTurned(self) -> bool:
        return self.__is_whole_turned

    def setWholeTurned(self, is_turned: bool) -> None:
        self.__is_whole_turned = is_turned
        self.updateExpr()

    def find(self, search_data: str) -> None:
        self.__search_data = search_data
        self.updateExpr()

        options: QTextDocument.FindFlag = QTextDocument.FindFlag(0)
        if self.__is_case_turned:
            options |= QTextDocument.FindFlag.FindCaseSensitively

        if self.__is_whole_turned:
            options |= QTextDocument.FindFlag.FindWholeWords

        new_cursor: QTextCursor = self.__cursor.document().find(self.__expr, self.__cursor, options)

        if new_cursor.position() == -1:
            new_cursor = self.__cursor.document().find(self.__expr, 0, options)

        if new_cursor.position() != -1:
            self.__cursor.setPosition(new_cursor.position())

        self.repaintRequest.emit()
        self.updateUIRequest.emit()

    def highlightBlock(self, text: str) -> None:
        char_format: QTextCharFormat = QTextCharFormat()
        char_format.setBackground(self.__background_color)

        if self.__expr.isValid():
            it: QRegularExpressionMatchIterator = self.__expr.globalMatch(text)
            while it.hasNext():
                match: QRegularExpressionMatch = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)

    def updateExpr(self) -> None:
        pattern: str = self.__search_data

        if not self.__is_regex_turned:
            pattern = re.escape(pattern)

        if self.__is_whole_turned:
            pattern = "\\b" + pattern + "\\b"

        self.__expr.setPattern(pattern)

        options: QRegularExpression.PatternOption = QRegularExpression.PatternOption.NoPatternOption
        if not self.__is_case_turned:
            options |= QRegularExpression.PatternOption.CaseInsensitiveOption

        self.__expr.setPatternOptions(options)

        self.rehighlight()
        self.repaintRequest.emit()
