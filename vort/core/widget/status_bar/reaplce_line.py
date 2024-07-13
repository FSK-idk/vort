from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap


import resource.resource_rc


class ReplaceLine(QWidget):
    replaceRequest: Signal = Signal()
    replaceAllRequest: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.replace_line: QLineEdit = QLineEdit(self)
        self.replace_line.setPlaceholderText("Replace")
        self.replace_line.returnPressed.connect(self.onReplacePressed)

        self.replace_button: QPushButton = QPushButton(self)
        self.replace_button.setIcon(QPixmap(":/icon/replace.svg"))
        self.replace_button.setToolTip("Replace")
        self.replace_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.replace_button.clicked.connect(self.onReplacePressed)

        self.replace_all_button: QPushButton = QPushButton(self)
        self.replace_all_button.setIcon(QPixmap(":/icon/replace_all.svg"))
        self.replace_all_button.setToolTip("Replace all")
        self.replace_all_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.replace_all_button.clicked.connect(self.onReplaceAllClicked)

        # layout

        reaplace_layout: QHBoxLayout = QHBoxLayout()
        reaplace_layout.setContentsMargins(0, 0, 0, 0)
        reaplace_layout.setSpacing(2)
        reaplace_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        reaplace_layout.addWidget(self.replace_line)
        reaplace_layout.addWidget(self.replace_button)
        reaplace_layout.addWidget(self.replace_all_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        main_layout.addLayout(reaplace_layout)

        self.setLayout(main_layout)

    def replaceData(self) -> str:
        return self.replace_line.text()

    @Slot()
    def onReplacePressed(self) -> None:
        self.replaceRequest.emit()

    @Slot()
    def onReplaceAllClicked(self) -> None:
        self.replaceAllRequest.emit()
