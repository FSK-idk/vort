from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QTextDocument, QTextCursor


class HistoryComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def undo(self) -> None:
        document: QTextDocument = self.__cursor.document()
        if document.isUndoAvailable():
            document.undo(self.__cursor)
            self.repaintRequest.emit()

    def redo(self) -> None:
        document: QTextDocument = self.__cursor.document()
        if document.isRedoAvailable():
            document.redo(self.__cursor)
            self.repaintRequest.emit()
