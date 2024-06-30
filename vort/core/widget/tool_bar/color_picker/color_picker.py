from PySide6.QtCore import QEvent, QObject, Signal, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QColor, QMouseEvent

from util import PointF, RectF

from core.widget.tool_bar.color_picker.color_picker_ui import ColorPickerUI


# there is a problem with hiding the popup color palette.
# the palette closes regardless of whether you pressed the button or not.
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


class ColorPicker(QWidget):
    colorChanged = Signal(QColor)
    closed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: ColorPickerUI = ColorPickerUI(parent)

        self.ui.button.clicked.connect(self.onClicked)
        self.ui.color_palette.colorClicked.connect(self.onColorSelected)

        self.mouse_pressed_filter = MousePressedFilter()
        self.mouse_pressed_filter.mousePressed.connect(self.onMousePressed)
        self.ui.color_palette.installEventFilter(self.mouse_pressed_filter)

    def setText(self, text: str) -> None:
        self.ui.button.setText(text)

    def setColor(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.ui.button.setIcon(icon)

    @Slot(QColor)
    def onColorSelected(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.ui.button.setIcon(icon)
        self.ui.button.setChecked(False)
        self.ui.hidePalette()
        self.colorChanged.emit(color)
        self.closed.emit()

    @Slot(bool)
    def onClicked(self, checked) -> None:
        # only if the button is checked, the other case is considered in the mouse event
        if checked:
            self.ui.showPalette()

    @Slot(QMouseEvent)
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
            self.ui.hidePalette()
            self.closed.emit()
