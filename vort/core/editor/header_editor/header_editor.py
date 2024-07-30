from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QTextCursor

from core.editor.header_editor.header_document_context import HeaderDocumentContext


class HeaderEditor(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, context: HeaderDocumentContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__context: HeaderDocumentContext = context

        # signal

        self.__context.layout.pageCountChanged.connect(self.onPageCountChanged)

        self.__context.formatting_component.applied.connect(self.repaintRequest.emit)

        self.__context.page_component.applied.connect(self.updateContent)
        self.__context.page_component.applied.connect(self.repaintRequest.emit)

        self.__context.pagination_component.paginationTurned.connect(self.onPaginationTurned)
        self.__context.pagination_component.applied.connect(self.updateContent)
        self.__context.pagination_component.applied.connect(self.repaintRequest.emit)

        self.__context.text_component.textTurned.connect(self.onTextTurned)
        self.__context.text_component.applied.connect(self.updateContent)
        self.__context.text_component.applied.connect(self.repaintRequest.emit)

    def context(self) -> HeaderDocumentContext:
        return self.__context

    @Slot()
    def updateContent(self) -> None:
        for i in range(self.__context.page_component.pageCount()):
            block = self.__context.document.findBlockByNumber(i)

            self.__context.cursor.setPosition(block.position())
            self.__context.cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

            if i == 0 and not self.__context.page_component.isFirstPageIncluded():
                self.__context.cursor.insertText("")

            elif self.__context.pagination_component.isPaginationTurned():
                self.__context.cursor.insertText(str(self.__context.pagination_component.paginationStartingNumber() + i))  # type: ignore

            elif self.__context.text_component.isTextTurned():
                self.__context.cursor.insertText(self.__context.text_component.text())

            else:
                self.__context.cursor.insertText("")

        self.__context.formatting_component.formatDocument()

    @Slot(int)
    def onPageCountChanged(self, count: int) -> None:
        difference = count - self.__context.page_component.pageCount()
        if difference > 0:
            self.__context.page_component.addPage(difference)
        elif difference < 0:
            self.__context.page_component.removePage(-difference)

    @Slot(bool)
    def onPaginationTurned(self, is_turned) -> None:
        if is_turned:
            self.__context.text_component.setTextTurned(False)

    @Slot(bool)
    def onTextTurned(self, is_turned) -> None:
        if is_turned:
            self.__context.pagination_component.setPaginationTurned(False)
