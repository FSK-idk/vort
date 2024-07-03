from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor

# TODO: make slots, private cursor


class Component(QObject):
    applied = Signal()

    def __init__(self, text_cursor: QTextCursor) -> None:
        super().__init__()
        self.text_cursor: QTextCursor = text_cursor
