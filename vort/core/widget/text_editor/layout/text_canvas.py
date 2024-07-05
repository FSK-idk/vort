from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QGraphicsTextItem, QStyleOptionGraphicsItem
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

from core.widget.text_editor.layout.text_document_layout import (
    TextDocumentLayout,
    Selection,
    PaintContext,
    HitResult,
)

from core.widget.text_editor.layout.footer_document_layout import FooterDocumentLayout, FooterPaintContext


from core.widget.text_editor.layout.page_layout import PageLayout


class TextCanvas(QWidget):
    sizeChanged = Signal(PointF)
    characterCountChanged = Signal(int)
    pageCountChanged = Signal(int)

    def __init__(
        self,
        page_layout: PageLayout,
        text_document_layout: TextDocumentLayout,
        text_cursor: QTextCursor,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.__page_layout: PageLayout = page_layout
        self.__text_document_layout: TextDocumentLayout = text_document_layout
        self.__text_cursor: QTextCursor = text_cursor

        self.__footer_document: QTextDocument = QTextDocument()
        self.__footer_document_layout: FooterDocumentLayout = FooterDocumentLayout(
            self.__footer_document, self.__page_layout
        )
        self.__footer_document.setDocumentLayout(self.__footer_document_layout)

        self.__is_footer_shown: bool = False

        self.setFixedWidth(int(self.__page_layout.width()))
        self.setFixedHeight(int(self.__page_layout.height()))

        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        self.setPalette(palette)

        self.__text_document_layout.characterCountChanged.connect(self.characterCountChanged.emit)
        self.__page_layout.pageCountChanged.connect(self.onPageCountChanged)

    def setFooterShown(self, is_shown: bool) -> None:
        self.__is_footer_shown = is_shown

    def pageWidth(self) -> float:
        return self.__page_layout.pageWidth()

    def pageHeight(self) -> float:
        return self.__page_layout.pageHeight()

    def hitTest(self, point: PointF) -> HitResult:
        return self.__text_document_layout.hitTest(point)

    def blockTest(self, position: int) -> PointF:
        return self.__text_document_layout.blockTest(position)

    def onPageCountChanged(self, size: PointF) -> None:
        self.setFixedWidth(int(self.__page_layout.width()))
        self.setFixedHeight(int(self.__page_layout.height()))
        self.sizeChanged.emit(PointF(self.__page_layout.width(), self.__page_layout.height()))

    def paintEvent(self, event: QPaintEvent):
        painter: QPainter = QPainter(self)

        # paint papers and text and images

        # TODO: to config
        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(QColor("blue"))
        format.setForeground(QColor("white"))

        cursor_selection: Selection = Selection()
        if self.__text_cursor.hasSelection():
            cursor_selection.start = self.__text_cursor.selectionStart()
            cursor_selection.end = self.__text_cursor.selectionEnd()
            cursor_selection.format.setBackground(QColor("blue"))
            cursor_selection.format.setForeground(QColor("white"))

        context: PaintContext = PaintContext()
        context.painter = painter
        context.viewport_rect = RectF.fromQRect(event.rect())
        context.cursor_position = self.__text_cursor.position()
        context.cursor_selection = cursor_selection
        # TODO: to config
        context.page_color = QColor("white")

        self.__text_document_layout.paint(context)

        # paint footer
        footer_context: FooterPaintContext = FooterPaintContext()
        footer_context.painter = painter
        footer_context.viewport_rect = RectF.fromQRect(event.rect())

        if self.__is_footer_shown:
            self.__footer_document_layout.paint(footer_context)
