from PySide6.QtCore import QObject, Signal, Qt, QPointF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide6.QtGui import QGuiApplication, QFont, QColor, QTextCursor, QTextCharFormat, QTextItem, QTextBlock

from util import PointF


class Page:
    def __init__(
        self,
        width: float = 0,
        height: float = 0,
        margin: float = 0,
        padding: float = 0,
    ) -> None:
        self.width: float = width
        self.height: float = height
        self.margin: float = margin
        self.padding: float = padding


class PageLayout(QObject):
    sizeChanged = Signal(PointF)
    pageCountChanged = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        # TODO: add to config
        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        self.__page_width: float = 21 * dpi / 2.54
        self.__page_height: float = 29.7 * dpi / 2.54
        self.__page_margin: float = 1 * dpi / 2.54
        self.__page_padding: float = 1 * dpi / 2.54
        self.__spacing: float = 1 * dpi / 2.54
        self.__page_count: int = 1  # at least one

        self.__footer_height: float = 1 * dpi / 2.54

    def pageWidth(self) -> float:
        return self.__page_width

    def setPageWidth(self, page_width) -> None:
        self.__page_width = page_width

    def pageHeight(self) -> float:
        return self.__page_height

    def setPageHeight(self, page_height) -> None:
        self.__page_width = page_height

    def pageMargin(self) -> float:
        return self.__page_margin

    def setPageMargin(self, page_margin) -> None:
        self.__page_margin = page_margin

    def pagePadding(self) -> float:
        return self.__page_padding

    def setPagePadding(self, page_padding) -> None:
        self.__page_padding = page_padding

    def spacing(self) -> float:
        return self.__spacing

    def setSpacing(self, spacing) -> None:
        self.__spacing = spacing

    def pageCount(self) -> int:
        return self.__page_count

    def addPage(self, count: int = 1) -> None:
        self.__page_count += count
        self.sizeChanged.emit(PointF(self.width(), self.height()))

        self.pageCountChanged.emit(self.__page_count)

    def removePage(self, count: int = 1) -> None:
        self.__page_count -= count
        self.sizeChanged.emit(PointF(self.width(), self.height()))

        self.pageCountChanged.emit(self.__page_count)

    def height(self) -> float:
        return self.__page_height * self.__page_count + self.__spacing * (self.__page_count - 1)

    def width(self) -> float:
        return self.__page_width

    def footerHeight(self) -> float:
        return self.__footer_height

    def setFooterHeight(self, height: float):
        self.__footer_height = height

    def pagePosition(self, index: int) -> PointF:
        return PointF(0, (self.__page_height + self.__spacing) * (index - 1))

    def textXPosition(self) -> float:
        return self.__page_margin + self.__page_padding

    def textYPosition(self) -> float:
        return self.__page_margin + self.__page_padding

    def textWidth(self) -> float:
        return self.__page_width - (self.__page_margin + self.__page_padding) * 2

    def textHeight(self) -> float:
        return self.__page_height - (self.__page_margin + self.__page_padding) * 2 - self.__footer_height
