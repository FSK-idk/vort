from PySide6.QtCore import QPointF, QRectF

class Page:
    def __init__(self) -> None:
        self.__x_position: float = 0
        self.__y_position: float = 0
        self.__width: float = 0
        self.__height: float = 0

    def width(self) -> float:
        return self.__width

    def setWidth(self, width: float) -> None:
        self.__width = width

    def height(self) -> float:
        return self.__height
    
    def setHeight(self, height: float) -> None:
        self.__height = height

    def position(self) -> QPointF:
        return QPointF(self.__x_position, self.__y_position)

    def setPosition(self, position: QPointF) -> None:
        self.__x_position = position.x()
        self.__y_position = position.y()

    def xPosition(self) -> float:
        return self.__x_position
    
    def setXPosition(self, x_position) -> None:
        self.__x_position = x_position
    
    def yPosition(self) -> float:
        return self.__y_position

    def setYPosition(self, y_position) -> None:
        self.__y_position = y_position

    def rect(self) -> QRectF:
        return QRectF(self.__x_position, self.__y_position, self.__width, self.__height)

    def move(self, x: float, y: float) -> None:
        self.__x_position += x
        self.__y_position += y