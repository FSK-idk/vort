from typing import Self
from PySide6.QtCore import QPointF, QPoint


class PointF:
    def __init__(
        self,
        x_position: float = 0,
        y_position: float = 0,
    ) -> None:
        self.__x_position: float = x_position
        self.__y_position: float = y_position

    @classmethod
    def fromQPointF(cls, point: QPointF) -> Self:
        return cls(point.x(), point.y())

    @classmethod
    def fromQPoint(cls, point: QPoint) -> Self:
        return cls(point.x(), point.y())

    def toQPointF(self) -> QPointF:
        return QPointF(self.__x_position, self.__y_position)

    def toQPoint(self) -> QPoint:
        return QPoint(int(self.__x_position), int(self.__y_position))

    def xPosition(self) -> float:
        return self.__x_position

    def setXPosition(self, x_position: float) -> None:
        self.__x_position = x_position

    def yPosition(self) -> float:
        return self.__y_position

    def move(self, vector: Self) -> None:
        self.__x_position += vector.xPosition()
        self.__y_position += vector.yPosition()
