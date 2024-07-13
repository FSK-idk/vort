from PySide6.QtCore import QEvent, QObject, Signal, Slot, QPoint, QRectF, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QMouseEvent

from core.widget.color_picker.color_picker_tool_ui import ColorPickerToolUI


# there is a problem with hiding the popup color palette.
# the palette closes regardless of whether you pressed the button or not.
# therefore, when you click the button to close, the palette will not close
# to solve this, I use a filter to somehow affect the process of hiding the palette and checking the button.


# specifically for the color palette
class ColorPickerToolFilter(QObject):
    mousePressed = Signal(QMouseEvent)
    mouseReleased = Signal(QMouseEvent)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        # popup closes only on mouse event, we do it ourselves
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressed.emit(event)
            return True
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleased.emit(event)
            return True
        # we reject other events, they may interfere with us
        return True


class ColorPickerTool(QWidget):
    colorChanged: Signal = Signal(QColor)
    closed: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: ColorPickerToolUI = ColorPickerToolUI(parent)
        self.__color: QColor = QColor()

        # self.ui.button.clicked.connect(self.onClicked)
        self.ui.clicked.connect(self.onClicked)
        self.ui.color_palette.colorClicked.connect(self.onColorSelected)

        self.mouse_filter: ColorPickerToolFilter = ColorPickerToolFilter()
        self.mouse_filter.mousePressed.connect(self.onMousePressed)
        self.mouse_filter.mouseReleased.connect(self.onMouseReleased)
        self.ui.color_palette.installEventFilter(self.mouse_filter)

    def color(self) -> QColor:
        return self.__color

    def setColor(self, color: QColor) -> None:
        self.__color = color
        self.ui.setColorIcon(self.__color)

    @Slot(QColor)
    def onColorSelected(self, color: QColor) -> None:
        self.__color = color
        self.ui.setColorIcon(self.__color)
        self.ui.setChecked(False)
        self.ui.hidePalette()
        self.colorChanged.emit(self.__color)
        self.closed.emit()

    @Slot(bool)
    def onClicked(self, checked) -> None:
        # only if the button is checked, the other case is considered in the mouse event
        if checked:
            self.ui.showPalette()

    @Slot(QMouseEvent)
    def onMousePressed(self, event: QMouseEvent) -> None:
        point: QPointF = self.ui.color_palette.mapToGlobal(event.position())
        button_pos: QPointF = self.ui.mapToGlobal(QPoint(0, 0)).toPointF()
        palette_pos: QPointF = self.ui.mapToGlobal(QPoint(0, self.ui.height())).toPointF()

        button_rect_w: float = self.ui.width()
        button_rect_h: float = self.ui.height()
        button_rect: QRectF = QRectF(button_pos.x(), button_pos.y(), button_rect_w, button_rect_h)

        palette_rect_w: float = self.ui.color_palette.width()
        palette_rect_h: float = self.ui.color_palette.height()
        palette_rect: QRectF = QRectF(palette_pos.x(), palette_pos.y(), palette_rect_w, palette_rect_h)

        if not palette_rect.contains(point):
            if not button_rect.contains(point):
                self.ui.setChecked(False)
                self.ui.hidePalette()
                self.closed.emit()

    @Slot(QMouseEvent)
    def onMouseReleased(self, event: QMouseEvent) -> None:
        point: QPointF = self.ui.color_palette.mapToGlobal(event.position())
        button_pos: QPointF = self.ui.mapToGlobal(QPoint(0, 0)).toPointF()
        palette_pos: QPointF = self.ui.mapToGlobal(QPoint(0, self.ui.height())).toPointF()

        button_rect_w: float = self.ui.width()
        button_rect_h: float = self.ui.height()
        button_rect: QRectF = QRectF(button_pos.x(), button_pos.y(), button_rect_w, button_rect_h)

        palette_rect_w: float = self.ui.color_palette.width()
        palette_rect_h: float = self.ui.color_palette.height()
        palette_rect: QRectF = QRectF(palette_pos.x(), palette_pos.y(), palette_rect_w, palette_rect_h)

        if not palette_rect.contains(point):
            if button_rect.contains(point):
                self.ui.setChecked(False)
                self.ui.hidePalette()
                self.closed.emit()
