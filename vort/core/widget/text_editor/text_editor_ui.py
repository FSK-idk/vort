from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtGui import QKeyEvent, QMouseEvent, QKeyEvent


class TextEditorUI(QGraphicsView):
    keyPressed = Signal(QKeyEvent)
    mousePressed = Signal(QMouseEvent)
    mouseMoved = Signal(QMouseEvent)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def event(self, event: QEvent) -> bool:
        if isinstance(event, QKeyEvent) and event.type() == QEvent.Type.KeyPress:
            self.keyPressed.emit(event)

        return super().event(event)

    def viewportEvent(self, event: QEvent) -> bool:
        if isinstance(event, QMouseEvent):
            match event.type():
                case QEvent.Type.MouseButtonPress:
                    self.mousePressed.emit(event)
                case QEvent.Type.MouseMove:
                    self.mouseMoved.emit(event)

        return super().viewportEvent(event)
