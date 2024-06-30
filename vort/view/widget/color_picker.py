from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap, QColor, QMouseEvent
from PySide6.QtCore import QEvent, QObject, Qt, QPoint, Signal, QPointF

from utils import PointF, RectF

from view.widget.color_palette_view import ColorPaletteView


# there is a problem with hiding the popup color palette.
# the palette closes regardless of whether I pressed the button or not.
# to solve this, I use a filter to somehow affect the process of hiding the palette and checking the button.


# specifically for the color palette
class MousePressedFilter(QObject):
    mousePressed = Signal(QMouseEvent)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        # popup closes only on mouse pressed event
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressed.emit(event)
        # we reject other events, such as hiding, so we don't have to handle them inside the class
        return True


class ColorPicker(QWidget):
    colorSelected = Signal(QColor)

    def __init__(self, text: str | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        icon: QPixmap = QPixmap(16, 16)
        icon.fill(Qt.GlobalColor.black)

        self.button: QPushButton = QPushButton(text)
        self.button.setIcon(icon)
        self.button.setCheckable(True)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.color_palette: ColorPaletteView = ColorPaletteView(self)

        self.button.clicked.connect(self.onClicked)
        self.color_palette.colorSelected.connect(self.onColorSelected)

        self.mouse_pressed_filter = MousePressedFilter()
        self.color_palette.installEventFilter(self.mouse_pressed_filter)
        self.mouse_pressed_filter.mousePressed.connect(self.onMousePressed)

    def setColor(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.button.setIcon(icon)

    def onColorSelected(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.button.setIcon(icon)
        self.colorSelected.emit(color)
        self.button.setChecked(False)
        self.color_palette.hide()

    def onClicked(self, checked) -> None:
        # only if the button is checked, the other case is considered in the mouse event
        if checked:
            button_bottom_left: QPoint = self.mapToGlobal(self.button.geometry().bottomLeft())
            self.color_palette.show(button_bottom_left)

    def onMousePressed(self, event: QMouseEvent) -> None:
        # calculate rects with own classes to make sure the math is ok
        point = PointF.fromQPointF(self.color_palette.mapToGlobal(event.position()))
        button_pos = PointF.fromQPoint(self.mapToGlobal(self.button.pos()))
        palette_pos: PointF = PointF.fromQPoint(self.mapToGlobal(self.button.geometry().bottomLeft()))

        button_rect_w: float = self.button.width()
        button_rect_h: float = self.button.height()
        button_rect: RectF = RectF(button_pos.xPosition(), button_pos.yPosition(), button_rect_w, button_rect_h)

        palette_rect_w: float = self.color_palette.width()
        palette_rect_h: float = self.color_palette.height()
        palette_rect: RectF = RectF(palette_pos.xPosition(), palette_pos.yPosition(), palette_rect_w, palette_rect_h)

        if button_rect.contains(point) and not palette_rect.contains(point):
            self.button.setChecked(True)
            self.color_palette.hide()
        if not button_rect.contains(point) and palette_rect.contains(point):
            return
        if not button_rect.contains(point) and not palette_rect.contains(point):
            self.button.setChecked(False)
            self.color_palette.hide()
