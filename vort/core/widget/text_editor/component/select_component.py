from PySide6.QtGui import QTextCursor, QTextBlock, QTextFragment

from core.widget.text_editor.component.component import Component
from core.widget.text_editor.layout.text_document_layout import HitResult, Hit

from util.point_f import PointF


class HyperlinkSelection:
    def __init__(self) -> None:
        self.text: str = ""
        self.hyperlink: str = ""
        self.start: int = 0
        self.end: int = 0


class SelectComponent(Component):
    def selectedText(self) -> str:
        return self._text_cursor.selectedText()

    def selectedHyperlink(self) -> HyperlinkSelection:  # text, hyperlink
        result: HyperlinkSelection = HyperlinkSelection()

        if self._text_cursor.hasSelection():
            selection_start = self._text_cursor.selectionStart()
            selection_end = self._text_cursor.selectionEnd()

            selections: list[HyperlinkSelection] = []

            helper: QTextCursor = QTextCursor(self._text_cursor.document())
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
                        selection.text = helper.selectedText()
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
                        selection.text = helper.selectedText()
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
                        selection.text = helper.selectedText()
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
                        selection.text = helper.selectedText()
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
                    if need_hyperlink and (prev_position == selection_start or result.hyperlink == selection.hyperlink):
                        result.hyperlink = selection.hyperlink

                    else:
                        need_hyperlink = False
                        result.hyperlink = ""

                    prev_position = selection.end

                else:
                    break

            if prev_position == selection_end:
                result.text = self._text_cursor.selectedText()

        else:
            result.hyperlink = self._text_cursor.charFormat().anchorHref()

            if not result.hyperlink == "":
                block = self._text_cursor.block()
                it: QTextBlock.iterator = block.begin()

                while it != block.end():
                    fragment: QTextFragment = it.fragment()

                    if fragment.contains(self._text_cursor.position()):
                        if fragment.charFormat().anchorHref() != "":
                            self._text_cursor.setPosition(fragment.position())
                            self._text_cursor.setPosition(
                                fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor
                            )

                        else:
                            result.hyperlink = ""

                        break

                    it += 1

                result.text = self._text_cursor.selectedText()

        self.applied.emit()

        return result

    def selectAll(self) -> None:
        self._text_cursor.select(QTextCursor.SelectionType.Document)
        self.applied.emit()

    def selectWord(self, result: HitResult) -> None:
        if result.hit in [Hit.Text, Hit.Hyperlink]:
            self._text_cursor.setPosition(result.position, QTextCursor.MoveMode.MoveAnchor)
            self._text_cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self.applied.emit()
