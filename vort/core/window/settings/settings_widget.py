from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDoubleSpinBox, QComboBox, QSpinBox
from PySide6.QtGui import QWheelEvent


class ComboBox(QComboBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)


class SpinBox(QSpinBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)
