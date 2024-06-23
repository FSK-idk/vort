from PySide6.QtGui import QPainter, QPaintEvent, QColor, QResizeEvent
from PySide6.QtCore import QPointF, QRectF, Qt, QPoint

from model.page import Page


class PageLayout:
    def __init__(self) -> None:
        self.__pages: list[Page] = []
        
        self.__x_position: float = 0
        self.__y_position: float = 0
        
        self.__page_width: float = 0
        self.__page_height: float = 0
        self.__spacing: float = 0

    def width(self) -> float:
        return self.__page_width

    def height(self) -> float:
        return self.__page_height * len(self.__pages) + self.__spacing * (len(self.__pages) - 1)

    def position(self) -> QPointF:
        return QPointF(self.__x_position, self.__y_position)

    def xPosition(self) -> float:
        return self.__x_position
    
    def setXPosition(self, x_position) -> None:
        self.__x_position = x_position
    
    def yPosition(self) -> float:
        return self.__y_position

    def setYPosition(self, y_position) -> None:
        self.__y_position = y_position

    def move(self, x: float, y: float) -> None:
        self.__x_position += x
        self.__y_position += y

    def setPageWidth(self, page_width: float) -> None:
        self.__page_width = page_width
        for page in self.__pages:
            page.setWidth(self.__page_width)

    def setPageHeight(self, page_height: float) -> None:
        self.__page_height = page_height
        current_height = 0
        for page in self.__pages:
            page.setHeight(self.__page_height)
            current_height += self.__page_height
            current_height += self.__spacing

    def setSpacing(self, spacing: float) -> None:
        self.__spacing = spacing

    def append(self, page: Page) -> None:
        page.setWidth(self.__page_width)
        page.setHeight(self.__page_height)

        if self.__pages:
            last_page = self.__pages[-1]
            page.setYPosition(last_page.yPosition() + last_page.height() + self.__spacing)

        self.__pages.append(page)

    def paint(self, painter: QPainter, event: QPaintEvent) -> None:
        painter.setBrush(QColor("white"))

        for page in self.__pages:

            rect_x = page.xPosition() + self.__x_position - event.rect().x()
            rect_y = page.yPosition() + self.__y_position - event.rect().y()
            rect_w = page.width()
            rect_h = page.height()

            rect: QRectF = QRectF(rect_x, rect_y, rect_w, rect_h)

            painter.drawRect(rect)

    def onResizeEvent(self, event: QResizeEvent) -> None:
        self.__x_position = (event.size().width() - self.__page_width) / 2