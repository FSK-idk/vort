from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor


class Component(QObject):
    applied = Signal()

    def __init__(self, text_cursor: QTextCursor) -> None:
        super().__init__()
        self._text_cursor: QTextCursor = text_cursor
