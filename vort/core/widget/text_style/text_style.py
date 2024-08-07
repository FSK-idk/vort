from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class TextStyle:
    ALIGNMENT_FLAGS: list[Qt.AlignmentFlag] = [
        Qt.AlignmentFlag.AlignLeft,
        Qt.AlignmentFlag.AlignHCenter,
        Qt.AlignmentFlag.AlignRight,
    ]
    ALIGNMENT_NAMES: list[str] = ["Left", "Center", "Right"]

    def __init__(self) -> None:
        self.name: str = ""

        self.is_font_changed: bool = False
        self.font_family: str = ""
        self.font_size: int = 1
        self.background_color: QColor = QColor()
        self.foreground_color: QColor = QColor()
        self.is_bold: bool = False
        self.is_italic: bool = False
        self.is_underlined: bool = False

        self.is_paragraph_changed: bool = False
        self.alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft
        self.first_line_indent: float = 0.0  # cm
        self.indent: int = 0
        self.line_spacing: float = 1.0  # ratio
        self.top_margin: float = 0.0  # cm
        self.bottom_margin: float = 0.0  # cm
        self.left_margin: float = 0.0  # cm
        self.right_margin: float = 0.0  # cm

    def setData(self, data: list) -> None:
        # fmt:off
        self.name                   = data[0]
        self.is_font_changed        = True if data[1] == 1 else False
        self.font_family            = data[2]
        self.font_size              = data[3]
        self.background_color       = QColor(data[4], data[5], data[6], data[7])
        self.foreground_color       = QColor(data[8], data[9], data[10], data[11])
        self.is_bold                = True if data[12] == 1 else False
        self.is_italic              = True if data[13] == 1 else False
        self.is_underlined          = True if data[14] == 1 else False
        self.is_paragraph_changed   = True if data[15] == 1 else False
        self.alignment              = self.ALIGNMENT_FLAGS[self.ALIGNMENT_NAMES.index(data[16])]
        self.first_line_indent      = data[17]
        self.indent                 = data[18]
        self.line_spacing           = data[19]
        self.top_margin             = data[20]
        self.bottom_margin          = data[21]
        self.left_margin            = data[22]
        self.right_margin           = data[23]
        # fmt:on

    @staticmethod
    def alignmentName(flag: Qt.AlignmentFlag) -> str:
        return TextStyle.ALIGNMENT_NAMES[TextStyle.ALIGNMENT_FLAGS.index(flag)]

    @staticmethod
    def alignmentFlag(name: str) -> Qt.AlignmentFlag:
        return TextStyle.ALIGNMENT_FLAGS[TextStyle.ALIGNMENT_NAMES.index(name)]
