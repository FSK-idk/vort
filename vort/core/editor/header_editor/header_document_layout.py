from PySide6.QtCore import QPointF, QRectF, Qt, Slot, Signal
from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QTextDocument,
    QTextBlock,
    QTextLayout,
    QTextLine,
    QPainter,
    QTextBlockFormat,
)

from core.editor.page_layout.page_layout import PageLayout
from core.editor.document_paint_context import DocumentPaintContext


class HeaderDocumentLayout(QAbstractTextDocumentLayout):
    pageCountChanged: Signal = Signal(int)

    def __init__(self, document: QTextDocument, page_layout: PageLayout) -> None:
        super().__init__(document)

        self.__page_layout: PageLayout = page_layout

        self.__page_layout.pageCountChanged.connect(self.pageCountChanged.emit)
        self.__page_layout.internalChanged.connect(self.onPageLayoutInternalChanged)

    def pageCount(self) -> int:
        return self.__page_layout.pageCount()

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        for i in range(self.document().blockCount() - 1):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_format: QTextBlockFormat = block.blockFormat()
            block_layout: QTextLayout = block.layout()

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()

            while line.isValid():
                line.setLineWidth(self.__page_layout.textWidth())
                line_rect: QRectF = line.naturalTextRect()

                line_x: float = self.__page_layout.headerXPosition(i)
                line_y: float = self.__page_layout.headerYPosition(i)

                # change x position
                if Qt.AlignmentFlag.AlignLeft in block_format.alignment():
                    line_x += 0

                elif Qt.AlignmentFlag.AlignHCenter in block_format.alignment():
                    line_x += (self.__page_layout.textWidth() - line_rect.width()) / 2

                elif Qt.AlignmentFlag.AlignRight in block_format.alignment():
                    line_x += self.__page_layout.textWidth() - line_rect.width()

                # change y position
                if Qt.AlignmentFlag.AlignTop in block_format.alignment():
                    line_y += 0

                elif Qt.AlignmentFlag.AlignVCenter in block_format.alignment():
                    line_y += (self.__page_layout.headerHeight() - line_rect.height()) / 2

                elif Qt.AlignmentFlag.AlignBottom in block_format.alignment():
                    line_y += self.__page_layout.headerHeight() - line_rect.height()

                line.setLineWidth(line_rect.width())
                line.setPosition(QPointF(line_x, line_y))

                line = block_layout.createLine()

            block_layout.endLayout()

        self.update.emit()

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def paint(self, context: DocumentPaintContext):
        painter: QPainter = context.painter
        rect: QRectF = context.rect

        for i in range(self.document().blockCount() - 1):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_layout.draw(painter, QPointF(0, 0), [], rect)

    @Slot()
    def onPageLayoutInternalChanged(self) -> None:
        self.documentChanged(0, 0, 0)
