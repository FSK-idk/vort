from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QTextCursor


class DocumentPaintContext:
    def __init__(
        self,
        painter: QPainter,
        rect: QRectF,
        cursor: QTextCursor,
    ) -> None:
        self.painter: QPainter = painter
        self.rect: QRectF = rect
        self.cursor: QTextCursor = cursor
