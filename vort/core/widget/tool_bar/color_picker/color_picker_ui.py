from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QToolButton
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QPen, QColor

from core.widget.tool_bar.color_picker.color_palette import ColorPalette


class ColorPickerUI(QToolButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.color_icon: QPixmap = QPixmap(16, 16)
        self.color_icon.fill(Qt.GlobalColor.blue)

        self.icon: QPixmap | None = None

        self.setCheckable(True)
        self.setFixedWidth(32)

        self.color_palette: ColorPalette = ColorPalette(self)
        self.color_palette.setWindowFlags(Qt.WindowType.Popup)

    def setColorIcon(self, color: QColor) -> None:
        if color == QColor("transparent"):
            self.color_icon.fill(QColor("white"))
            painter: QPainter = QPainter(self.color_icon)
            pen: QPen = QPen(QColor("red"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(0, 16, 16, 0)
            painter.end()

        else:
            self.color_icon.fill(color)
        self.repaint()

    def setIcon(self, icon: QPixmap) -> None:
        self.icon = icon
        self.setFixedWidth(56)
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter: QPainter = QPainter(self)
        coord_y = int((self.height() - 16) / 2)

        painter.drawPixmap(8, coord_y, self.color_icon)
        if self.icon is not None:
            painter.drawPixmap(32, coord_y, self.icon)

    def showPalette(self) -> None:
        button_bottom_left: QPoint = self.mapToGlobal(QPoint(0, self.height()))
        self.color_palette.move(button_bottom_left)
        self.color_palette.setVisible(True)

    def hidePalette(self) -> None:
        self.color_palette.hide()
