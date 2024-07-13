from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtSql import QSqlQuery, QSqlQueryModel

from data_base.data_base import data_base
from data_base.query import Query


class TextStyleTableModel(QSqlQueryModel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ascending: bool = True
        self.search_data: str = ""

        self.updateTable()

        data_base.updatedStyleTable.connect(self.updateTable)

    def setSearchData(self, search_data: str) -> None:
        self.search_data = search_data

    def setSortData(self, order: Qt.SortOrder) -> None:
        self.ascending = order == Qt.SortOrder.AscendingOrder

    @Slot()
    def updateTable(self) -> None:
        query: QSqlQuery = QSqlQuery(data_base.data_base)
        query.prepare(Query.selectTextStyleTable(self.ascending))
        query.bindValue(":name", self.search_data)
        query.exec()
        self.setQuery(query)
        self.setHeaderData(0, Qt.Orientation.Horizontal, "Name")
