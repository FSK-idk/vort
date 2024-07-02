from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QPixmap, QColor


class ColorButton(QPushButton):
    colorClicked = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__color: QColor = QColor()
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(self.__color)
        self.setIcon(icon)
        self.setFixedSize(16, 16)
        self.clicked.connect(self.onClicked)

    def color(self) -> QColor:
        return self.__color

    def setColor(self, color: QColor) -> None:
        self.__color = color
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(self.__color)
        self.setIcon(icon)

    @Slot()
    def onClicked(self) -> None:
        self.colorClicked.emit(self.__color)