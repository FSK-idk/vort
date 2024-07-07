from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor


class PageLayout(QObject):
    # page layout in one column.
    # you can do two, three, etc. columns or in some way of your own,
    # if you override pageXPosition and pageYPosition methods

    # page width, page height, spacing, page_count
    layoutSizeChanged = Signal()
    # page margins, page paddings, header height, footer height
    pageLayoutSizeChanged = Signal()
    # page color, border color
    colorChanged = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.__page_width: float = 0.0
        self.__page_height: float = 0.0
        self.__page_spacing: float = 0.0

        self.__page_count: int = 1  # at least one

        self.__page_color: QColor = QColor("white")

        self.__page_top_margin: float = 0.0
        self.__page_bottom_margin: float = 0.0
        self.__page_left_margin: float = 0.0
        self.__page_right_margin: float = 0.0

        self.__page_top_padding: float = 0.0
        self.__page_bottom_padding: float = 0.0
        self.__page_left_padding: float = 0.0
        self.__page_right_padding: float = 0.0

        self.__border_width: float = 0.0
        self.__border_color: QColor = QColor("black")

        self.__header_height: float = 0.0
        self.__footer_height: float = 0.0

    def pageWidth(self) -> float:
        return self.__page_width

    def setPageWidth(self, width: float) -> None:
        self.__page_width = width
        self.layoutSizeChanged.emit()

    def pageHeight(self) -> float:
        return self.__page_height

    def setPageHeight(self, height: float) -> None:
        self.__page_height = height
        self.layoutSizeChanged.emit()

    def pageSpacing(self) -> float:
        return self.__page_spacing

    def setPageSpacing(self, spacing: float) -> None:
        self.__page_spacing = spacing
        self.layoutSizeChanged.emit()

    def pageCount(self) -> int:
        return self.__page_count

    def addPage(self, count: int = 1) -> None:
        self.__page_count += count
        self.layoutSizeChanged.emit()

    def removePage(self, count: int = 1) -> None:
        self.__page_count -= count
        self.layoutSizeChanged.emit()

    def height(self) -> float:
        return self.__page_height * self.__page_count + self.__page_spacing * (self.__page_count - 1)

    def width(self) -> float:
        return self.__page_width

    def pageXPosition(self, index: int) -> float:
        return 0.0

    def pageYPosition(self, index: int) -> float:
        return (self.__page_height + self.__page_spacing) * index

    def pageColor(self) -> QColor:
        return self.__page_color

    def setPageColor(self, color: QColor) -> None:
        self.__page_color = color
        self.colorChanged.emit()

    def pageTopMargin(self) -> float:
        return self.__page_top_margin

    def setPageTopMargin(self, margin: float) -> None:
        self.__page_top_margin = margin
        self.pageLayoutSizeChanged.emit()

    def pageBottomMargin(self) -> float:
        return self.__page_bottom_margin

    def setPageBottomMargin(self, margin: float) -> None:
        self.__page_bottom_margin = margin
        self.pageLayoutSizeChanged.emit()

    def pageLeftMargin(self) -> float:
        return self.__page_left_margin

    def setPageLeftMargin(self, margin: float) -> None:
        self.__page_left_margin = margin
        self.pageLayoutSizeChanged.emit()

    def pageRightMargin(self) -> float:
        return self.__page_right_margin

    def setPageRightMargin(self, margin: float) -> None:
        self.__page_right_margin = margin
        self.pageLayoutSizeChanged.emit()

    def pageTopPadding(self) -> float:
        return self.__page_top_padding

    def setPageTopPadding(self, padding: float) -> None:
        self.__page_top_padding = padding
        self.pageLayoutSizeChanged.emit()

    def pageBottomPadding(self) -> float:
        return self.__page_bottom_padding

    def setPageBottomPadding(self, padding: float) -> None:
        self.__page_bottom_padding = padding
        self.pageLayoutSizeChanged.emit()

    def pageLeftPadding(self) -> float:
        return self.__page_left_padding

    def setPageLeftPadding(self, padding: float) -> None:
        self.__page_left_padding = padding
        self.pageLayoutSizeChanged.emit()

    def pageRightPadding(self) -> float:
        return self.__page_right_padding

    def setPageRightPadding(self, padding: float) -> None:
        self.__page_right_padding = padding
        self.pageLayoutSizeChanged.emit()

    def borderWidth(self) -> float:
        return self.__border_width

    def setBorderWidth(self, width: float) -> None:
        self.__border_width = width

    def borderColor(self) -> QColor:
        return self.__border_color

    def setBorderColor(self, color: QColor) -> None:
        self.__border_color = color

    def headerHeight(self) -> float:
        return self.__header_height

    def setHeaderHeight(self, height: float):
        self.__header_height = height

    def footerHeight(self) -> float:
        return self.__footer_height

    def setFooterHeight(self, height: float):
        self.__footer_height = height

    def textWidth(self) -> float:
        return (
            self.__page_width
            - self.__page_left_margin
            - self.__border_width
            - self.__page_left_padding
            - self.__page_right_padding
            - self.__border_width
            - self.__page_right_margin
        )

    def textHeight(self) -> float:
        return (
            self.__page_height
            - self.__page_top_margin
            - self.__border_width
            - self.__page_top_padding
            - self.__header_height
            - self.__footer_height
            - self.__page_bottom_padding
            - self.__border_width
            - self.__page_bottom_margin
        )

    def textXPosition(self, index: int) -> float:
        return self.pageXPosition(index) + self.__page_left_margin + self.__border_width + self.__page_left_padding

    def textYPosition(self, index: int) -> float:
        return (
            self.pageYPosition(index)
            + self.__page_top_margin
            + self.__border_width
            + self.__page_top_padding
            + self.__header_height
        )

    def headerXPosition(self, index: int) -> float:
        return self.pageXPosition(index) + self.__page_left_margin + self.__border_width + self.__page_left_padding

    def headerYPosition(self, index: int) -> float:
        return self.pageYPosition(index) + self.__page_top_margin + self.__border_width + self.__page_top_padding

    def footerXPosition(self, index: int) -> float:
        return self.pageXPosition(index) + self.__page_left_margin + self.__border_width + self.__page_left_padding

    def footerYPosition(self, index: int) -> float:
        return self.textYPosition(index) + self.textHeight()
