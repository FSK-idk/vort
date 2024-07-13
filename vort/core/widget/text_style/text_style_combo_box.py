from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from core.widget.text_style.text_style_table_model import TextStyleTableModel
from core.widget.basic_widget import ComboBox

from core.widget.text_style.text_style import TextStyle
from data_base.data_base import data_base


class TextStyleComboBox(ComboBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.combo_box_model: TextStyleTableModel = TextStyleTableModel(self)

        self.setModel(self.combo_box_model)
        self.setEditable(True)
        self.lineEdit().setEnabled(False)
        self.lineEdit().setPlaceholderText("Style")
        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setFixedWidth(100)

    def style(self) -> TextStyle:
        return data_base.selectTextStyleData(self.currentText())
