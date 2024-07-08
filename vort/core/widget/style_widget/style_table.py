from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QTableView, QAbstractItemView, QHeaderView

from core.widget.style_widget.style_table_model import StyleTableModel


class StyleTable(QTableView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_table_model: StyleTableModel = StyleTableModel()

        self.setSortingEnabled(True)
        self.setModel(self.style_table_model)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.horizontalHeader().sortIndicatorChanged.connect(self.sort)

    @Slot()
    def sort(self, index: int, order: Qt.SortOrder) -> None:
        self.style_table_model.setSortData(order)
        self.style_table_model.updateTable()

    def search(self, search_data: str) -> None:
        self.style_table_model.setSearchData(search_data)
        self.style_table_model.updateTable()
