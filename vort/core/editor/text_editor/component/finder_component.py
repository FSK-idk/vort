from PySide6.QtCore import (
    Signal,
    QRegularExpression,
    QRegularExpressionMatch,
    QRegularExpressionMatchIterator,
)
from PySide6.QtGui import QTextDocument, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor


class FinderComponent(QSyntaxHighlighter):
    repaintRequest: Signal = Signal()
    updateUIRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__(cursor.document())

        self.__cursor: QTextCursor = cursor

        self.__find_data: str = ""

        self.__is_regex_turned: bool = False
        self.__is_case_turned: bool = False
        self.__is_whole_turned: bool = False

        self.__background_color: QColor = QColor("yellow")

        self.__expr: QRegularExpression = QRegularExpression()
        self.__exact_expr: QRegularExpression = QRegularExpression()

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

    def find(self, find_data: str) -> None:
        self.__find_data = find_data
        self.updateExpr()

        options: QTextDocument.FindFlag = QTextDocument.FindFlag(0)
        if self.__is_case_turned:
            options |= QTextDocument.FindFlag.FindCaseSensitively

        if self.__is_whole_turned:
            options |= QTextDocument.FindFlag.FindWholeWords

        helper: QTextCursor = self.__cursor.document().find(self.__expr, self.__cursor, options)
        if helper.position() == -1:
            helper = self.__cursor.document().find(self.__expr, 0, options)

        if helper.position() != -1:
            self.__cursor.setPosition(helper.selectionStart())
            self.__cursor.setPosition(helper.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
        else:
            self.__cursor.clearSelection()

        self.repaintRequest.emit()
        self.updateUIRequest.emit()

    def replace(self, replace_data: str) -> None:
        helper: QTextCursor = QTextCursor(self.__cursor.document())

        if self.__exact_expr.match(self.__cursor.selectedText()).hasMatch():
            helper.setPosition(self.__cursor.selectionStart())
            helper.setPosition(self.__cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
            helper.insertText(replace_data)

        else:
            self.find(self.__find_data)

        self.repaintRequest.emit()

    def replaceAll(self, replace_data: str) -> None:
        self.__cursor.beginEditBlock()

        options: QTextDocument.FindFlag = QTextDocument.FindFlag(0)
        if self.__is_case_turned:
            options |= QTextDocument.FindFlag.FindCaseSensitively

        if self.__is_whole_turned:
            options |= QTextDocument.FindFlag.FindWholeWords

        helper: QTextCursor = self.__cursor.document().find(self.__expr, self.__cursor, options)
        if helper.position() == -1:
            helper = self.__cursor.document().find(self.__expr, 0, options)

        while helper.position() != -1:
            helper.insertText(replace_data)

            helper = self.__cursor.document().find(self.__expr, self.__cursor, options)
            if helper.position() == -1:
                helper = self.__cursor.document().find(self.__expr, 0, options)

        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def highlightBlock(self, text: str) -> None:
        char_format: QTextCharFormat = QTextCharFormat()
        char_format.setBackground(self.__background_color)

        if self.__expr.isValid():
            it: QRegularExpressionMatchIterator = self.__expr.globalMatch(text)
            while it.hasNext():
                match: QRegularExpressionMatch = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)

    def updateExpr(self) -> None:
        pattern: str = self.__find_data

        if not self.__is_regex_turned:
            pattern = QRegularExpression.escape(pattern)

        if self.__is_whole_turned:
            pattern = "\\b" + pattern + "\\b"

        self.__expr.setPattern(pattern)
        self.__exact_expr.setPattern(QRegularExpression.anchoredPattern(pattern))

        options: QRegularExpression.PatternOption = QRegularExpression.PatternOption.NoPatternOption
        if not self.__is_case_turned:
            options |= QRegularExpression.PatternOption.CaseInsensitiveOption

        self.__expr.setPatternOptions(options)
        self.__exact_expr.setPatternOptions(self.__exact_expr.patternOptions() | options)

        self.rehighlight()
        self.repaintRequest.emit()
