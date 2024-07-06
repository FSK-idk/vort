from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextDocument


class DocumentFile:
    def __init__(self) -> None:
        self.text_document: QTextDocument = QTextDocument()

        # page

        self.page_width: float = 0.0
        self.page_height: float = 0.0
        self.page_spacing: float = 0.0

        self.page_color: QColor = QColor("black")

        self.page_top_margin: float = 0.0
        self.page_bottom_margin: float = 0.0
        self.page_left_margin: float = 0.0
        self.page_right_margin: float = 0.0

        self.page_top_padding: float = 0.0
        self.page_bottom_padding: float = 0.0
        self.page_left_padding: float = 0.0
        self.page_right_padding: float = 0.0

        self.border_width: float = 0.0
        self.border_color: QColor = QColor("black")

        self.header_height: float = 0.0
        self.footer_height: float = 0.0

        # indent step

        self.default_indent_step: float = 0.0

        # header

        self.header_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft

        self.header_font_family: str = ""
        self.header_font_size: int = 1

        self.header_text_background_color: QColor = QColor("black")
        self.header_text_foreground_color: QColor = QColor("black")

        self.is_header_turned_for_first_page: bool = False

        self.is_header_pagination_turned: bool = False
        self.header_pagination_starting_number: int = 0

        self.is_header_text_turned: bool = False
        self.header_text: str = ""

        # footer

        self.footer_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft

        self.footer_font_family: str = ""
        self.footer_font_size: int = 1

        self.footer_text_background_color: QColor = QColor("black")
        self.footer_text_foreground_color: QColor = QColor("black")

        self.is_footer_turned_for_first_page: bool = False

        self.is_footer_pagination_turned: bool = False
        self.footer_pagination_starting_number: int = 0

        self.is_footer_text_turned: bool = False
        self.footer_text: str = ""

        # hyperlink

        self.is_hyperlink_bold_turned: bool = False
        self.is_hyperlink_bold: bool = False

        self.is_hyperlink_italic_turned: bool = False
        self.is_hyperlink_italic: bool = False

        self.is_hyperlink_underlined_turned: bool = False
        self.is_hyperlink_underlined: bool = False

        self.is_hyperlink_background_color_turned: bool = False
        self.hyperlink_background_color: QColor = QColor("black")
        self.is_hyperlink_foreground_color_turned: bool = False
        self.hyperlink_foreground_color: QColor = QColor("black")
