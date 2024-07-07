from typing import Self

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextDocument, QTextCursor, QTextCharFormat, QTextBlockFormat, QFont


class DocumentFile:
    def __init__(self) -> None:
        self.html_text: str = ""

        # page

        self.page_width: float = 0.0  # cm
        self.page_height: float = 0.0  # cm
        self.page_spacing: float = 0.0  # cm

        self.page_color: QColor = QColor("black")

        self.page_top_margin: float = 0.0  # cm
        self.page_bottom_margin: float = 0.0  # cm
        self.page_left_margin: float = 0.0  # cm
        self.page_right_margin: float = 0.0  # cm

        self.page_top_padding: float = 0.0  # cm
        self.page_bottom_padding: float = 0.0  # cm
        self.page_left_padding: float = 0.0  # cm
        self.page_right_padding: float = 0.0  # cm

        self.border_width: float = 0.0  # mm
        self.border_color: QColor = QColor("black")

        self.header_height: float = 0.0  # cm
        self.footer_height: float = 0.0  # cm

        # indent step

        self.default_indent_step: float = 0.0  # cm

        # header

        self.header_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

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

        self.footer_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom

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

    @classmethod
    def default_file(cls) -> Self:
        file: Self = cls()

        file.html_text = ""
        file.page_width = 21
        file.page_height = 29.7
        file.page_spacing = 1
        file.page_color = QColor("white")
        file.page_top_margin = 1
        file.page_bottom_margin = 1
        file.page_left_margin = 1
        file.page_right_margin = 1
        file.page_top_padding = 1
        file.page_bottom_padding = 1
        file.page_left_padding = 1
        file.page_right_padding = 1
        file.border_width = 0
        file.border_color = QColor("black")
        file.header_height = 0.0
        file.footer_height = 0.0
        file.default_indent_step = 1
        file.header_alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        file.header_font_family = "Segoe UI"
        file.header_font_size = 16
        file.header_text_background_color = QColor("transparent")
        file.header_text_foreground_color = QColor("black")
        file.is_header_turned_for_first_page = True
        file.is_header_pagination_turned = False
        file.header_pagination_starting_number = 1
        file.is_header_text_turned = False
        file.header_text = ""
        file.footer_alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        file.footer_font_family = "Segoe UI"
        file.footer_font_size = 16
        file.footer_text_background_color = QColor("transparent")
        file.footer_text_foreground_color = QColor("black")
        file.is_footer_turned_for_first_page = True
        file.is_footer_pagination_turned = False
        file.footer_pagination_starting_number = 1
        file.is_footer_text_turned = False
        file.footer_text = ""
        file.is_hyperlink_bold_turned = False
        file.is_hyperlink_bold = False
        file.is_hyperlink_italic_turned = False
        file.is_hyperlink_italic = False
        file.is_hyperlink_underlined_turned = True
        file.is_hyperlink_underlined = True
        file.is_hyperlink_background_color_turned = False
        file.hyperlink_background_color = QColor("transparent")
        file.is_hyperlink_foreground_color_turned = True
        file.hyperlink_foreground_color = QColor("blue")

        return file
