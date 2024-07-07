from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel


class ZoomSlider(QWidget):
    zoomFactorChanged = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.slider: QSlider = QSlider(self)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMaximum(300)
        self.slider.setMinimum(25)
        self.slider.setValue(100)
        self.setFixedWidth(100)

        self.label: QLabel = QLabel(self)
        self.label.setText("100%")
        self.label.setFixedWidth(30)

        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)

        self.slider.valueChanged.connect(self.onSliderValueChanged)

    @Slot()
    def onSliderValueChanged(self, value: int) -> None:
        if abs(value - 100) < 10:
            self.slider.blockSignals(True)
            self.slider.setValue(100)
            self.slider.blockSignals(False)
        self.label.setText(f"{self.slider.value()}%")
        self.zoomFactorChanged.emit(self.slider.value() / 100)

    def setZoomFactor(self, zoom_factor: float) -> None:
        self.slider.setValue(round(zoom_factor * 100))
        self.label.setText(f"{round(zoom_factor * 100)}%")
