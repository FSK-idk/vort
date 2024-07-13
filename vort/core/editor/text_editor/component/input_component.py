from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QTextCursor, QTextBlock, QTextFragment


class InputComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def insertText(self, text: str) -> None:
        self.__cursor.beginEditBlock()

        is_block_start: bool = False

        selection_start = self.__cursor.selectionStart()
        helper: QTextCursor = QTextCursor(self.__cursor.document())
        helper.setPosition(selection_start)

        if helper.atBlockStart():
            is_block_start = True

        if self.__cursor.charFormat().isImageFormat():
            self.__cursor.setCharFormat(helper.blockCharFormat())

        if is_block_start:
            helper.setPosition(selection_start)
            block_char_format = helper.charFormat()
            block_char_format.setAnchorHref("")
            self.__cursor.mergeBlockCharFormat(block_char_format)

        self.__cursor.insertText(text)

        self.fixupImage()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def deletePrevious(self, modifiers: Qt.KeyboardModifier) -> None:
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            self.__cursor.beginEditBlock()

            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_end)

            if helper.atBlockEnd() or helper.charFormat().isImageFormat():
                helper.setPosition(selection_start)
                block_char_format = helper.blockCharFormat()
            else:
                helper.setPosition(selection_end + 1)
                block_char_format = helper.charFormat()

            # has selection -> delete selection
            if self.__cursor.hasSelection():
                self.__cursor.deletePreviousChar()

            # line with image, left side -> delete image
            elif self.__cursor.atBlockStart() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.deleteChar()

            # line with image, right side -> delete image
            elif self.__cursor.atBlockEnd() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.deletePreviousChar()

            # left side
            elif self.__cursor.atBlockStart() and self.__cursor.blockNumber() > 0:
                self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore

                # line under image -> delete image, move line up
                if self.__cursor.charFormat().isImageFormat():
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.__cursor.deletePreviousChar()

                # move up
                else:
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.deletePreviousChar()

            # otherwise delete prev word
            else:
                self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.KeepAnchor)
                self.__cursor.deletePreviousChar()

            if self.__cursor.atBlockStart():
                block_char_format.setAnchorHref("")
                self.__cursor.mergeBlockCharFormat(block_char_format)

            self.fixupImage()
            self.__cursor.endEditBlock()

        if modifiers in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
            self.__cursor.beginEditBlock()

            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_end)

            if helper.atBlockEnd() or helper.charFormat().isImageFormat():
                helper.setPosition(selection_start)
                block_char_format = helper.blockCharFormat()
            else:
                helper.setPosition(selection_end + 1)
                block_char_format = helper.charFormat()

            # has selection -> delete selection
            if self.__cursor.hasSelection():
                self.__cursor.deletePreviousChar()

            # line with image, left side -> delete char from prev line
            elif (
                self.__cursor.atBlockStart()
                and self.__cursor.blockNumber() > 0
                and self.__cursor.charFormat().isImageFormat()
            ):
                self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)
                self.__cursor.deletePreviousChar()
                # self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)

            # line with image, right side -> delete image
            elif self.__cursor.atBlockEnd() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor)
                self.__cursor.deletePreviousChar()

            # left side
            elif self.__cursor.atBlockStart() and self.__cursor.blockNumber() > 0:
                self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore

                # line under image -> delete image, move line up
                if self.__cursor.charFormat().isImageFormat():
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.__cursor.deletePreviousChar()

                # move up
                else:
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.deletePreviousChar()

            # otherwise delete prev char
            else:
                self.__cursor.deletePreviousChar()

            if self.__cursor.atBlockStart():
                block_char_format.setAnchorHref("")
                self.__cursor.mergeBlockCharFormat(block_char_format)

            self.fixupImage()
            self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def delete(self, modifiers: Qt.KeyboardModifier) -> None:
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            self.__cursor.beginEditBlock()

            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            if helper.atBlockStart() or helper.charFormat().isImageFormat():
                helper.setPosition(selection_end)
                block_char_format = helper.blockCharFormat()
            else:
                helper.setPosition(selection_start)
                block_char_format = helper.charFormat()

            # has selection -> delete selection
            if self.__cursor.hasSelection():
                self.__cursor.deleteChar()

            # line with image, left side -> delete image
            elif self.__cursor.atBlockStart() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.deleteChar()

            # line with image, right side -> delete image
            elif self.__cursor.atBlockEnd() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.deletePreviousChar()

            # right side
            elif self.__cursor.atBlockEnd() and self.__cursor.blockNumber() < self.__cursor.document().blockCount() - 1:
                self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)

                # line above image -> delete image, move line after up
                if self.__cursor.charFormat().isImageFormat():
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.__cursor.deleteChar()
                    self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore

                # move up
                else:
                    self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.deleteChar()

            # otherwise delete next word
            else:
                self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor)
                self.__cursor.deleteChar()

            if self.__cursor.atBlockStart():
                block_char_format.setAnchorHref("")
                self.__cursor.mergeBlockCharFormat(block_char_format)

            self.fixupImage()
            self.__cursor.endEditBlock()

        if modifiers in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
            self.__cursor.beginEditBlock()

            selection_start = self.__cursor.selectionStart()
            selection_end = self.__cursor.selectionEnd()

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            if helper.atBlockStart() or helper.charFormat().isImageFormat():
                helper.setPosition(selection_end)
                block_char_format = helper.blockCharFormat()
            else:
                helper.setPosition(selection_start)
                block_char_format = helper.charFormat()

            # has selection -> delete selection
            if self.__cursor.hasSelection():
                self.__cursor.deleteChar()

            # line with image, left side -> delete image
            elif self.__cursor.atBlockStart() and self.__cursor.charFormat().isImageFormat():
                self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                self.__cursor.deleteChar()
                self.__cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)

            # line with image, right side -> delete char from next line
            elif (
                self.__cursor.atBlockEnd()
                and self.__cursor.blockNumber() < self.__cursor.document().blockCount() - 1
                and self.__cursor.charFormat().isImageFormat()
            ):
                self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)
                self.__cursor.deleteChar()

            # right side
            elif self.__cursor.atBlockEnd() and self.__cursor.blockNumber() < self.__cursor.document().blockCount() - 1:
                self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor)

                # line above image -> delete image, move line after up
                if self.__cursor.charFormat().isImageFormat():
                    self.__cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.__cursor.deleteChar()
                    self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore

                # delete char
                else:
                    self.__cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)  # type: ignore
                    self.__cursor.deleteChar()

            # otherwise delete char
            else:
                self.__cursor.deleteChar()

            if self.__cursor.atBlockStart():
                block_char_format.setAnchorHref("")
                self.__cursor.mergeBlockCharFormat(block_char_format)

            self.fixupImage()
            self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def fixupImage(self) -> None:
        # position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha
        images: list[tuple[int, bool, bool, bool, bool]] = []

        for i in range(self.__cursor.document().blockCount()):
            block: QTextBlock = self.__cursor.document().findBlockByNumber(i)

            it: QTextBlock.iterator = block.begin()
            while it != block.end():
                frag: QTextFragment = it.fragment()

                if frag.charFormat().isImageFormat():
                    if frag.length() > 0:
                        # is first
                        offset = 0

                        if it != block.begin():
                            it -= 1
                            if not it.fragment().charFormat().isImageFormat():
                                if block.position() == frag.position():
                                    images.append((frag.position() + offset, True, False, False, False))
                                else:
                                    images.append((frag.position() + offset, False, True, False, False))
                                offset += 1
                            it += 1
                        else:
                            if block.position() == frag.position():
                                images.append((frag.position() + offset, True, False, False, False))
                            else:
                                images.append((frag.position() + offset, False, True, False, False))
                            offset += 1

                        # is not first
                        while offset < frag.length():
                            images.append((frag.position() + offset, False, False, True, False))
                            offset += 1

                        it += 1
                        if it != block.end():
                            if not it.fragment().charFormat().isImageFormat():
                                position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha = images[-1]
                                images[-1] = (position, is_pref_empty, is_pref_alpha, is_pref_img, True)
                        it -= 1

                it += 1

        # case 1
        # [alpha] \img/ || [alpha]

        # case 2
        # [empty] \img/ || [alpha]

        # case 3
        # [alpha] \img/ || [empty]

        # case 4
        # [empty] \alpha/ || [img]

        # case 5
        # [img] \alpha/ || [empty]

        # case 6
        # [img] \alpha/ || [empty]

        # case 7
        # [empty] \img/ || [img]

        helper: QTextCursor = QTextCursor(self.__cursor.document())
        helper2: QTextCursor = QTextCursor(self.__cursor.document())

        is_case_4 = False
        if not self.__cursor.atBlockStart() and not self.__cursor.atBlockEnd():
            helper.setPosition(self.__cursor.position() + 1)
            if self.__cursor.charFormat().isCharFormat() and helper.charFormat().isImageFormat():
                is_case_4 = True

        offset = 0

        for position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha in images:
            helper.beginEditBlock()
            if is_pref_alpha or is_pref_img:
                helper.setPosition(position + offset)

                if is_pref_alpha:
                    last_char_format = helper.charFormat()

                if is_pref_img:
                    last_char_format = helper.blockCharFormat()

                helper.insertBlock()

                helper.setBlockCharFormat(last_char_format)

                helper.movePosition(QTextCursor.MoveOperation.PreviousBlock)
                helper.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)

                offset += 1

            if is_suff_alpha:
                helper.setPosition(position + offset + 1)

                helper2.setPosition(helper.position() + 1)
                last_char_format = helper2.charFormat()

                helper.insertBlock()

                helper.setBlockCharFormat(last_char_format)

                offset += 1

            helper.endEditBlock()

        if is_case_4:
            self.__cursor.setPosition(self.__cursor.position() - 1)
