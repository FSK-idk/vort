from PySide6.QtCore import Slot, Signal, Qt
from PySide6.QtWidgets import QFontComboBox, QWidget
from PySide6.QtGui import QFont, QWheelEvent


class FontComboBox(QFontComboBox):
    fontFamilyChanged = Signal(str)
    closed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.currentFontChanged.connect(self.onCurrentFontChanged)
        self.activated.connect(self.onActivated)
        self.lineEdit().returnPressed.connect(self.onLineEditReturnPressed)

    def setFontFamily(self, font_family: str) -> None:
        self.setCurrentFont(font_family)

    @Slot(int)
    def onActivated(self, index: int) -> None:
        self.closed.emit()

    @Slot(QFont)
    def onCurrentFontChanged(self, font: QFont) -> None:
        self.fontFamilyChanged.emit(font.family())

    @Slot()
    def onLineEditReturnPressed(self) -> None:
        self.closed.emit()

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()
