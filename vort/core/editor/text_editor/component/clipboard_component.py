import hashlib

from PySide6.QtCore import Signal, QObject, QMimeData, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import (
    QTextDocument,
    QTextCursor,
    QGuiApplication,
    QImage,
    QTextImageFormat,
    QTextBlock,
    QTextBlockFormat,
    QTextCharFormat,
    QColor,
    QTextFragment,
    QFont,
    QTextDocumentFragment,
)


class ClipboardComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

    def cut(self) -> None:
        if self.__cursor.hasSelection():
            self.__cursor.beginEditBlock()

            selection: QTextDocumentFragment = self.__cursor.selection()
            mime_data: QMimeData = QMimeData()
            mime_data.setHtml(selection.toHtml())
            mime_data.setText(selection.toPlainText())
            QGuiApplication.clipboard().setMimeData(mime_data)

            self.__cursor.removeSelectedText()

            if self.__cursor.atBlockStart() and not self.__cursor.charFormat().isImageFormat():
                self.__cursor.setBlockCharFormat(self.__cursor.charFormat())

            self.fixupImage()
            self.__cursor.endEditBlock()

            self.repaintRequest.emit()

    def copy(self) -> None:
        if self.__cursor.hasSelection():
            selection = self.__cursor.selection()
            mime_data: QMimeData = QMimeData()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QGuiApplication.clipboard().setMimeData(mime_data)

    def paste(self) -> None:
        if self.pasteImage():
            return
        if self.pasteText():
            return
        if self.pastePlain():
            return

    def pasteText(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()

        if not mime_data.hasHtml():
            return False

        self.__cursor.beginEditBlock()

        is_block_start: bool = False

        selection_start = self.__cursor.selectionStart()
        helper: QTextCursor = QTextCursor(self.__cursor.document())
        helper.setPosition(selection_start)

        if helper.atBlockStart():
            is_block_start = True

        self.__cursor.insertHtml(self.parseHtml(mime_data.html()))

        if is_block_start:
            helper.setPosition(selection_start)
            block_char_format = helper.charFormat()
            block_char_format.setAnchorHref("")
            self.__cursor.mergeBlockCharFormat(block_char_format)

        self.fixupImage()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

        return True

    def pastePlain(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()

        if not mime_data.hasText():
            return False

        self.__cursor.beginEditBlock()

        is_block_start: bool = False

        selection_start = self.__cursor.selectionStart()
        helper: QTextCursor = QTextCursor(self.__cursor.document())
        helper.setPosition(selection_start)

        if helper.atBlockStart():
            is_block_start = True

        self.__cursor.insertText(self.parsePlainText(mime_data.text()))

        if is_block_start:
            helper.setPosition(selection_start)
            block_char_format = helper.charFormat()
            block_char_format.setAnchorHref("")
            self.__cursor.mergeBlockCharFormat(block_char_format)

        self.fixupImage()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

        return True

    def pasteImage(self) -> bool:
        mime_data = QGuiApplication.clipboard().mimeData()

        if not mime_data.hasImage():
            return False

        self.__cursor.beginEditBlock()

        image: QImage = QImage(mime_data.imageData())

        bytes_array: QByteArray = QByteArray()
        buffer: QBuffer = QBuffer(bytes_array)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "png")
        image_bytes: bytes = bytes_array.data()

        name: str = f"pasted_image_{hashlib.sha256(image_bytes).hexdigest()}"

        self.__cursor.document().addResource(QTextDocument.ResourceType.ImageResource, name, image)

        image_format: QTextImageFormat = QTextImageFormat()
        image_format.setWidth(image.width())
        image_format.setHeight(image.height())
        image_format.setName(name)
        image_format.setForeground(QColor("black"))
        image_format.setBackground(QColor("transparent"))

        self.__cursor.insertImage(image_format)

        self.fixupImage()

        helper: QTextCursor = QTextCursor(self.__cursor.document())
        if self.__cursor.position() > 1:
            helper.setPosition(self.__cursor.position() - 1)
        if (
            helper.atBlockEnd()
            and helper.charFormat().isImageFormat()
            and self.__cursor.atBlockStart()
            and self.__cursor.charFormat().isCharFormat()
        ):
            "ok"
            self.__cursor.setPosition(helper.position())

        elif (
            helper.atBlockEnd()
            and helper.charFormat().isCharFormat()
            and self.__cursor.atBlockStart()
            and self.__cursor.charFormat().isImageFormat()
        ):
            self.__cursor.setPosition(helper.position())

        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

        return True

    def insertImage(self, image: QImage) -> None:
        if image.isNull():
            return

        self.__cursor.beginEditBlock()

        bytes_array: QByteArray = QByteArray()
        buffer: QBuffer = QBuffer(bytes_array)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "png")
        image_bytes: bytes = bytes_array.data()

        name: str = f"pasted_image_{hashlib.sha256(image_bytes).hexdigest()}"

        self.__cursor.document().addResource(QTextDocument.ResourceType.ImageResource, name, image)

        image_format: QTextImageFormat = QTextImageFormat()
        image_format.setWidth(image.width())
        image_format.setHeight(image.height())
        image_format.setName(name)
        image_format.setForeground(QColor("black"))
        image_format.setBackground(QColor("transparent"))

        self.__cursor.insertImage(image_format)

        self.fixupImage()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def insertHyperlink(self, text: str, hyperlink: str) -> None:
        if text == "" and not self.__cursor.hasSelection():
            return

        self.__cursor.beginEditBlock()

        format = self.__cursor.charFormat()
        format.setAnchorHref(hyperlink)

        self.__cursor.insertText(text, format)

        self.fixupImage()
        self.__cursor.endEditBlock()

        self.repaintRequest.emit()

    def parseHtml(self, html_text: str) -> str:
        document = QTextDocument()
        helper: QTextCursor = QTextCursor(document)
        helper.insertHtml(html_text)

        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_format: QTextBlockFormat = block.blockFormat()

            new_block_format: QTextBlockFormat = QTextBlockFormat()
            new_block_format.setAlignment(block_format.alignment())
            new_block_format.setTextIndent(block_format.textIndent())
            new_block_format.setIndent(block_format.indent())

            if block_format.lineHeightType() != 1:
                new_block_format.setLineHeight(1, 1)
            elif block_format.lineHeight() > 5:
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

                if char_format.isImageFormat():
                    image: QImage | None = self.__cursor.document().resource(
                        QTextDocument.ResourceType.ImageResource, char_format.toImageFormat().name()
                    )
                    if image is None:
                        new_char_format: QTextCharFormat = QTextCharFormat()
                        helper.setPosition(fragment.position(), QTextCursor.MoveMode.MoveAnchor)
                        helper.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)
                        helper.setCharFormat(new_char_format)
                    continue

                if char_format.isCharFormat():
                    new_char_format: QTextCharFormat = QTextCharFormat()

                    if char_format.fontPointSize() < 1:
                        new_char_format.setFontPointSize(16)
                    else:
                        new_char_format.setFontPointSize(char_format.fontPointSize())

                    if char_format.fontFamilies() is not None:
                        new_char_format.setFontFamilies([char_format.fontFamilies()[0]])
                    else:
                        new_char_format.setFontFamilies(["Segoe UI"])

                    new_char_format.setForeground(char_format.foreground())
                    new_char_format.setBackground(char_format.background())

                    if char_format.fontWeight() == QFont.Weight.Bold:
                        new_char_format.setFontWeight(QFont.Weight.Bold)
                    else:
                        new_char_format.setFontWeight(QFont.Weight.Normal)

                    new_char_format.setFontItalic(char_format.fontItalic())

                    if char_format.underlineStyle() == QTextCharFormat.UnderlineStyle.SingleUnderline:
                        new_char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
                    else:
                        new_char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)

                    helper.setPosition(fragment.position(), QTextCursor.MoveMode.MoveAnchor)
                    helper.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)
                    helper.setCharFormat(new_char_format)

                it += 1

        return document.toHtml()

    def parsePlainText(self, text: str) -> str:
        document = QTextDocument()
        helper: QTextCursor = QTextCursor(document)
        helper.insertText(text)

        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_format: QTextBlockFormat = block.blockFormat()

            new_block_format: QTextBlockFormat = QTextBlockFormat()
            new_block_format.setAlignment(block_format.alignment())
            new_block_format.setTextIndent(block_format.textIndent())
            new_block_format.setIndent(block_format.indent())

            if block_format.lineHeightType() != 1:
                new_block_format.setLineHeight(1, 1)
            elif block_format.lineHeight() > 5:
                new_block_format.setLineHeight(block_format.lineHeight() / 100, 1)
            else:
                new_block_format.setLineHeight(block_format.lineHeight(), 1)

            new_block_format.setTopMargin(block_format.topMargin())
            new_block_format.setBottomMargin(block_format.bottomMargin())
            new_block_format.setLeftMargin(block_format.leftMargin())
            new_block_format.setRightMargin(block_format.rightMargin())

            helper.setPosition(block.position())
            helper.setBlockFormat(new_block_format)

        return document.toPlainText()

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

        helper: QTextCursor = QTextCursor(self.__cursor.document())

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

                last_char_format = helper.blockCharFormat()

                helper.insertBlock()

                helper.setBlockCharFormat(last_char_format)

                offset += 1

            helper.endEditBlock()

        if is_case_4:
            self.__cursor.setPosition(self.__cursor.position() - 1)
