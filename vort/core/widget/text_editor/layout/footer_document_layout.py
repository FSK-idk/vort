from enum import Enum

from PySide6.QtCore import QPointF, Signal, QRect, QRectF, Qt
from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QTextDocument,
    QTextBlock,
    QTextLayout,
    QTextLine,
    QPainter,
    QTextCursor,
    QTextCharFormat,
    QColor,
    QTextBlockFormat,
    QGuiApplication,
    QTextInlineObject,
    QTextFormat,
    QTextFragment,
    QTextImageFormat,
    QImage,
    QFont,
)

from util import PointF, RectF

from core.widget.text_editor.layout.page_layout import PageLayout


class FooterPaintContext:
    def __init__(
        self,
        painter: QPainter = QPainter(),
        viewport_rect: RectF = RectF(),
    ) -> None:
        self.painter = painter
        self.viewport_rect: RectF = viewport_rect


class FooterDocumentLayout(QAbstractTextDocumentLayout):
    sizeChanged = Signal(PointF)

    def __init__(self, footer_document: QTextDocument, page_layout: PageLayout) -> None:
        super().__init__(footer_document)

        self.__page_layout: PageLayout = page_layout
        self.__text_cursor: QTextCursor = QTextCursor(footer_document)

        self.__char_format: QTextCharFormat = QTextCharFormat()
        self.__char_format.setFontFamily(QFont().family())
        self.__char_format.setFontPointSize(16)
        self.__char_format.setForeground(QColor("black"))
        self.__char_format.setBackground(QColor("white"))

        self.__alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter

        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(self.__char_format)

        self.addPage(self.__page_layout.pageCount())

        self.__page_layout.pageCountChanged.connect(self.onPageCountChange)

    def onPageCountChange(self, count: int) -> None:
        diff = self.document().blockCount() + 1 - count
        if diff > 0:
            self.addPage(diff)
        else:
            self.removePage(-diff)

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.__alignment = alignment
        self.documentChanged(0, 0, 0)

    def setFontFamily(self, family: str) -> None:
        self.__char_format.setFontFamily(family)
        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(self.__char_format)
        self.documentChanged(0, 0, 0)

    def setFontSize(self, size: int) -> None:
        self.__char_format.setFontPointSize(size)
        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(self.__char_format)
        self.documentChanged(0, 0, 0)

    def setForegroundColor(self, color: QColor) -> None:
        self.__char_format.setForeground(color)
        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(self.__char_format)
        self.documentChanged(0, 0, 0)

    def setBackgroundColor(self, color: QColor) -> None:
        self.__char_format.setBackground(color)
        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(self.__char_format)
        self.documentChanged(0, 0, 0)

    def addPage(self, count: int = 1) -> None:
        for i in range(count):
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.__text_cursor.setCharFormat(self.__char_format)
            self.__text_cursor.setBlockCharFormat(self.__char_format)
            self.__text_cursor.insertText(str(self.document().blockCount()))
            self.__text_cursor.insertBlock()
        self.documentChanged(0, 0, 0)

    def removePage(self, count: int = 1) -> None:
        for i in reversed(range(count)):
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)
            self.__text_cursor.removeSelectedText()
        self.documentChanged(0, 0, 0)

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        root_x = self.__page_layout.textXPosition()
        root_y = self.__page_layout.textYPosition() + self.__page_layout.textHeight()
        step_y = self.__page_layout.pageHeight() + self.__page_layout.spacing()

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()

            while line.isValid():
                line.setLineWidth(self.__page_layout.textWidth())
                line_rect: QRectF = line.naturalTextRect()

                line_x: float = root_x
                line_y: float = root_y

                if self.__alignment == Qt.AlignmentFlag.AlignCenter:
                    line_x += (self.__page_layout.textWidth() - line_rect.width()) / 2
                    line_y += (self.__page_layout.footerHeight() - line_rect.height()) / 2

                elif self.__alignment == Qt.AlignmentFlag.AlignLeft:
                    line_x += 0
                    line_y += (self.__page_layout.footerHeight() - line_rect.height()) / 2

                elif self.__alignment == Qt.AlignmentFlag.AlignRight:
                    line_x += self.__page_layout.textWidth() - line_rect.width()
                    line_y += (self.__page_layout.footerHeight() - line_rect.height()) / 2

                line.setLineWidth(line_rect.width())
                line.setPosition(QPointF(line_x, line_y))

                line = block_layout.createLine()

            root_y += step_y

            block_layout.endLayout()

        self.update.emit()

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def paint(self, context: FooterPaintContext):
        painter: QPainter = context.painter
        viewport_rect: RectF = context.viewport_rect

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_layout.draw(painter, QPointF(0, 0), [], viewport_rect.toQRectF())
