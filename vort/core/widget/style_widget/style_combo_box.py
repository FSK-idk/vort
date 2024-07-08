from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget

from core.widget.style_widget.style_table_model import StyleTableModel
from core.widget.style_widget.style_table_model import StyleTableModel
from core.widget.basic_widget import ComboBox

from etc.style_data import StyleData
from etc.data_base.data_base import data_base


class StyleComboBox(ComboBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.combo_box_model: StyleTableModel = StyleTableModel(self)

        self.setModel(self.combo_box_model)
        self.setEditable(True)
        self.lineEdit().setEnabled(False)
        self.lineEdit().setPlaceholderText("Style")
        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setFixedWidth(100)

    def style(self) -> StyleData:
        return data_base.selectStyleData(self.currentText())
