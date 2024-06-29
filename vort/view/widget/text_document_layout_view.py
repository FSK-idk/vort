from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QTextDocument,
    QTextBlock,
    QTextLayout,
    QTextLine,
    QPainter,
    QTextCursor,
    QTextCharFormat,
    QPalette,
    QPen,
    QBrush,
    QColor,
)
from PySide6.QtCore import QPointF, Signal, QEvent

from utils import PointF, RectF

from model.page_layout_model import PageLayoutModel
from model.page_model import PageModel


class Selection:
    def __init__(
        self,
        cursor: QTextCursor = QTextCursor(),
        format: QTextCharFormat = QTextCharFormat(),
    ) -> None:
        self.cursor: QTextCursor = cursor
        self.format: QTextCharFormat = format


class PaintContext:
    def __init__(
        self,
        rect: RectF = RectF(),
        cursor_position: int = -1,
        palette: QPalette = QPalette(),
        selections: list[Selection] = [],
    ) -> None:
        self.rect: RectF = rect
        self.cursor_position: int = cursor_position
        self.palette: QPalette = palette
        self.selections: list[Selection] = selections


class TextDocumentLayoutView(QAbstractTextDocumentLayout):
    pageCountChanged = Signal(int)
    characterCountChanged = Signal(int)

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)

        # model

        self.__character_count: int = 0

        # TODO: add in config
        page_spacing: float = 10

        self.page_layout: PageLayoutModel = PageLayoutModel(spacing=page_spacing)
        # has at least one page
        self.page_layout.addPage()

    def pageCount(self) -> int:
        return self.page_layout.pageCount()

    def characterCount(self) -> int:
        return self.__character_count

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        old_page_count: int = self.page_layout.pageCount()

        character_count: int = 0

        current_page_index: int = 0
        current_page: PageModel = self.page_layout.getPage(current_page_index)

        current_page_width: float = current_page.textWidth()
        current_page_height: float = current_page.textHeight()

        current_x_position: float = current_page.xPosition() + current_page.margin() + current_page.padding()
        current_y_position: float = current_page.yPosition() + current_page.margin() + current_page.padding()

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

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

                character_count += line.textLength()

                line = block_layout.createLine()

            block_layout.endLayout()

        while self.page_layout.pageCount() > current_page_index + 1:
            self.page_layout.deleteLastPage()

        self.update.emit()

        if old_page_count != self.page_layout.pageCount():
            self.pageCountChanged.emit(self.page_layout.pageCount())

        if self.__character_count != character_count:
            self.__character_count = character_count
            self.characterCountChanged.emit(self.__character_count)

    def draw(self, painter: QPainter, context: PaintContext):
        self.drawClear(painter, context)
        self.drawPage(painter, context)
        self.drawText(painter, context)

        self.update.emit()

    def drawClear(self, painter: QPainter, context: PaintContext) -> None:
        rect: RectF = context.rect
        palette: QPalette = QPalette()
        rect.move(PointF(-1, -1))

        old_brush: QBrush = painter.brush()
        old_pen: QPen = painter.pen()

        painter.setBrush(palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Base))
        painter.setPen(palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Base))

        painter.drawRect(context.rect.toQRectF())

        painter.setBrush(old_brush)
        painter.setPen(old_pen)

    def drawPage(self, painter: QPainter, context: PaintContext) -> None:
        rect: RectF = context.rect
        palette: QPalette = context.palette

        old_brush: QBrush = painter.brush()
        old_pen: QPen = painter.pen()

        painter.setBrush(palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Base))
        painter.setPen(palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Base))

        for i in range(self.page_layout.pageCount()):
            page_rect: RectF = self.page_layout.getPage(i).rect()
            page_rect.move(
                PointF(self.page_layout.xPosition() - rect.xPosition(), self.page_layout.yPosition() - rect.yPosition())
            )
            painter.drawRect(page_rect.toQRectF())

        painter.setBrush(old_brush)
        painter.setPen(old_pen)

    def drawText(self, painter: QPainter, context: PaintContext):
        rect: RectF = context.rect
        cursor_position: int = context.cursor_position
        palette: QPalette = context.palette
        selections: list[Selection] = context.selections

        carriage_position: QPointF = QPointF(
            self.page_layout.xPosition() - rect.xPosition(), self.page_layout.yPosition() - rect.yPosition()
        )
        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_position: int = block.position()
            block_length: int = block.length()

            format_ranges: list[QTextLayout.FormatRange] = []

            for selection in selections:
                selection_start: int = selection.cursor.selectionStart() - block_position
                selection_end: int = selection.cursor.selectionEnd() - block_position
                if selection_start < block_length and selection_end > 0:
                    format_range: QTextLayout.FormatRange = QTextLayout.FormatRange()
                    format_range.start = selection_start  # type: ignore
                    format_range.length = selection_end - selection_start  # type: ignore
                    format_range.format = selection.format  # type: ignore
                    format_ranges.append(format_range)

            if cursor_position >= block_position and cursor_position < block_position + block_length and not selections:
                block_layout.drawCursor(painter, carriage_position, cursor_position - block_position)

            block_layout.draw(painter, carriage_position, format_ranges, painter.clipBoundingRect())

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

    def resizePageLayout(self, point: PointF):
        self.page_layout.setXPosition((point.xPosition() - self.page_layout.width()) / 2)
