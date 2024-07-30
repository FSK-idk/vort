from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPaintEvent, QPainter, QPalette, QColor


from core.editor.text_editor.text_document_context import TextDocumentContext
from core.editor.header_editor.header_document_context import HeaderDocumentContext
from core.editor.footer_editor.footer_document_context import FooterDocumentContext
from core.editor.document_paint_context import DocumentPaintContext


class DocumentCanvas(QWidget):
    def __init__(
        self,
        text_context: TextDocumentContext,
        header_context: HeaderDocumentContext,
        footer_context: FooterDocumentContext,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.__text_context = text_context
        self.__header_context = header_context
        self.__footer_context = footer_context

        palette = self.palette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
        self.setPalette(palette)

    def paintEvent(self, event: QPaintEvent):
        painter: QPainter = QPainter(self)

        # text

        context: DocumentPaintContext = DocumentPaintContext(
            painter, event.rect().toRectF(), self.__text_context.cursor
        )
        self.__text_context.layout.paint(context)

        # header

        context: DocumentPaintContext = DocumentPaintContext(
            painter, event.rect().toRectF(), self.__header_context.cursor
        )
        self.__header_context.layout.paint(context)

        # footer

        context: DocumentPaintContext = DocumentPaintContext(
            painter, event.rect().toRectF(), self.__footer_context.cursor
        )
        self.__footer_context.layout.paint(context)

        painter.end()
