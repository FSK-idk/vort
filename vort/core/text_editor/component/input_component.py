import hashlib

from PySide6.QtCore import Qt, QMimeData, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import (
    QTextCursor,
    QFont,
    QTextBlockFormat,
    QGuiApplication,
    QKeyEvent,
    QTextBlock,
    QTextFragment,
    QTextImageFormat,
    QImage,
    QColor,
    QTextDocument,
    QTextDocumentFragment,
    QTextCharFormat,
)

from core.text_editor.component.component import Component


class InputComponent(Component):
    def cut(self) -> None:
        if self._text_cursor.hasSelection():
            self._text_cursor.beginEditBlock()
            mime_data: QMimeData = QMimeData()
            selection = self._text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QGuiApplication.clipboard().setMimeData(mime_data)
            self._text_cursor.removeSelectedText()
            self.fixup()
            self._text_cursor.endEditBlock()
            self.applied.emit()

    def copy(self) -> None:
        if self._text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self._text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QGuiApplication.clipboard().setMimeData(mime_data)
            self.applied.emit()

    def paste(self) -> None:
        if self.insertImage():
            return
        if self.insertText():
            return
        if self.insertPlainText():
            return

    def insertText(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()
        if not mime_data.hasHtml():
            return False

        self._text_cursor.beginEditBlock()

        is_block_start: bool = self._text_cursor.atBlockStart()
        prev_position: int = self._text_cursor.position()

        self._text_cursor.insertHtml(self.parse_to_html(mime_data.html()))

        if is_block_start:
            new_position: int = self._text_cursor.position()
            self._text_cursor.setPosition(prev_position, QTextCursor.MoveMode.MoveAnchor)
            self._text_cursor.setBlockCharFormat(self._text_cursor.charFormat())
            self._text_cursor.setPosition(new_position, QTextCursor.MoveMode.MoveAnchor)

        self.fixup()
        self._text_cursor.endEditBlock()

        self.applied.emit()

        return True

    def insertPlainText(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()
        if not mime_data.hasText():
            return False

        self._text_cursor.beginEditBlock()

        is_block_start: bool = self._text_cursor.atBlockStart()
        prev_position: int = self._text_cursor.position()

        self._text_cursor.insertText(self.parse_to_plain_text(mime_data.text()))

        if is_block_start:
            new_position: int = self._text_cursor.position()
            self._text_cursor.setPosition(prev_position, QTextCursor.MoveMode.MoveAnchor)
            self._text_cursor.setBlockCharFormat(self._text_cursor.charFormat())
            self._text_cursor.setPosition(new_position, QTextCursor.MoveMode.MoveAnchor)

        self.fixup()
        self._text_cursor.endEditBlock()
        self.applied.emit()

        return True

    def insertImage(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()
        if not mime_data.hasImage():
            return False

        self._text_cursor.beginEditBlock()

        image: QImage = QImage(mime_data.imageData())

        bytes_array: QByteArray = QByteArray()
        buffer: QBuffer = QBuffer(bytes_array)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "png")
        image_bytes: bytes = bytes_array.data()

        name: str = f"pasted_image_{hashlib.sha256(image_bytes).hexdigest()}"

        self._text_cursor.document().addResource(QTextDocument.ResourceType.ImageResource, name, image)

        image_format: QTextImageFormat = QTextImageFormat()
        image_format.setWidth(image.width())
        image_format.setHeight(image.height())
        image_format.setName(name)
        image_format.setForeground(QColor("black"))
        image_format.setBackground(QColor("white"))

        self._text_cursor.insertImage(image_format)

        self.fixup()
        self._text_cursor.endEditBlock()
        self.applied.emit()

        return True

    def insertHyperlink(self, text: str, hyperlink: str) -> bool:
        if text == "" and not self._text_cursor.hasSelection():
            return False

        self._text_cursor.beginEditBlock()

        format = self._text_cursor.charFormat()
        if format.isImageFormat():
            format = self._text_cursor.blockCharFormat()

        format.setAnchorHref(hyperlink)
        self._text_cursor.insertText(text, format)

        self.fixup()
        self._text_cursor.endEditBlock()
        self.applied.emit()

        return True

    def input(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.text():
            match event.key():
                case Qt.Key.Key_Backspace:
                    self._text_cursor.beginEditBlock()

                    format = self._text_cursor.charFormat()

                    # has selection -> delete selection
                    if self._text_cursor.hasSelection():
                        self._text_cursor.deletePreviousChar()

                    # line with image, left side -> delete image
                    elif self._text_cursor.atBlockStart() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deletePreviousChar()

                    # line with image, right side -> delete image
                    elif self._text_cursor.atBlockEnd() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deletePreviousChar()

                    # left side
                    elif self._text_cursor.atBlockStart() and self._text_cursor.blockNumber() > 0:
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                        # line under image -> delete image, move line up
                        if self._text_cursor.charFormat().isImageFormat():
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor
                            )
                            self._text_cursor.deletePreviousChar()

                        # delete prev char
                        else:
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.deletePreviousChar()

                    # otherwise delete prev word
                    else:
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deletePreviousChar()

                    if self._text_cursor.atBlockStart():
                        format.setAnchorHref("")
                        self._text_cursor.mergeBlockCharFormat(format)

                    self.fixup()
                    self._text_cursor.endEditBlock()

                case Qt.Key.Key_Delete:
                    self._text_cursor.beginEditBlock()

                    format = self._text_cursor.charFormat()

                    # has selection -> delete selection
                    if self._text_cursor.hasSelection():
                        self._text_cursor.deleteChar()

                    # line with image, left side -> delete image
                    elif self._text_cursor.atBlockStart() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deleteChar()

                    # line with image, right side -> delete image
                    elif self._text_cursor.atBlockEnd() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deleteChar()

                    # right side
                    elif (
                        self._text_cursor.atBlockEnd()
                        and self._text_cursor.blockNumber() < self._text_cursor.document().blockCount() - 1
                    ):
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                        # line above image -> delete image, move line after up
                        if self._text_cursor.charFormat().isImageFormat():
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor
                            )
                            self._text_cursor.deleteChar()
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                            )

                        # delete prev char
                        else:
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.deleteChar()

                    # otherwise delete next word
                    else:
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deleteChar()

                    if self._text_cursor.atBlockStart():
                        format.setAnchorHref("")
                        self._text_cursor.mergeBlockCharFormat(format)

                    self.fixup()
                    self._text_cursor.endEditBlock()

                case _:
                    return

            self.applied.emit()
            return

        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
            match event.key():
                case Qt.Key.Key_Backspace:
                    self._text_cursor.beginEditBlock()

                    format = self._text_cursor.charFormat()

                    # has selection -> delete selection
                    if self._text_cursor.hasSelection():
                        self._text_cursor.deletePreviousChar()

                    # line with image, left side -> delete char from prev line
                    elif (
                        self._text_cursor.atBlockStart()
                        and self._text_cursor.blockNumber() > 0
                        and self._text_cursor.charFormat().isImageFormat()
                    ):
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                        )
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                        )
                        self._text_cursor.deletePreviousChar()
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                    # line with image, right side -> delete image
                    elif self._text_cursor.atBlockEnd() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deletePreviousChar()

                    # left side
                    elif self._text_cursor.atBlockStart() and self._text_cursor.blockNumber() > 0:
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                        # line under image -> delete image, move line up
                        if self._text_cursor.charFormat().isImageFormat():
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor
                            )
                            self._text_cursor.deletePreviousChar()

                        # delete prev char
                        else:
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.deletePreviousChar()

                    # otherwise delete prev char
                    else:
                        self._text_cursor.deletePreviousChar()

                    if self._text_cursor.atBlockStart():
                        format.setAnchorHref("")
                        self._text_cursor.mergeBlockCharFormat(format)

                    self.fixup()
                    self._text_cursor.endEditBlock()

                case Qt.Key.Key_Delete:
                    self._text_cursor.beginEditBlock()

                    format = self._text_cursor.charFormat()

                    # has selection -> delete selection
                    if self._text_cursor.hasSelection():
                        self._text_cursor.deleteChar()

                    # line with image, left side -> delete image
                    elif self._text_cursor.atBlockStart() and self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor
                        )
                        self._text_cursor.deleteChar()
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                    # line with image, right side -> delete char from next line
                    elif (
                        self._text_cursor.atBlockEnd()
                        and self._text_cursor.blockNumber() < self._text_cursor.document().blockCount() - 1
                        and self._text_cursor.charFormat().isImageFormat()
                    ):
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                        )
                        self._text_cursor.deleteChar()
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                        )
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                    # right side
                    elif (
                        self._text_cursor.atBlockEnd()
                        and self._text_cursor.blockNumber() < self._text_cursor.document().blockCount() - 1
                    ):
                        self._text_cursor.movePosition(
                            QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.MoveAnchor
                        )

                        # line above image -> delete image, move line after up
                        if self._text_cursor.charFormat().isImageFormat():
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor
                            )
                            self._text_cursor.deleteChar()
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                            )

                        # delete char
                        else:
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.movePosition(
                                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor
                            )
                            self._text_cursor.deleteChar()

                    # otherwise delete char
                    else:
                        self._text_cursor.deleteChar()

                    if self._text_cursor.atBlockStart():
                        format.setAnchorHref("")
                        self._text_cursor.mergeBlockCharFormat(format)

                    self.fixup()
                    self._text_cursor.endEditBlock()

                case Qt.Key.Key_Enter:
                    return  # ignore
                case Qt.Key.Key_Escape:
                    return  # ignore

                case _ if event.text():
                    self._text_cursor.beginEditBlock()

                    if self._text_cursor.charFormat().isImageFormat():
                        self._text_cursor.setCharFormat(self._text_cursor.blockCharFormat())

                    if self._text_cursor.atBlockStart():
                        format = self._text_cursor.charFormat()
                        format.setAnchorHref("")
                        self._text_cursor.mergeBlockCharFormat(format)

                    self._text_cursor.insertText(event.text())

                    self.fixup()
                    self._text_cursor.endEditBlock()

            self.applied.emit()

    def fixup(self) -> None:
        # position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha
        images: list[tuple[int, bool, bool, bool, bool]] = []

        for i in range(self._text_cursor.document().blockCount()):
            block: QTextBlock = self._text_cursor.document().findBlockByNumber(i)

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

        offset = 0

        helper: QTextCursor = QTextCursor(self._text_cursor.document())

        for position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha in images:
            helper.beginEditBlock()
            if is_pref_alpha or is_pref_img:
                helper.setPosition(position + offset)

                if is_pref_alpha:
                    _last_char_format = helper.charFormat()

                if is_pref_img:
                    _last_char_format = helper.blockCharFormat()

                helper.insertBlock()

                helper.setBlockCharFormat(_last_char_format)

                helper.movePosition(QTextCursor.MoveOperation.PreviousBlock)
                helper.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)

                offset += 1

            if is_suff_alpha:
                helper.setPosition(position + offset + 1)

                helper.insertBlock()

                offset += 1

            helper.endEditBlock()

        helper.setPosition(self._text_cursor.position(), QTextCursor.MoveMode.MoveAnchor)
        if helper.charFormat().isImageFormat() and helper.atBlockStart():
            self._text_cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock, QTextCursor.MoveMode.MoveAnchor)
            self._text_cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)

    def parse_to_html(self, html_text: str) -> str:
        document = QTextDocument()
        helper: QTextCursor = QTextCursor(document)
        helper.insertHtml(html_text)

        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_format: QTextBlockFormat = block.blockFormat()

            new_block_format: QTextBlockFormat = QTextBlockFormat()
            new_block_format.setAlignment(block_format.alignment())
            new_block_format.setHeadingLevel(0)
            new_block_format.setTextIndent(block_format.textIndent())
            new_block_format.setIndent(block_format.indent())
            if block_format.lineHeightType() != 1:
                new_block_format.setLineHeight(1, 1)
            else:
                if block_format.lineHeight() > 5:
                    new_block_format.setLineHeight(block_format.lineHeight() / 100, 1)
                else:
                    new_block_format.setLineHeight(block_format.lineHeight(), 1)
            new_block_format.setTopMargin(block_format.topMargin())
            new_block_format.setBottomMargin(block_format.bottomMargin())
            new_block_format.setLeftMargin(block_format.leftMargin())
            new_block_format.setRightMargin(block_format.rightMargin())

            helper.setPosition(block.position())
            helper.setBlockFormat(new_block_format)

            it: QTextBlock.iterator = block.begin()
            if it != block.end():
                fragment: QTextFragment = it.fragment()

                char_format: QTextCharFormat = fragment.charFormat()
                new_char_format: QTextCharFormat = QTextCharFormat()

                if char_format.isImageFormat():
                    continue

                if char_format.isCharFormat():
                    new_char_format.setFontPointSize(max(char_format.fontPointSize(), 1))
                    if char_format.fontFamilies() is not None:
                        new_char_format.setFontFamilies([char_format.fontFamilies()[0]])
                    else:
                        new_char_format.setFontFamilies(["Segoe UI"])
                    new_char_format.setBackground(char_format.background())
                    new_char_format.setForeground(char_format.foreground())
                    if new_char_format.fontWeight() == QFont.Weight.Bold:
                        weight = QFont.Weight.Bold
                    else:
                        weight = QFont.Weight.Normal
                    new_char_format.setFontWeight(weight)
                    new_char_format.setFontItalic(char_format.fontItalic())
                    if new_char_format.underlineStyle() == QTextCharFormat.UnderlineStyle.SingleUnderline:
                        underline = QTextCharFormat.UnderlineStyle.SingleUnderline
                    else:
                        underline = QTextCharFormat.UnderlineStyle.NoUnderline
                    new_char_format.setUnderlineStyle(underline)

                    helper.setPosition(fragment.position(), QTextCursor.MoveMode.MoveAnchor)
                    helper.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)
                    helper.setCharFormat(new_char_format)

                it += 1

        return document.toHtml()

    def parse_to_plain_text(self, text: str) -> str:
        document = QTextDocument()
        helper: QTextCursor = QTextCursor(document)
        helper.insertText(text)

        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_format: QTextBlockFormat = block.blockFormat()

            new_block_format: QTextBlockFormat = QTextBlockFormat()
            new_block_format.setAlignment(block_format.alignment())
            new_block_format.setHeadingLevel(0)
            new_block_format.setTextIndent(block_format.textIndent())
            new_block_format.setIndent(block_format.indent())
            if block_format.lineHeightType() != 1:
                new_block_format.setLineHeight(1, 1)
            else:
                new_block_format.setLineHeight(max(block_format.lineHeight(), 1), 1)
            new_block_format.setTopMargin(block_format.topMargin())
            new_block_format.setBottomMargin(block_format.bottomMargin())
            new_block_format.setLeftMargin(block_format.leftMargin())
            new_block_format.setRightMargin(block_format.rightMargin())

            helper.setPosition(block.position())
            helper.setBlockFormat(new_block_format)

        return document.toPlainText()
