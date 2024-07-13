from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor, QTextBlock, QTextFragment, QImage, QTextDocument, QTextImageFormat


class HyperlinkSelection:
    def __init__(self) -> None:
        self.hyperlink: str = ""
        self.start: int = 0
        self.end: int = 0


class ImageSelection:
    def __init__(self) -> None:
        self.name: str = ""
        self.start: int = 0
        self.end: int = 0


class SelectionComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def selectedText(self) -> str:
        return self.__cursor.selectedText()

    def selectWord(self, position: int) -> None:
        self.__cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
        self.__cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        self.repaintRequest.emit()

    def selectDocument(self) -> None:
        self.__cursor.select(QTextCursor.SelectionType.Document)
        self.repaintRequest.emit()

    def selectedImage(self) -> QImage:
        name: str = ""

        if self.__cursor.hasSelection():
            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            selections: list[ImageSelection] = []

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            while helper.position() <= selection_end:

                block = helper.block()
                it: QTextBlock.iterator = block.begin()

                while it != block.end():
                    fragment: QTextFragment = it.fragment()

                    fragment_start: int = fragment.position()
                    fragment_end: int = fragment.position() + fragment.length()

                    # --------|--------case-4--------|--------
                    # ---------------|-case-3-|---------------
                    # -----------|----fragment----|-----------
                    # --|----case-1----|----|----case-2----|--

                    # case 1
                    if (
                        selection_start <= fragment_start
                        and selection_start <= selection_end
                        and selection_end <= fragment_end
                        and fragment_start < selection_end
                    ):
                        helper.setPosition(fragment_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(selection_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: ImageSelection = ImageSelection()
                        selection.name = fragment.charFormat().toImageFormat().name()
                        selection.start = fragment_start
                        selection.end = selection_end
                        selections.append(selection)

                    # case 2
                    elif (
                        fragment_end <= selection_end
                        and fragment_start <= selection_start
                        and selection_start <= fragment_end
                        and selection_start < fragment_end
                    ):
                        helper.setPosition(selection_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(fragment_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: ImageSelection = ImageSelection()
                        selection.name = fragment.charFormat().toImageFormat().name()
                        selection.start = selection_start
                        selection.end = fragment_end
                        selections.append(selection)

                    # case 3
                    elif (
                        fragment_start <= selection_start
                        and selection_start <= fragment_end
                        and fragment_start <= selection_end
                        and selection_end <= fragment_end
                        and selection_start < selection_end
                    ):
                        helper.setPosition(selection_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(selection_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: ImageSelection = ImageSelection()
                        selection.name = fragment.charFormat().toImageFormat().name()
                        selection.start = selection_start
                        selection.end = selection_end
                        selections.append(selection)

                    # case 4
                    elif (
                        selection_start <= fragment_start
                        and fragment_start <= selection_end
                        and selection_start <= fragment_end
                        and fragment_end <= selection_end
                        and fragment_start < fragment_end
                    ):
                        helper.setPosition(fragment_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(fragment_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: ImageSelection = ImageSelection()
                        selection.name = fragment.charFormat().toImageFormat().name()
                        selection.start = fragment_start
                        selection.end = fragment_end
                        selections.append(selection)

                    it += 1

                if block.position() + block.length() <= selection_end:
                    helper.setPosition(block.position() + block.length(), QTextCursor.MoveMode.MoveAnchor)
                else:
                    break

            prev_position = selection_start
            need_name = True
            for selection in selections:
                if selection.start == prev_position:
                    if need_name and (prev_position == selection_start or name == selection.name):
                        name = selection.name

                    else:
                        need_name = False
                        name = ""

                    prev_position = selection.end

                else:
                    break

        else:
            name = self.__cursor.charFormat().toImageFormat().name()

        image: QImage | None = self.__cursor.document().resource(QTextDocument.ResourceType.ImageResource, name)

        if image is None:
            return QImage()

        return image

    def selectImage(self) -> None:
        if self.__cursor.hasSelection():
            # you can check selection using selectedHyperlink method
            return

        name = self.__cursor.charFormat().toImageFormat().name()

        if name != "":
            block: QTextBlock = self.__cursor.block()
            it: QTextBlock.iterator = block.begin()

            while it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.contains(self.__cursor.position()):
                    # if (
                    #     self.__cursor.position() == fragment.position()
                    #     or self.__cursor.position() == fragment.position() + fragment.length()
                    # ):
                    #     return

                    self.__cursor.setPosition(fragment.position())
                    self.__cursor.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    break

                it += 1

        self.repaintRequest.emit()

    def selectedHyperlink(self) -> str:
        hyperlink = ""

        if self.__cursor.hasSelection():
            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            selections: list[HyperlinkSelection] = []

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            while helper.position() <= selection_end:

                block = helper.block()
                it: QTextBlock.iterator = block.begin()

                while it != block.end():
                    fragment: QTextFragment = it.fragment()

                    fragment_start: int = fragment.position()
                    fragment_end: int = fragment.position() + fragment.length()

                    # --------|--------case-4--------|--------
                    # ---------------|-case-3-|---------------
                    # -----------|----fragment----|-----------
                    # --|----case-1----|----|----case-2----|--

                    # case 1
                    if (
                        selection_start <= fragment_start
                        and selection_start <= selection_end
                        and selection_end <= fragment_end
                        and fragment_start < selection_end
                    ):
                        helper.setPosition(fragment_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(selection_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: HyperlinkSelection = HyperlinkSelection()
                        selection.hyperlink = fragment.charFormat().anchorHref()
                        selection.start = fragment_start
                        selection.end = selection_end
                        selections.append(selection)

                    # case 2
                    elif (
                        fragment_end <= selection_end
                        and fragment_start <= selection_start
                        and selection_start <= fragment_end
                        and selection_start < fragment_end
                    ):
                        helper.setPosition(selection_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(fragment_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: HyperlinkSelection = HyperlinkSelection()
                        selection.hyperlink = fragment.charFormat().anchorHref()
                        selection.start = selection_start
                        selection.end = fragment_end
                        selections.append(selection)

                    # case 3
                    elif (
                        fragment_start <= selection_start
                        and selection_start <= fragment_end
                        and fragment_start <= selection_end
                        and selection_end <= fragment_end
                        and selection_start < selection_end
                    ):
                        helper.setPosition(selection_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(selection_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: HyperlinkSelection = HyperlinkSelection()
                        selection.hyperlink = fragment.charFormat().anchorHref()
                        selection.start = selection_start
                        selection.end = selection_end
                        selections.append(selection)

                    # case 4
                    elif (
                        selection_start <= fragment_start
                        and fragment_start <= selection_end
                        and selection_start <= fragment_end
                        and fragment_end <= selection_end
                        and fragment_start < fragment_end
                    ):
                        helper.setPosition(fragment_start, QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(fragment_end, QTextCursor.MoveMode.KeepAnchor)

                        selection: HyperlinkSelection = HyperlinkSelection()
                        selection.hyperlink = fragment.charFormat().anchorHref()
                        selection.start = fragment_start
                        selection.end = fragment_end
                        selections.append(selection)

                    it += 1

                if block.position() + block.length() <= selection_end:
                    helper.setPosition(block.position() + block.length(), QTextCursor.MoveMode.MoveAnchor)
                else:
                    break

            prev_position = selection_start
            need_hyperlink = True
            for selection in selections:
                if selection.start == prev_position:
                    if need_hyperlink and (prev_position == selection_start or hyperlink == selection.hyperlink):
                        hyperlink = selection.hyperlink

                    else:
                        need_hyperlink = False
                        hyperlink = ""

                    prev_position = selection.end

                else:
                    break

        else:
            hyperlink = self.__cursor.charFormat().anchorHref()

            if hyperlink != "":
                block: QTextBlock = self.__cursor.block()
                it: QTextBlock.iterator = block.begin()

                while it != block.end():
                    fragment: QTextFragment = it.fragment()

                    if (
                        self.__cursor.position() == fragment.position()
                        or self.__cursor.position() == fragment.position() + fragment.length()
                    ):
                        hyperlink = ""
                        break

                    it += 1

        return hyperlink

    def selectHyperlink(self) -> None:
        if self.__cursor.hasSelection():
            # you can check selection using selectedHyperlink method
            return

        hyperlink = self.__cursor.charFormat().anchorHref()

        if hyperlink != "":
            block: QTextBlock = self.__cursor.block()
            it: QTextBlock.iterator = block.begin()

            while it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.contains(self.__cursor.position()):
                    if (
                        self.__cursor.position() == fragment.position()
                        or self.__cursor.position() == fragment.position() + fragment.length()
                    ):
                        return

                    self.__cursor.setPosition(fragment.position())
                    self.__cursor.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    break

                it += 1

        self.repaintRequest.emit()
