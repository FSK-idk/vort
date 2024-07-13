from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget


from core.editor.text_editor.text_document_context import TextDocumentContext


# text editor only supports one cursor at a time


class TextEditor(QObject):
    repaintRequest: Signal = Signal()
    updateUIRequest: Signal = Signal()
    charCountChanged: Signal = Signal(int)

    def __init__(self, context: TextDocumentContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__context: TextDocumentContext = context

        # signal

        self.__context.history_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.history_component.repaintRequest.connect(self.updateUIRequest.emit)
        self.__context.clipboard_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.clipboard_component.repaintRequest.connect(self.updateUIRequest.emit)
        self.__context.selection_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.input_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.input_component.repaintRequest.connect(self.updateUIRequest.emit)
        self.__context.movement_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.movement_component.repaintRequest.connect(self.updateUIRequest.emit)
        self.__context.paragraph_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.char_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.text_style_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.text_style_component.repaintRequest.connect(self.updateUIRequest.emit)
        self.__context.finder_component.repaintRequest.connect(self.repaintRequest.emit)
        self.__context.finder_component.repaintRequest.connect(self.updateUIRequest.emit)

        self.__context.layout.characterCountChanged.connect(self.charCountChanged.emit)

    def context(self) -> TextDocumentContext:
        return self.__context
