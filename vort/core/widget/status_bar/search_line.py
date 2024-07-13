from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout


class SearchLine(QWidget):
    findRequest: Signal = Signal()
    caseTurned: Signal = Signal(bool)
    wholeTurned: Signal = Signal(bool)
    regexTurned: Signal = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.find_line: QLineEdit = QLineEdit(self)
        self.find_line.textChanged.connect(self.onFindChanged)
        self.find_line.editingFinished.connect(self.onFindEditingFinished)

        self.case_button: QPushButton = QPushButton(self)
        self.case_button.setCheckable(True)
        self.case_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.case_button.setText("A")
        self.case_button.clicked.connect(self.onCaseClicked)

        self.whole_button: QPushButton = QPushButton(self)
        self.whole_button.setCheckable(True)
        self.whole_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.whole_button.setText("_")
        self.whole_button.clicked.connect(self.onWholeClicked)

        self.regex_button: QPushButton = QPushButton(self)
        self.regex_button.setCheckable(True)
        self.regex_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.regex_button.setText("*")
        self.regex_button.clicked.connect(self.onRegexClicked)

        # layout

        find_line_layout: QHBoxLayout = QHBoxLayout()
        find_line_layout.setContentsMargins(0, 0, 0, 0)
        find_line_layout.setSpacing(10)
        find_line_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        find_line_layout.addWidget(self.find_line)
        find_line_layout.addWidget(self.case_button)
        find_line_layout.addWidget(self.whole_button)
        find_line_layout.addWidget(self.regex_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        main_layout.addLayout(find_line_layout)

        self.setLayout(main_layout)

    def searchData(self) -> str:
        return self.find_line.text()

    @Slot(str)
    def onFindChanged(self, search_data: str) -> None:
        self.findRequest.emit()

    @Slot()
    def onFindEditingFinished(self) -> None:
        self.findRequest.emit()

    @Slot(bool)
    def setCaseTurned(self, is_turned: bool) -> None:
        self.case_button.setChecked(is_turned)

    @Slot(bool)
    def setWholeTurned(self, is_turned: bool) -> None:
        self.whole_button.setChecked(is_turned)

    @Slot(bool)
    def setRegexTurned(self, is_turned: bool) -> None:
        self.regex_button.setChecked(is_turned)

    @Slot(bool)
    def onCaseClicked(self, checked: bool) -> None:
        self.caseTurned.emit(checked)

    @Slot(bool)
    def onWholeClicked(self, checked: bool) -> None:
        self.wholeTurned.emit(checked)

    @Slot(bool)
    def onRegexClicked(self, checked: bool) -> None:
        self.regexTurned.emit(checked)
