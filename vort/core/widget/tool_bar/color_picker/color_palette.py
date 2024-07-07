from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtGui import QColor

from core.widget.tool_bar.color_picker.color_button import ColorButton


class ColorPalette(QWidget):
    colorClicked = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # TODO: add transparent
        # fmt: off
        self.colors: list[list[QColor]] = [
            [QColor("transparent"), QColor("#000000"), QColor("#2B2B2B"), QColor("#555555"), QColor("#808080"), QColor("#AAAAAA"), QColor("#D5D5D5"), QColor("#FFFFFF")],
            [QColor("#FF0000"),     QColor("#FF9900"), QColor("#FFFF00"), QColor("#00FF00"), QColor("#00FFFF"), QColor("#0000FF"), QColor("#9900FF"), QColor("#FF00FF")],
            [QColor("#D90000"),     QColor("#E18400"), QColor("#DDD900"), QColor("#09D000"), QColor("#00CCCC"), QColor("#000DD9"), QColor("#7B00D5"), QColor("#D000CC")],
            [QColor("#B30000"),     QColor("#C46F00"), QColor("#BBB300"), QColor("#11A200"), QColor("#009999"), QColor("#001AB3"), QColor("#5E00AA"), QColor("#A20099")],
            [QColor("#8C0000"),     QColor("#A65900"), QColor("#998C00"), QColor("#1A7300"), QColor("#006666"), QColor("#00268C"), QColor("#400080"), QColor("#730066")],
            [QColor("#660000"),     QColor("#884400"), QColor("#776600"), QColor("#224400"), QColor("#003333"), QColor("#003366"), QColor("#220055"), QColor("#440033")],
        ]
        # fmt: on

        self.buttons: list[ColorButton] = []
        palette_layout: QGridLayout = QGridLayout()
        palette_layout.setContentsMargins(4, 4, 4, 4)
        palette_layout.setSpacing(4)

        for row, color_row in enumerate(self.colors):
            for col, color in enumerate(color_row):
                button: ColorButton = ColorButton()
                button.setColor(color)
                button.colorClicked.connect(self.colorClicked.emit)
                self.buttons.append(button)
                palette_layout.addWidget(button, row, col)

        self.setLayout(palette_layout)
