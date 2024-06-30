from PySide6.QtWidgets import QWidget, QLabel


class CharacterCountLabel(QLabel):
    def __init_(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setText("0 characters")

    def setCharacterCount(self, character_count: int) -> None:
        text = "1 character" if character_count == 1 else f"{character_count} characters"
        self.setText(text)
