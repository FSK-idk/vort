from utils import PointF, RectF

# TODO: Move in config
PAGE_WIDTH = 360
PAGE_HEIGHT = 480
PAGE_MARGIN = 20
PAGE_PADDING = 10


class PageModel:
    def __init__(
        self,
        x_position: float = 0,
        y_position: float = 0,
        width: float = 0,
        height: float = 0,
        margin: float = 0,
        padding: float = 0,
    ) -> None:
        self.__x_position: float = x_position
        self.__y_position: float = y_position
        self.__width: float = PAGE_WIDTH
        self.__height: float = PAGE_HEIGHT
        self.__margin: float = PAGE_MARGIN
        self.__padding: float = PAGE_PADDING

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

    def width(self) -> float:
        return self.__width

    def setWidth(self, width: float) -> None:
        self.__width = width

    def height(self) -> float:
        return self.__height

    def setHeight(self, height: float) -> None:
        self.__height = height

    def margin(self) -> float:
        return self.__margin

    def setMargin(self, margin: float) -> None:
        self.__margin = margin

    def padding(self) -> float:
        return self.__padding

    def setPadding(self, padding: float) -> None:
        self.__padding = padding

    def textWidth(self) -> float:
        return self.__width - (self.__margin + self.__padding) * 2

    def textHeight(self) -> float:
        return self.__height - (self.__margin + self.__padding) * 2

    def rect(self) -> RectF:
        return RectF(self.__x_position, self.__y_position, self.__width, self.__height)

    def move(self, vector: PointF) -> None:
        self.__x_position += vector.xPosition()
        self.__y_position += vector.yPosition()
