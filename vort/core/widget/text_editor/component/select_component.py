from PySide6.QtGui import QTextCursor, QTextBlock, QTextFragment

from core.widget.text_editor.component.component import Component


class SelectComponent(Component):
    def selectedText(self) -> str:
        return self._text_cursor.selectedText()

    def selectedHyperlink(self) -> tuple[str, str]:  # text, hyperlink
        text = ""
        hyperlink = ""

        if self._text_cursor.hasSelection():
            selection_start = self._text_cursor.selectionStart()
            selection_end = self._text_cursor.selectionEnd()

            block = self._text_cursor.block()
            it: QTextBlock.iterator = block.begin()

            while it != block.end():
                fragment: QTextFragment = it.fragment()

                if (
                    fragment.charFormat().anchorHref() != ""
                    and selection_start >= fragment.position()
                    and selection_end <= fragment.position() + fragment.length()
                ):
                    hyperlink = fragment.charFormat().anchorHref()
                    break

                it += 1

            text = self._text_cursor.selectedText()

        else:
            format = self._text_cursor.charFormat()
            hyperlink = format.anchorHref()

            if not hyperlink == "":
                block = self._text_cursor.block()
                it: QTextBlock.iterator = block.begin()

                while it != block.end():
                    fragment: QTextFragment = it.fragment()

                    if fragment.contains(self._text_cursor.position()):
                        self._text_cursor.setPosition(fragment.position())
                        self._text_cursor.setPosition(
                            fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor
                        )
                        break

                    it += 1

                text = self._text_cursor.selectedText()

        return (text, hyperlink)

    def selectAll(self) -> None:
        self._text_cursor.select(QTextCursor.SelectionType.Document)
        self.applied.emit()
