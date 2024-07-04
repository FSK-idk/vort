from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QTextDocument,
    QPainter,
    QTextCursor,
    QTextCharFormat,
    QColor,
    QTextDocument,
    QTextCursor,
    QColor,
    QPaintEvent,
    QPainter,
    QTextCharFormat,
    QPalette,
)

from util import RectF, PointF

from core.widget.text_editor.text_document_layout import TextDocumentLayout, Selection, PaintContext, HitResult


class TextCanvas(QWidget):
    sizeChanged = Signal(PointF)
    characterCountChanged = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__text_document_layout: TextDocumentLayout | None = None
        self.__text_cursor: QTextCursor | None = None

        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        self.setPalette(palette)

    def pageWidth(self) -> float:
        if self.__text_document_layout is not None:
            return self.__text_document_layout.page_layout.pageWidth()
        return 0

    def pageHeight(self) -> float:
        if self.__text_document_layout is not None:
            return self.__text_document_layout.page_layout.pageHeight()
        return 0

    def setTextContext(self, text_document: QTextDocument, text_cursor: QTextCursor) -> None:
        if self.__text_document_layout is not None:
            self.__text_document_layout.characterCountChanged.disconnect(self.characterCountChanged.emit)
            self.__text_document_layout.sizeChanged.disconnect(self.onSizeChanged)

        self.__text_document_layout = TextDocumentLayout(text_document)
        self.setFixedWidth(int(self.__text_document_layout.page_layout.width()))
        self.setFixedHeight(int(self.__text_document_layout.page_layout.height()))
        self.__text_cursor = text_cursor
        self.__text_document_layout.characterCountChanged.connect(self.characterCountChanged.emit)
        self.__text_document_layout.sizeChanged.connect(self.onSizeChanged)
        text_document.setDocumentLayout(self.__text_document_layout)

    def clearContext(self) -> None:
        if self.__text_document_layout is not None:
            self.__text_document_layout.characterCountChanged.disconnect(self.characterCountChanged.emit)
            self.__text_document_layout.sizeChanged.disconnect(self.onSizeChanged)

        self.__text_document_layout = None
        self.__text_cursor = None

    def hitTest(self, point: PointF) -> HitResult:
        if self.__text_document_layout is not None:
            return self.__text_document_layout.hitTest(point)
        return HitResult()

    def blockTest(self, position: int) -> PointF:
        if self.__text_document_layout is not None:
            return self.__text_document_layout.blockTest(position)
        return PointF(-1, -1)

    def onSizeChanged(self, size: PointF) -> None:
        if self.__text_document_layout is not None:
            self.setFixedWidth(int(self.__text_document_layout.page_layout.width()))
            self.setFixedHeight(int(self.__text_document_layout.page_layout.height()))
            self.sizeChanged.emit(size)

    def paintEvent(self, event: QPaintEvent):
        if self.__text_document_layout is None or self.__text_cursor is None:
            return

        painter: QPainter = QPainter(self)

        # TODO: to config
        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(QColor("blue"))
        format.setForeground(QColor("white"))

        cursor_selection: Selection | None = None
        if self.__text_cursor.hasSelection():
            selection_start: int = self.__text_cursor.selectionStart()
            selection_end: int = self.__text_cursor.selectionEnd()
            cursor_selection = Selection(selection_start, selection_end, format)

        context = PaintContext()
        context.painter = painter
        context.viewport_rect = RectF.fromQRect(event.rect())
        context.cursor_position = self.__text_cursor.position()
        context.cursor_selection = cursor_selection
        # TODO: to config
        context.page_color = QColor("white")

        self.__text_document_layout.paint(context)
        return
