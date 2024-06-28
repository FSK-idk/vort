from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject


class Controller(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.ui: QWidget
