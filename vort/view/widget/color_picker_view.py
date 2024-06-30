from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint

from view.widget.color_palette_view import ColorPaletteView


class ColorPickerView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        icon: QPixmap = QPixmap(16, 16)
        icon.fill(Qt.GlobalColor.black)

        self.button: QPushButton = QPushButton(self)
        self.button.setIcon(icon)
        self.button.setCheckable(True)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.color_palette: ColorPaletteView = ColorPaletteView(self)
        self.color_palette.setWindowFlags(Qt.WindowType.Popup)

    def showPalette(self) -> None:
        button_bottom_left: QPoint = self.mapToGlobal(self.button.geometry().bottomLeft())
        self.color_palette.move(button_bottom_left)
        self.color_palette.setVisible(True)
