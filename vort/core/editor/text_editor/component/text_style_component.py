from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextBlockFormat, QTextCursor, QGuiApplication


from core.widget.text_style.text_style import TextStyle


class TextStyleComponent(QObject):
    repaintRequest: Signal = Signal()

    def __init__(self, cursor: QTextCursor) -> None:
        super().__init__()
        self.__cursor: QTextCursor = cursor

        self.__default_char_format: QTextCharFormat = QTextCharFormat()
        self.__default_char_format.setFont("Segoe UI")
        self.__default_char_format.setFontPointSize(16)
        self.__default_char_format.setBackground(QColor("transparent"))
        self.__default_char_format.setForeground(QColor("black"))
        self.__default_char_format.setFontWeight(QFont.Weight.Normal)
        self.__default_char_format.setFontItalic(False)
        self.__default_char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)

        self.__default_block_format: QTextBlockFormat = QTextBlockFormat()
        self.__default_block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__default_block_format.setTextIndent(0)
        self.__default_block_format.setIndent(0)
        self.__default_block_format.setLineHeight(1, 1)
        self.__default_block_format.setTopMargin(0)
        self.__default_block_format.setBottomMargin(0)
        self.__default_block_format.setLeftMargin(0)
        self.__default_block_format.setRightMargin(0)

    def setTextStyle(self, style_data: TextStyle) -> None:
        if not style_data.is_font_changed and not style_data.is_paragraph_changed:
            return

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()
        cm_to_px = dpi / 2.54

        if style_data.is_font_changed:
            char_format: QTextCharFormat = QTextCharFormat()
            char_format.setFontFamilies([style_data.font_family])
            char_format.setFontPointSize(style_data.font_size)
            char_format.setBackground(style_data.background_color)
            char_format.setForeground(style_data.foreground_color)
            char_format.setFontWeight(QFont.Weight.Bold if style_data.is_bold else QFont.Weight.Normal)
            char_format.setFontItalic(style_data.is_italic)
            char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline if style_data.is_underlined else QTextCharFormat.UnderlineStyle.NoUnderline)  # type: ignore

        if style_data.is_font_changed and not style_data.is_paragraph_changed:
            self.__cursor.setCharFormat(char_format)

            selection_start: int = self.__cursor.selectionStart()

            helper: QTextCursor = QTextCursor(self.__cursor.document())
            helper.setPosition(selection_start)

            if helper.atBlockStart():
                helper.mergeBlockCharFormat(helper.charFormat())

        if style_data.is_paragraph_changed:
            block_format: QTextBlockFormat = QTextBlockFormat()
            block_format.setAlignment(style_data.alignment)
            block_format.setTextIndent(style_data.first_line_indent * cm_to_px)
            block_format.setIndent(style_data.indent)
            block_format.setLineHeight(style_data.line_spacing, 1)
            block_format.setTopMargin(style_data.top_margin * cm_to_px)
            block_format.setBottomMargin(style_data.bottom_margin * cm_to_px)
            block_format.setLeftMargin(style_data.left_margin * cm_to_px)
            block_format.setRightMargin(style_data.right_margin * cm_to_px)

        if not style_data.is_font_changed and style_data.is_paragraph_changed:
            self.__cursor.setBlockFormat(block_format)

        if style_data.is_font_changed and style_data.is_paragraph_changed:
            helper: QTextCursor = QTextCursor(self.__cursor.document())

            helper.beginEditBlock()

            helper.setPosition(self.__cursor.selectionStart())
            start_block_number: int = helper.blockNumber()
            helper.setPosition(self.__cursor.selectionEnd())
            end_block_number: int = helper.blockNumber()

            for i in range(start_block_number, end_block_number + 1):
                block = self.__cursor.document().findBlockByLineNumber(i)
                helper.setPosition(block.position(), QTextCursor.MoveMode.MoveAnchor)
                helper.setPosition(block.position() + block.length() - 1, QTextCursor.MoveMode.KeepAnchor)
                helper.setCharFormat(char_format)
                helper.setBlockCharFormat(char_format)
                helper.setBlockFormat(block_format)

            helper.endEditBlock()

        self.repaintRequest.emit()

    def clearTextStyle(self) -> None:
        if not self.__cursor.hasSelection():
            return

        selection_start = self.__cursor.selectionStart()
        selection_end = self.__cursor.selectionEnd()

        helper: QTextCursor = QTextCursor(self.__cursor.document())

        helper.setPosition(selection_start)
        start_block_number: int = helper.blockNumber()
        is_block_start: int = helper.atBlockStart()
        helper.setPosition(selection_end)
        end_block_number: int = helper.blockNumber()
        is_block_end: int = helper.atBlockEnd()

        if start_block_number == end_block_number and not (is_block_start and is_block_end):
            self.__cursor.setCharFormat(self.__default_char_format)

        else:
            self.__cursor.setCharFormat(self.__default_char_format)
            self.__cursor.setBlockCharFormat(self.__default_char_format)
            self.__cursor.setBlockFormat(self.__default_block_format)

        self.repaintRequest.emit()
