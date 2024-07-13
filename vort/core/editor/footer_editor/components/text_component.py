from PySide6.QtCore import QObject, Signal


class TextComponent(QObject):
    applied: Signal = Signal()
    textTurned: Signal = Signal(bool)

    def __init__(self) -> None:
        super().__init__()

        self.__is_text_turned: bool = False
        self.__text: str = ""

    def isTextTurned(self) -> bool:
        return self.__is_text_turned

    def setTextTurned(self, is_turned: bool) -> None:
        if self.__is_text_turned != is_turned:
            self.__is_text_turned = is_turned
            self.textTurned.emit(self.__is_text_turned)
            self.applied.emit()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        if self.__text != text:
            self.__text = text
            self.applied.emit()
