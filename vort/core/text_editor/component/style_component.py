from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextBlockFormat, QTextCursor, QGuiApplication

from core.text_editor.component.component import Component

from etc.style_data import StyleData


class StyleComponent(Component):
    def setFontFamily(self, font_family: str) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamilies([font_family])
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setFontSize(self, font_size: int) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(font_size)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setBackgroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(color)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setForegroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setForeground(color)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def turnBold(self, is_bold: bool) -> None:
        font_weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(font_weight)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def turnItalic(self, is_italic: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontItalic(is_italic)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def turnUnderlined(self, is_underlined: bool) -> None:
        underline = (
            QTextCharFormat.UnderlineStyle.SingleUnderline
            if is_underlined
            else QTextCharFormat.UnderlineStyle.NoUnderline
        )
        format: QTextCharFormat = QTextCharFormat()
        format.setUnderlineStyle(underline)
        self._text_cursor.mergeCharFormat(format)
        if self._text_cursor.atBlockStart() and self._text_cursor.atBlockEnd():
            format = self._text_cursor.charFormat()
            format.setAnchorHref("")
            self._text_cursor.mergeBlockCharFormat(format)
        self.applied.emit()

    def setStyle(self, style_data: StyleData) -> None:
        if not style_data.is_font_changed and not style_data.is_paragraph_changed:
            return

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px = dpi / 2.54

        char_format: QTextCharFormat = QTextCharFormat()
        block_format: QTextBlockFormat = QTextBlockFormat()

        if style_data.is_font_changed:
            char_format.setFontFamilies([style_data.font_family])
            char_format.setFontPointSize(style_data.font_size)
            char_format.setBackground(style_data.background_color)
            char_format.setForeground(style_data.foreground_color)
            char_format.setFontWeight(QFont.Weight.Bold if style_data.is_bold else QFont.Weight.Normal)
            char_format.setFontItalic(style_data.is_italic)
            char_format.setUnderlineStyle(
                QTextCharFormat.UnderlineStyle.SingleUnderline
                if style_data.is_underlined
                else QTextCharFormat.UnderlineStyle.NoUnderline
            )

        if style_data.is_paragraph_changed:
            block_format.setAlignment(style_data.alignment)
            block_format.setTextIndent(style_data.first_line_indent * cm_to_px)
            block_format.setIndent(style_data.indent)
            block_format.setLineHeight(style_data.line_spacing, 1)
            block_format.setTopMargin(style_data.top_margin * cm_to_px)
            block_format.setBottomMargin(style_data.bottom_margin * cm_to_px)
            block_format.setLeftMargin(style_data.left_margin * cm_to_px)
            block_format.setRightMargin(style_data.right_margin * cm_to_px)

        if style_data.is_font_changed and not style_data.is_paragraph_changed:
            self._text_cursor.setCharFormat(char_format)

        if not style_data.is_font_changed and style_data.is_paragraph_changed:
            self._text_cursor.setBlockFormat(block_format)

        if style_data.is_font_changed and style_data.is_paragraph_changed:

            self._text_cursor.selectionStart()
            helper: QTextCursor = QTextCursor(self._text_cursor.document())
            helper.beginEditBlock()
            helper.setPosition(self._text_cursor.selectionStart())
            start_block_number: int = helper.blockNumber()
            helper.setPosition(self._text_cursor.selectionEnd())
            end_block_number: int = helper.blockNumber()

            for i in range(start_block_number, end_block_number + 1):
                block = self._text_cursor.document().findBlockByLineNumber(i)
                helper.setPosition(block.position(), QTextCursor.MoveMode.MoveAnchor)
                helper.setPosition(block.position() + block.length() - 1, QTextCursor.MoveMode.KeepAnchor)
                helper.setCharFormat(char_format)
                helper.setBlockCharFormat(char_format)
                helper.setBlockFormat(block_format)
            helper.endEditBlock()

        self.applied.emit()

    def clearStyle(self) -> None:
        char_format: QTextCharFormat = QTextCharFormat()
        char_format.setFont("Segoe UI")
        char_format.setFontPointSize(16)
        char_format.setBackground(QColor("transparent"))
        char_format.setForeground(QColor("black"))
        char_format.setFontWeight(QFont.Weight.Normal)
        char_format.setFontItalic(False)
        char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)

        block_format: QTextBlockFormat = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
        block_format.setTextIndent(0)
        block_format.setIndent(0)
        block_format.setLineHeight(1, 1)
        block_format.setTopMargin(0)
        block_format.setBottomMargin(0)
        block_format.setLeftMargin(0)
        block_format.setRightMargin(0)

        self._text_cursor.setCharFormat(char_format)
        self._text_cursor.setBlockFormat(block_format)
        if self._text_cursor.selectionStart() == self._text_cursor.block().position():
            self._text_cursor.setBlockCharFormat(char_format)

        self.applied.emit()
