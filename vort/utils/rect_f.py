from typing import Self
from PySide6.QtCore import QRectF, QRect
from utils.point_f import PointF


class RectF:
    def __init__(
        self,
        x_position: float = 0,
        y_position: float = 0,
        width: float = 0,
        height: float = 0,
    ) -> None:
        self.__x_position: float = x_position
        self.__y_position: float = y_position
        self.__width: float = width
        self.__height: float = height

    @classmethod
    def fromQRectF(cls, rect: QRectF) -> Self:
        return cls(rect.x(), rect.y(), rect.width(), rect.height())

    @classmethod
    def fromQRect(cls, rect: QRect) -> Self:
        return cls(rect.x(), rect.y(), rect.width(), rect.height())

    def toQRectF(self) -> QRectF:
        return QRectF(self.__x_position, self.__y_position, self.__width, self.__height)

    def toQRect(self) -> QRect:
        return QRect(int(self.__x_position), int(self.__y_position), int(self.__width), int(self.__height))

    def xPosition(self) -> float:
        return self.__x_position

    def setXPosition(self, x_position: float) -> None:
        self.__x_position = x_position

    def yPosition(self) -> float:
        return self.__y_position

    def setYPosition(self, y_position: float) -> None:
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

    def move(self, vector: PointF) -> None:
        self.__x_position += vector.xPosition()
        self.__y_position += vector.yPosition()
