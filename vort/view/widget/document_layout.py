from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QTextDocument,
    QTextBlock,
    QTextLayout,
    QTextLine,
    QPainter,
    QTextCursor,
    QTextFrame,
    QFont,
    QFontMetricsF,
    QPalette,
    QTextFrameFormat,
    QPen,
    QColor,
    QBrush,
)
from PySide6.QtCore import QPointF, QRectF, QSizeF, Qt, QObject, Signal

from utils import PointF, RectF

from model.page_layout import PageLayout
from model.page import Page


class PaintContext:
    def __init__(
        self,
        rect: RectF = RectF(),
        cursor_position: int = -1,
        palette: QPalette = QPalette(),
    ) -> None:
        self.rect: RectF = rect
        self.cursor_position: int = cursor_position
        self.palette: QPalette = palette


class DocumentLayout(QAbstractTextDocumentLayout):
    def __init__(
        self,
        document: QTextDocument,
    ) -> None:
        super().__init__(document)

        page_spacing: float = 10

        self.page_layout: PageLayout = PageLayout(spacing=page_spacing)
        # has at least one page
        self.page_layout.addPage()

        # root_frame: QTextFrame = self.document.rootFrame()
        # root_frame_format: QTextFrameFormat = root_frame.frameFormat()
        # root_frame_format.setWidth(self.__page_width)
        # root_frame_format.setHeight(self.__page_height)
        # root_frame_format.setMargin(self.__page_margin)
        # root_frame_format.setPadding(self.__page_padding)
        # root_frame_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash)
        # root_frame_format.setBorderBrush(QBrush(Qt.GlobalColor.blue))
        # root_frame_format.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_Auto)
        # self.document.rootFrame().setFrameFormat(root_frame_format)

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        old_page_count: int = self.page_layout.pageCount()

        current_page_index: int = 0
        current_page: Page = self.page_layout.getPage(current_page_index)

        current_page_width: float = current_page.textWidth()
        current_page_height: float = current_page.textHeight()

        current_x_position: float = current_page.xPosition() + current_page.margin() + current_page.padding()
        current_y_position: float = current_page.yPosition() + current_page.margin() + current_page.padding()

        for i in range(self.document().blockCount()):
            block_layout: QTextLayout = self.document().findBlockByNumber(i).layout()

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()
            while line.isValid():
                line.setLineWidth(current_page_width)
                line.setPosition(QPointF(current_x_position, current_y_position))

                while current_page_height - line.height() < 0:
                    current_page_index += 1
                    if self.page_layout.pageCount() == current_page_index:
                        self.page_layout.addPage()
                    current_page = self.page_layout.getPage(current_page_index)

                    current_page_width = current_page.textWidth()
                    current_page_height = current_page.textHeight()

                    current_x_position = current_page.xPosition() + current_page.margin() + current_page.padding()
                    current_y_position = current_page.yPosition() + current_page.margin() + current_page.padding()

                    line.setLineWidth(current_page_width)
                    line.setPosition(QPointF(current_x_position, current_y_position))

                current_y_position += line.height()
                current_page_height -= line.height()

                line = block_layout.createLine()

            block_layout.endLayout()

        while self.page_layout.pageCount() > current_page_index + 1:
            self.page_layout.deleteLastPage()

        self.update.emit()

        if old_page_count != self.page_layout.pageCount():
            self.pageCountChanged.emit(self.page_layout.pageCount())

    def draw(self, painter: QPainter, context: PaintContext):
        self.drawPage(painter, context)
        self.drawText(painter, context)

        self.update.emit()

    def drawPage(self, painter: QPainter, context: PaintContext) -> None:
        rect: RectF = context.rect
        cursor_position: int = context.cursor_position
        palette: QPalette = context.palette

        painter.setBrush(QColor("white"))
        painter.setPen(QColor("blue"))

        for i in range(self.page_layout.pageCount()):
            page_rect: RectF = self.page_layout.getPage(i).rect()
            page_rect.move(
                PointF(self.page_layout.xPosition() - rect.xPosition(), self.page_layout.yPosition() - rect.yPosition())
            )
            painter.drawRect(page_rect.toQRectF())

    def drawText(self, painter: QPainter, context: PaintContext):
        rect: RectF = context.rect
        cursor_position: int = context.cursor_position
        palette: QPalette = context.palette

        painter.setPen(QColor("red"))

        carriage_position: QPointF = QPointF(
            self.page_layout.xPosition() - rect.xPosition(), self.page_layout.yPosition() - rect.yPosition()
        )
        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_position: int = block.position()
            block_length: int = block.length()

            if cursor_position >= block_position and cursor_position < block_position + block_length:
                block_layout.drawCursor(painter, carriage_position, cursor_position - block_position)

            block_layout.draw(painter, carriage_position, [], rect.toQRectF())

    def resize(self, point: PointF):
        self.page_layout.setXPosition((point.xPosition() - self.page_layout.width()) / 2)

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def frameBoundingRect(self, frame: QTextFrame) -> QRectF:
        first_block: QTextBlock = frame.firstCursorPosition().block()
        last_block: QTextBlock = frame.lastCursorPosition().block()
        first_rect: QRectF = self.blockBoundingRect(first_block)
        last_rect: QRectF = self.blockBoundingRect(last_block)
        frame_rect: QRectF = first_rect.united(last_rect)
        return frame_rect

    def documentSize(self) -> QSizeF:
        root_frame: QTextFrame = self.document().rootFrame()
        root_frame_rect: QRectF = self.frameBoundingRect(root_frame)
        return root_frame_rect.size()

    def pageCount(self) -> int:
        return self.page_layout.pageCount()

    def hitTest(self, point: PointF) -> int:

        current_cursor_position = 0

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_rect: RectF = RectF.fromQRectF(block_layout.boundingRect())
            block_rect.move(self.page_layout.position())

            if block_rect.contains(point):
                for j in range(block_layout.lineCount()):
                    line: QTextLine = block_layout.lineAt(j)
                    line_rect: RectF = RectF.fromQRectF(line.rect())
                    line_rect.move(self.page_layout.position())

                    if line_rect.contains(point):
                        x_coord = point.xPosition() - self.page_layout.xPosition()
                        line_cursor_position = line.xToCursor(x_coord, QTextLine.CursorPosition.CursorBetweenCharacters)
                        current_cursor_position += line_cursor_position

                        return current_cursor_position

            current_cursor_position += block.length()

        return -1
