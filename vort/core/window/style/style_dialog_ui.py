from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox

from core.widget.text_style.text_style_table import TextStyleTable
from core.window.style.new_style_dialog_ui import NewStyleDialogUI
from core.window.style.modify_style_dialog_ui import ModifyStyleDialogUI

from data_base.data_base import data_base


class StyleDialogUI(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Style")
        self.resize(650, 400)

        self.search_line: QLineEdit = QLineEdit(self)
        self.search_line.setPlaceholderText("Search...")

        self.style_table: TextStyleTable = TextStyleTable()
        self.search_line.textChanged.connect(self.style_table.search)

        self.new_button: QPushButton = QPushButton(self)
        self.new_button.setText("New")
        self.new_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.new_button.clicked.connect(self.onNewClicked)

        self.modify_button: QPushButton = QPushButton(self)
        self.modify_button.setText("Modify")
        self.modify_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.modify_button.clicked.connect(self.onModifyClicked)

        self.delete_button: QPushButton = QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.delete_button.clicked.connect(self.onDeleteClicked)

        self.close_button: QPushButton = QPushButton(self)
        self.close_button.setText("Close")
        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        main_layout.addWidget(self.search_line)
        main_layout.addWidget(self.style_table)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    @Slot()
    def onNewClicked(self) -> None:
        dialog: NewStyleDialogUI = NewStyleDialogUI(self)
        dialog.exec()

    @Slot()
    def onModifyClicked(self) -> None:
        if self.style_table.selectedIndexes():
            name = self.style_table.selectedIndexes()[0].data()

            dialog: ModifyStyleDialogUI = ModifyStyleDialogUI(name, self)
            dialog.exec()

    @Slot()
    def onDeleteClicked(self) -> None:
        if self.style_table.selectedIndexes():
            name = self.style_table.selectedIndexes()[0].data()

            message = QMessageBox(
                QMessageBox.Icon.Warning,
                "Deletion",
                f'Are you sure you want to delete "{name}" style?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                self,
            )

            if message.exec() == QMessageBox.StandardButton.Yes:
                data_base.deleteTextStyle(name)

    @Slot()
    def onCloseClicked(self) -> None:
        self.reject()
