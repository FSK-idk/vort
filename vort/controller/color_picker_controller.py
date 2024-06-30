from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QColor, QMouseEvent
from PySide6.QtCore import QEvent, QObject, Signal

from utils import PointF, RectF

from view.widget.color_picker_view import ColorPickerView


# there is a problem with hiding the popup color palette.
# the palette closes regardless of whether I pressed the button or not.
# therefore, when you click the button to close, the palette will not close
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


class ColorPickerController(QWidget):
    colorSelected = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: ColorPickerView = ColorPickerView(parent)

        self.ui.button.clicked.connect(self.onClicked)
        self.ui.color_palette.colorSelected.connect(self.onColorSelected)

        self.mouse_pressed_filter = MousePressedFilter()
        self.ui.color_palette.installEventFilter(self.mouse_pressed_filter)
        self.mouse_pressed_filter.mousePressed.connect(self.onMousePressed)

    def setText(self, text: str) -> None:
        self.ui.button.setText(text)

    def setColor(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.ui.button.setIcon(icon)

    def onColorSelected(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.ui.button.setIcon(icon)
        self.ui.button.setChecked(False)
        self.ui.color_palette.hide()
        self.colorSelected.emit(color)

    def onClicked(self, checked) -> None:
        # only if the button is checked, the other case is considered in the mouse event
        if checked:
            self.ui.showPalette()

    def onMousePressed(self, event: QMouseEvent) -> None:
        # calculate rects with own classes to make sure the math is ok
        point: PointF = PointF.fromQPointF(self.ui.color_palette.mapToGlobal(event.position()))
        button_pos: PointF = PointF.fromQPoint(self.ui.mapToGlobal(self.ui.button.pos()))
        palette_pos: PointF = PointF.fromQPoint(self.ui.mapToGlobal(self.ui.button.geometry().bottomLeft()))

        button_rect_w: float = self.ui.button.width()
        button_rect_h: float = self.ui.button.height()
        button_rect: RectF = RectF(button_pos.xPosition(), button_pos.yPosition(), button_rect_w, button_rect_h)

        palette_rect_w: float = self.ui.color_palette.width()
        palette_rect_h: float = self.ui.color_palette.height()
        palette_rect: RectF = RectF(palette_pos.xPosition(), palette_pos.yPosition(), palette_rect_w, palette_rect_h)

        if not palette_rect.contains(point):
            if button_rect.contains(point):
                self.ui.button.setChecked(True)
            else:
                self.ui.button.setChecked(False)
            self.ui.color_palette.hide()
