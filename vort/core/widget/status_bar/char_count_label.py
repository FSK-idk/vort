from PySide6.QtWidgets import QWidget, QLabel


class CharCountLabel(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setText("0 characters")

    def setCharCount(self, count: int) -> None:
        text = f"{count} character" + ("s" if count != 1 else "")
        self.setText(text)
