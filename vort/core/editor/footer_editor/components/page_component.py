from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor


class PageComponent(QObject):
    applied: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()

        self.__cursor: QTextCursor = cursor

        self.__is_first_page_included: bool = False
        self.__page_count: int = 0

    def pageCount(self) -> int:
        return self.__page_count

    def addPage(self, count: int = 1) -> None:
        if count != 0:
            for i in range(count):
                self.__cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
                self.__cursor.insertBlock()

            self.__page_count += count
            self.applied.emit()

    def removePage(self, count: int = 1) -> None:
        if count != 0:
            for i in range(count):
                self.__cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
                self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                self.__cursor.deleteChar()

            self.__page_count -= count
            self.applied.emit()

    def isFirstPageIncluded(self) -> bool:
        return self.__is_first_page_included

    def setFirstPageIncluded(self, is_included):
        if self.__is_first_page_included != is_included:
            self.__is_first_page_included = is_included
            self.applied.emit()
