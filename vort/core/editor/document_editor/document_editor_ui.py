from PySide6.QtCore import Qt, QEvent, Signal, QPointF
from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtGui import QKeyEvent, QMouseEvent, QKeyEvent, QWheelEvent, QGuiApplication


class DocumentEditorUI(QGraphicsView):
    keyPressed: Signal = Signal(QKeyEvent)
    mousePressed: Signal = Signal(QMouseEvent)
    mouseReleased: Signal = Signal(QMouseEvent)
    mouseMoved: Signal = Signal(QMouseEvent)
    mouseLeft: Signal = Signal(QEvent)
    mouseDoubleClicked: Signal = Signal(QMouseEvent)

    zoomFactorChanged: Signal = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # TODO: to config
        self.zoom_factor_max: float = 3.0
        self.zoom_factor_min: float = 0.2
        self.zoom_factor_step: float = 0.1
        self.zoom_factor: float = 1.0
        self.epsilon: float = 0.0001
        self.mouse_scene_position: QPointF = QPointF()
        self.mouse_viewport_position: QPointF = QPointF()

    def setZoomFactor(self, zoom_factor: float) -> None:
        if abs(zoom_factor - self.zoom_factor_min) < self.epsilon:
            zoom_factor = self.zoom_factor_min
        elif abs(zoom_factor - self.zoom_factor_max) < self.epsilon:
            zoom_factor = self.zoom_factor_max
        elif zoom_factor < self.zoom_factor_min or zoom_factor > self.zoom_factor_max:
            return

        self.resetTransform()
        self.scale(zoom_factor, zoom_factor)
        self.zoom_factor = zoom_factor

    def zoom(self, zoom_factor: float) -> None:
        if abs(zoom_factor - self.zoom_factor_min) < self.epsilon:
            zoom_factor = self.zoom_factor_min
        elif abs(zoom_factor - self.zoom_factor_max) < self.epsilon:
            zoom_factor = self.zoom_factor_max
        elif zoom_factor < self.zoom_factor_min or zoom_factor > self.zoom_factor_max:
            return

        zoom_factor = round(zoom_factor / self.zoom_factor_step) * self.zoom_factor_step
        self.resetTransform()
        self.scale(zoom_factor, zoom_factor)
        self.zoom_factor = zoom_factor

        self.centerOn(self.mouse_scene_position)
        viewport_center_position: QPointF = QPointF(self.viewport().width() / 2.0, self.viewport().height() / 2.0)
        mouse_center_position: QPointF = self.mouse_viewport_position - viewport_center_position
        new_mouse_scene_position: QPointF = self.mapFromScene(self.mouse_scene_position).toPointF()
        new_viewport_center: QPointF = new_mouse_scene_position - mouse_center_position
        self.centerOn(self.mapToScene(new_viewport_center.toPoint()))
        self.zoomFactorChanged.emit(self.zoom_factor)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.mouse_viewport_position = QPointF(event.position().toPoint())
        self.mouse_scene_position = self.mapToScene(event.position().toPoint())

        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        wheel_event: QWheelEvent = QWheelEvent(event)
        if QGuiApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            angle: float = wheel_event.angleDelta().y()
            if angle > 0:
                self.zoom(self.zoom_factor + self.zoom_factor_step)
            else:
                self.zoom(self.zoom_factor - self.zoom_factor_step)

            return

        return super().wheelEvent(event)

    def event(self, event: QEvent) -> bool:
        if isinstance(event, QKeyEvent) and event.type() == QEvent.Type.KeyPress:
            self.keyPressed.emit(event)
            return True

        return super().event(event)

    def viewportEvent(self, event: QEvent) -> bool:
        if isinstance(event, QMouseEvent):
            match event.type():
                case QEvent.Type.MouseButtonPress:
                    self.mousePressed.emit(event)
                case QEvent.Type.MouseButtonRelease:
                    self.mouseReleased.emit(event)
                case QEvent.Type.MouseMove:
                    self.mouseMoved.emit(event)
                case QEvent.Type.MouseButtonDblClick:
                    self.mouseDoubleClicked.emit(event)
        match event.type():
            case QEvent.Type.Leave:
                self.mouseLeft.emit(event)

        return super().viewportEvent(event)
