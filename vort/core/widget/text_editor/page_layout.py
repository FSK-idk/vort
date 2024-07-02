from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QGuiApplication

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

    def __init__(self) -> None:
        super().__init__()

        # TODO: add to config
        dpi = QGuiApplication.screens()[0].physicalDotsPerInch()

        self.__page_width: float = 210 * dpi / 25.4
        self.__page_height: float = 297.0 * dpi / 25.4
        self.__page_margin: float = 10 * dpi / 25.4
        self.__page_padding: float = 10 * dpi / 25.4
        self.__spacing: float = 10 * dpi / 25.4
        self.__page_count: int = 1  # at least one

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

    def removePage(self, count: int = 1) -> None:
        self.__page_count -= count
        self.sizeChanged.emit(PointF(self.width(), self.height()))

    def height(self) -> float:
        return self.__page_height * self.__page_count + self.__spacing * (self.__page_count - 1)

    def width(self) -> float:
        return self.__page_width

    def textWidth(self) -> float:
        return self.__page_width - 2 * (self.__page_margin + self.__page_padding)

    def textHeight(self) -> float:
        return self.__page_height - 2 * (self.__page_margin + self.__page_padding)

    def pagePosition(self, index: int) -> PointF:
        return PointF(0, (self.__page_height + self.__spacing) * (index - 1))
