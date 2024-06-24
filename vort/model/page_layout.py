from model.page import Page
from utils import PointF


class PageLayout:
    """
    By default all pages are centered
    """

    def __init__(
        self,
        x_position: float = 0,
        y_position: float = 0,
        pages: list[Page] = [],
        spacing: float = 0,
    ) -> None:
        self.__x_position: float = x_position
        self.__y_position: float = y_position
        self.__pages: list[Page] = pages
        self.__spacing: float = spacing

        self.__width: float = 0
        if self.__pages:
            self.__width = max([page.width() for page in self.__pages])

        # update page x positions
        for page in self.__pages:
            page_x_position = (self.__width - page.width()) / 2
            page.setXPosition(page_x_position)

        # update page y positions and set height
        self.__height = 0

        current_y_position = 0
        for page in self.__pages:
            page.setYPosition(current_y_position)
            self.__height += page.height()
            current_y_position += self.__spacing

        if len(self.__pages) > 1:
            self.__height += self.__spacing * (len(self.__pages) - 1)

    def xPosition(self) -> float:
        return self.__x_position

    def setXPosition(self, x_position) -> None:
        self.__x_position = x_position

    def yPosition(self) -> float:
        return self.__y_position

    def setYPosition(self, y_position) -> None:
        self.__y_position = y_position

    def position(self) -> PointF:
        return PointF(self.__x_position, self.__y_position)

    def setPosition(self, position: PointF) -> None:
        self.__x_position = position.xPosition()
        self.__y_position = position.yPosition()

    def pageCount(self) -> int:
        return len(self.__pages)

    def getPage(self, index) -> Page:
        """
        index in range(0, len(self.__pages))
        """
        return self.__pages[index]

    def insertPage(self, index: int, inserted_page: Page) -> None:
        """
        index in range(0, len(self.__pages) + 1)
        """
        self.__pages.insert(index, inserted_page)

        # update width
        if inserted_page.width() > self.__width:
            self.__width = inserted_page.width()
            # update page x positions
            for page in self.__pages:
                page_x_position = (self.__width - page.width()) / 2
                page.setXPosition(page_x_position)
        else:
            # update page x position
            page_x_position = (self.__width - inserted_page.width()) / 2
            inserted_page.setXPosition(page_x_position)

        # update page y positions
        if index - 1 >= 0:
            current_y_position = self.__pages[index - 1].yPosition() + self.__pages[index - 1].height() + self.__spacing
            for i in range(index, len(self.__pages)):
                self.__pages[i].setYPosition(current_y_position)
                current_y_position += self.__spacing

        # update height
        if len(self.__pages) > 1:
            self.__height += self.__spacing
        self.__height += inserted_page.height()

    def addPage(self) -> None:
        self.insertPage(len(self.__pages), Page())

    def deletePage(self, index: int) -> None:
        """
        index in range(0, len(self.__pages))
        """
        deleted_page_height = self.__pages[index].height()
        del self.__pages[index]

        self.__width = 0
        if self.__pages:
            self.__width = max([page.width() for page in self.__pages])

        # update page x positions
        for page in self.__pages:
            page_x_position = (self.__width - page.width()) / 2
            page.setXPosition(page_x_position)

        # update page y positions
        if index > 0:
            current_y_position = self.__pages[index - 1].yPosition() + self.__pages[index - 1].height() + self.__spacing
        else:
            current_y_position = 0

        for i in range(index, len(self.__pages)):
            self.__pages[i].setYPosition(current_y_position)
            current_y_position += self.__spacing

        # update height
        if len(self.__pages) > 0:
            self.__height -= self.__spacing
        self.__height -= deleted_page_height

    def deleteLastPage(self) -> None:
        self.deletePage(len(self.__pages) - 1)

    def spacing(self) -> float:
        return self.__spacing

    def setSpacing(self, spacing: float) -> None:
        self.__spacing = spacing

        # update page y positions and height
        self.__height = 0

        current_y_position = 0
        for page in self.__pages:
            page.setYPosition(current_y_position)
            self.__height += page.height()
            current_y_position += self.__spacing

        if len(self.__pages) > 1:
            self.__height += self.__spacing * (len(self.__pages) - 1)

    def width(self) -> float:
        return self.__width

    def height(self) -> float:
        return self.__height

    def move(self, x: float, y: float) -> None:
        self.__x_position += x
        self.__y_position += y
