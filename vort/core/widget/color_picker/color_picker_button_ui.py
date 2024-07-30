from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QPen, QColor

from core.widget.color_picker.color_palette import ColorPalette


class ColorPickerButtonUI(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.margin = 16

        self.color_icon: QPixmap = QPixmap(self.height() - self.margin, self.height() - self.margin)

        self.setCheckable(True)
        self.setFixedWidth(self.height())

        self.color_palette: ColorPalette = ColorPalette(self)
        self.color_palette.setWindowFlags(Qt.WindowType.Popup)

    def setColorIcon(self, color: QColor) -> None:
        if color == QColor("transparent"):
            self.color_icon.fill(QColor("white"))
            painter: QPainter = QPainter(self.color_icon)
            pen: QPen = QPen(QColor("red"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(0, self.color_icon.height(), self.color_icon.height(), 0)
            painter.end()
        else:
            self.color_icon.fill(color)
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter: QPainter = QPainter(self)
        coord_x = int((self.width() - self.color_icon.width()) / 2)
        coord_y = int((self.height() - self.color_icon.height()) / 2)

        painter.drawPixmap(coord_x, coord_y, self.color_icon)

    def showPalette(self) -> None:
        button_bottom_left: QPoint = self.mapToGlobal(QPoint(0, self.height()))
        self.color_palette.move(button_bottom_left)
        self.color_palette.setVisible(True)

    def hidePalette(self) -> None:
        self.color_palette.hide()
