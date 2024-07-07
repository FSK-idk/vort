from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
)

from core.widget.style_table.style_table import StyleTable


class StyleDialogUI(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Style")
        self.resize(650, 400)

        self.search_line: QLineEdit = QLineEdit(self)

        self.search_button: QPushButton = QPushButton(self)
        self.search_button.setText("Search")
        self.search_button.setFixedWidth(70)
        self.search_button.clicked.connect(self.onSearchClicked)

        search_layout: QHBoxLayout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)
        search_layout.addWidget(self.search_line)
        search_layout.addWidget(self.search_button)

        self.style_table: StyleTable = StyleTable()

        self.new_button: QPushButton = QPushButton(self)
        self.new_button.setText("New")
        self.new_button.setFixedWidth(70)
        self.new_button.clicked.connect(self.onNewClicked)

        self.modify_button: QPushButton = QPushButton(self)
        self.modify_button.setText("Modify")
        self.modify_button.setFixedWidth(70)
        self.modify_button.clicked.connect(self.onModifyClicked)

        self.delete_button: QPushButton = QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.setFixedWidth(70)
        self.delete_button.clicked.connect(self.onDeleteClicked)

        self.close_button: QPushButton = QPushButton(self)
        self.close_button.setText("Close")
        self.close_button.setFixedWidth(70)
        self.close_button.clicked.connect(self.onCloseClicked)

        button_layout: QHBoxLayout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.style_table)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    @Slot()
    def onSearchClicked(self) -> None:
        pass

    @Slot()
    def onNewClicked(self) -> None:
        pass

    @Slot()
    def onModifyClicked(self) -> None:
        pass

    @Slot()
    def onDeleteClicked(self) -> None:
        pass

    @Slot()
    def onCloseClicked(self) -> None:
        self.close()
