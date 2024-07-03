from PySide6.QtCore import Qt, QMimeData, QUrl
from PySide6.QtGui import (
    QTextCursor,
    QGuiApplication,
    QKeyEvent,
    QTextBlock,
    QTextFragment,
    QTextImageFormat,
    QImage,
    QColor,
    QTextDocument,
    QTextDocumentFragment,
)

from util.point_f import PointF

from core.widget.text_editor.component.component import Component
from core.widget.text_editor.text_canvas import TextCanvas


img_count = 0


class InputComponent(Component):
    def cut(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QGuiApplication.clipboard().setMimeData(mime_data)
            self.text_cursor.removeSelectedText()
            self.applied.emit()

    def copy(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QGuiApplication.clipboard().setMimeData(mime_data)
            self.applied.emit()

    # fmt:off
    def paste(self) -> None:
        global img_count
        mime_data = QGuiApplication.clipboard().mimeData()
        if mime_data.hasImage():
            url: QUrl = QUrl(f"pasted_image_{img_count}")
            image: QImage = QImage(mime_data.imageData())
            img_count += 1

            if not image.isNull():
                # TODO: check for start
                self.text_cursor.document().addResource(QTextDocument.ResourceType.ImageResource, url, image)

                imageFormat: QTextImageFormat = QTextImageFormat()
                imageFormat.setWidth(image.width())
                imageFormat.setHeight(image.height())
                imageFormat.setName(url.toString())
                imageFormat.setForeground(QColor("black"))
                imageFormat.setBackground(QColor("white"))

                print(imageFormat.toCharFormat().isImageFormat())

                prev_format = self.text_cursor.charFormat()
                self.text_cursor.setCharFormat(imageFormat.toCharFormat())
                self.text_cursor.insertImage(imageFormat)
                self.text_cursor.setCharFormat(prev_format)
            else:
                print("no image")

        elif mime_data.hasHtml():
            print("html:", mime_data.html())
            self.text_cursor.insertFragment(QTextDocumentFragment.fromHtml(mime_data.html()))
        else:
            self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))

        self.fixup()
        self.applied.emit()

    def pastePlain(self) -> None:
        mime_data = QGuiApplication.clipboard().mimeData()
        self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.applied.emit()

    def input(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.text():
            match event.key():
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete if not self.text_cursor.hasSelection():
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor)
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case _:
                    return
            self.applied.emit()

        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier]:
            match event.key():
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Enter:
                    return  # ignore
                case Qt.Key.Key_Escape:
                    return  # ignore
                case _ if event.text():
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertText(event.text())
                    self.text_cursor.endEditBlock()
            self.fixup()
            self.applied.emit()

    def fixup(self) -> None:
        # position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha
        images: list[tuple[int, bool, bool, bool, bool]] = []

        for i in range(self.text_cursor.document().blockCount()):
            block: QTextBlock = self.text_cursor.document().findBlockByNumber(i)

            it: QTextBlock.iterator = block.begin()
            while it != block.end():
                frag: QTextFragment = it.fragment()

                if frag.charFormat().isImageFormat():
                    form: QTextImageFormat = frag.charFormat().toImageFormat()

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

        offset_position = 0
        helper = QTextCursor(self.text_cursor.document())

        for position, is_pref_empty, is_pref_alpha, is_pref_img, is_suff_alpha in images:
            helper.beginEditBlock()
            if is_pref_alpha or is_pref_img:
                helper.setPosition(position + offset_position)
                helper.insertBlock()
                offset_position += 1
            if is_suff_alpha:
                helper.setPosition(position + offset_position + 1)
                helper.insertBlock()
                offset_position += 1
            helper.endEditBlock()
