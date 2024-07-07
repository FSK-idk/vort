from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QTextDocument,
    QPainter,
    QTextCursor,
    QColor,
    QTextDocument,
    QTextCursor,
    QColor,
    QPaintEvent,
    QPainter,
    QPalette,
)

from util import RectF

from core.widget.text_editor.layout.text_document_layout import TextDocumentLayout, Selection, PaintContext

from core.widget.text_editor.layout.footer_document_layout import FooterDocumentLayout, FooterPaintContext
from core.widget.text_editor.layout.header_document_layout import HeaderDocumentLayout, HeaderPaintContext


from core.widget.text_editor.layout.page_layout import PageLayout


class TextCanvas(QWidget):
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

        self.__header_document: QTextDocument = QTextDocument()
        self.__header_document_layout: HeaderDocumentLayout = HeaderDocumentLayout(
            self.__header_document, self.__page_layout
        )
        self.__header_document.setDocumentLayout(self.__header_document_layout)

        self.__footer_document: QTextDocument = QTextDocument()
        self.__footer_document_layout: FooterDocumentLayout = FooterDocumentLayout(
            self.__footer_document, self.__page_layout
        )
        self.__footer_document.setDocumentLayout(self.__footer_document_layout)

        self.setFixedWidth(int(self.__page_layout.width()))
        self.setFixedHeight(int(self.__page_layout.height()))

        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        self.setPalette(palette)

        self.__page_layout.layoutSizeChanged.connect(self.onPageCountChanged)

    def headerLayout(self) -> HeaderDocumentLayout:
        return self.__header_document_layout

    def footerLayout(self) -> FooterDocumentLayout:
        return self.__footer_document_layout

    def onPageCountChanged(self) -> None:
        self.setFixedWidth(int(self.__page_layout.width()))
        self.setFixedHeight(int(self.__page_layout.height()))

    def paintEvent(self, event: QPaintEvent):
        painter: QPainter = QPainter(self)

        # paint pages, text and images

        # TODO: to config
        cursor_selection: Selection = Selection()
        if self.__text_cursor.hasSelection():
            cursor_selection.start = self.__text_cursor.selectionStart()
            cursor_selection.end = self.__text_cursor.selectionEnd()
            cursor_selection.format.setBackground(QColor("blue"))
            cursor_selection.format.setForeground(QColor("white"))

        context: PaintContext = PaintContext()
        context.painter = painter
        context.rect = RectF.fromQRect(event.rect())
        context.cursor_position = self.__text_cursor.position()
        context.cursor_selection = cursor_selection

        self.__text_document_layout.paint(context)

        # # paint header

        header_context: HeaderPaintContext = HeaderPaintContext()
        header_context.painter = painter
        header_context.rect = RectF.fromQRect(event.rect())

        self.__header_document_layout.paint(header_context)

        # paint footer

        footer_context: FooterPaintContext = FooterPaintContext()
        footer_context.painter = painter
        footer_context.rect = RectF.fromQRect(event.rect())

        self.__footer_document_layout.paint(footer_context)

        painter.end()
