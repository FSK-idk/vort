from PySide6.QtCore import QPointF, QRectF, Qt, Slot
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
)

from util import RectF

from core.text_editor.layout.page_layout import PageLayout


class HeaderPaintContext:
    def __init__(self) -> None:
        self.painter: QPainter = QPainter()
        self.rect: RectF = RectF()


class HeaderDocumentLayout(QAbstractTextDocumentLayout):
    def __init__(self, header_document: QTextDocument, page_layout: PageLayout) -> None:
        super().__init__(header_document)

        self.__page_layout: PageLayout = page_layout

        self.__text_cursor: QTextCursor = QTextCursor(header_document)

        self.__alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter

        self.__font_family: str = ""
        self.__font_size: int = 1

        self.__text_background_color: QColor = QColor("black")
        self.__text_foreground_color: QColor = QColor("black")

        self.__is_turned_for_first_page: bool = False

        self.__is_pagination_turned: bool = False
        self.__pagination_starting_number: int = 0

        self.__is_text_turned: bool = False
        self.__text: str = ""

        self.addPage(self.__page_layout.pageCount())

        self.__page_layout.changed.connect(self.onPageLayoutChanged)

    def alignment(self) -> Qt.AlignmentFlag:
        return self.__alignment

    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.__alignment = alignment
        self.documentChanged(0, 0, 0)

    def fontFamily(self) -> str:
        return self.__font_family

    def setFontFamily(self, family: str) -> None:
        self.__font_family = family
        self.updateFormat()

    def fontSize(self) -> int:
        return self.__font_size

    def setFontSize(self, size: int) -> None:
        self.__font_size = size
        self.updateFormat()

    def textBackgroundColor(self) -> QColor:
        return self.__text_background_color

    def setTextBackgroundColor(self, color: QColor) -> None:
        self.__text_background_color = color
        self.updateFormat()

    def textForegroundColor(self) -> QColor:
        return self.__text_foreground_color

    def setTextForegroundColor(self, color: QColor) -> None:
        self.__text_foreground_color = color
        self.updateFormat()

    def isTurnedForFirstPage(self) -> bool:
        return self.__is_turned_for_first_page

    def turnForFirstPage(self, is_turned):
        self.__is_turned_for_first_page = is_turned
        self.updateHeader()

    def isPaginationTurned(self) -> bool:
        return self.__is_pagination_turned

    def turnPagination(self, is_turned: bool) -> None:
        self.__is_pagination_turned = is_turned
        if self.__is_pagination_turned:
            self.__is_text_turned = False
        self.updateHeader()

    def paginationStartingNumber(self) -> int:
        return self.__pagination_starting_number

    def setPaginationStartingNumber(self, number: int) -> None:
        self.__pagination_starting_number = number
        self.updateHeader()

    def isTextTurned(self) -> bool:
        return self.__is_text_turned

    def turnText(self, is_turned: bool) -> None:
        self.__is_text_turned = is_turned
        if self.__is_text_turned:
            self.__is_pagination_turned = False
        self.updateHeader()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        self.updateHeader()

    def addPage(self, count: int = 1) -> None:
        for i in range(count):
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.__text_cursor.insertBlock()

        self.updateHeader()

    def removePage(self, count: int = 1) -> None:
        for i in range(count):
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.KeepAnchor)
            self.__text_cursor.deleteChar()

        self.updateHeader()

    def updateFormat(self) -> None:
        __char_format: QTextCharFormat = QTextCharFormat()
        __char_format.setFontFamilies([self.__font_family])
        __char_format.setFontPointSize(self.__font_size)
        __char_format.setBackground(self.__text_background_color)
        __char_format.setForeground(self.__text_foreground_color)

        self.__text_cursor.select(QTextCursor.SelectionType.Document)
        self.__text_cursor.setCharFormat(__char_format)
        self.__text_cursor.setBlockCharFormat(__char_format)

    def updateHeader(self) -> None:
        for i in range(self.document().blockCount() - 1):
            block = self.document().findBlockByNumber(i)

            self.__text_cursor.setPosition(block.position())
            self.__text_cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

            if i == 0 and not self.__is_turned_for_first_page:
                self.__text_cursor.insertText("")

            elif self.__is_pagination_turned:
                self.__text_cursor.insertText(str(self.__pagination_starting_number + i))

            elif self.__is_text_turned:
                self.__text_cursor.insertText(self.__text)

            else:
                self.__text_cursor.insertText("")
        self.updateFormat()

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        for i in range(self.document().blockCount() - 1):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()

            while line.isValid():
                line.setLineWidth(self.__page_layout.textWidth())
                line_rect: QRectF = line.naturalTextRect()

                line_x: float = self.__page_layout.headerXPosition(i)
                line_y: float = self.__page_layout.headerYPosition(i)

                # change x position
                if Qt.AlignmentFlag.AlignLeft in self.__alignment:
                    line_x += 0

                elif Qt.AlignmentFlag.AlignHCenter in self.__alignment:
                    line_x += (self.__page_layout.textWidth() - line_rect.width()) / 2

                elif Qt.AlignmentFlag.AlignRight in self.__alignment:
                    line_x += self.__page_layout.textWidth() - line_rect.width()

                # change y position
                if Qt.AlignmentFlag.AlignTop in self.__alignment:
                    line_y += 0

                elif Qt.AlignmentFlag.AlignVCenter in self.__alignment:
                    line_y += (self.__page_layout.headerHeight() - line_rect.height()) / 2

                elif Qt.AlignmentFlag.AlignBottom in self.__alignment:
                    line_y += self.__page_layout.headerHeight() - line_rect.height()

                line.setLineWidth(line_rect.width())
                line.setPosition(QPointF(line_x, line_y))

                line = block_layout.createLine()

            block_layout.endLayout()

        self.update.emit()

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def paint(self, context: HeaderPaintContext):
        painter: QPainter = context.painter
        rect: RectF = context.rect

        for i in range(self.document().blockCount() - 1):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_layout.draw(painter, QPointF(0, 0), [], rect.toQRectF())

    @Slot()
    def onPageLayoutChanged(self) -> None:
        difference = self.__page_layout.pageCount() - (self.document().blockCount() - 1)
        if difference > 0:
            self.addPage(difference)
        elif difference < 0:
            self.removePage(-difference)
        else:
            self.documentChanged(0, 0, 0)
