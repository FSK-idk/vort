from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, QEvent

from view.widget.button_color import ButtonColor


class ColorPalette(QWidget):
    hidden = Signal()
    colorSelected = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # fmt: off
        self.colors: list[list[QColor]] = [
            [QColor("#000000"), QColor("#242424"), QColor("#494949"), QColor("#6D6D6D"), QColor("#929292"), QColor("#B6B6B6"), QColor("#DBDBDB"), QColor("#FFFFFF")],
            [QColor("#FF0000"), QColor("#FF9900"), QColor("#FFFF00"), QColor("#00FF00"), QColor("#00FFFF"), QColor("#0000FF"), QColor("#9900FF"), QColor("#FF00FF")],
            [QColor("#D90000"), QColor("#E18400"), QColor("#DDD900"), QColor("#09D000"), QColor("#00CCCC"), QColor("#000DD9"), QColor("#7B00D5"), QColor("#D000CC")],
            [QColor("#B30000"), QColor("#C46F00"), QColor("#BBB300"), QColor("#11A200"), QColor("#009999"), QColor("#001AB3"), QColor("#5E00AA"), QColor("#A20099")],
            [QColor("#8C0000"), QColor("#A65900"), QColor("#998C00"), QColor("#1A7300"), QColor("#006666"), QColor("#00268C"), QColor("#400080"), QColor("#730066")],
            [QColor("#660000"), QColor("#884400"), QColor("#776600"), QColor("#224400"), QColor("#003333"), QColor("#003366"), QColor("#220055"), QColor("#440033")],
        ]
        # fmt: on

        self.buttons: list[QPushButton] = []
        self.main_layout: QGridLayout = QGridLayout()
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(4)

        for row, color_row in enumerate(self.colors):
            for col, color in enumerate(color_row):
                button: ButtonColor = ButtonColor()
                button.setColor(color)
                button.colorClicked.connect(self.colorSelected)
                self.buttons.append(button)
                self.main_layout.addWidget(button, row, col)

        self.setLayout(self.main_layout)
        self.colorSelected.connect(self.hide)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Hide:
            self.hidden.emit()
        return super().event(event)
