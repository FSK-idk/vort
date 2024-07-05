from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QDialog, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QLineEdit


class EditHyperlinkDialogContext:
    def __init__(self) -> None:
        self.text: str = ""
        self.hyperlink: str = ""


class EditHyperlinkDialogUI(QDialog):
    def __init__(self, context: EditHyperlinkDialogContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: EditHyperlinkDialogContext = context

        self.setWindowTitle("Edit paragraph")
        self.setMinimumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # hyperlink

        self.hyperlink_title_label: QLabel = QLabel(self)
        self.hyperlink_title_label.setText("Hyperlink")

        self.text_line_edit_label: QLabel = QLabel(self)
        self.text_line_edit_label.setText("Text")

        self.text_line_edit: QLineEdit = QLineEdit(self)
        self.text_line_edit.setText(self.context.text)

        self.hyperlink_line_edit_label: QLabel = QLabel(self)
        self.hyperlink_line_edit_label.setText("Hyperlink")

        self.hyperlink_line_edit: QLineEdit = QLineEdit(self)
        self.hyperlink_line_edit.setText(self.context.hyperlink)

        text_line_edit_layout = QHBoxLayout()
        text_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        text_line_edit_layout.setSpacing(10)
        text_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        text_line_edit_layout.addWidget(self.text_line_edit_label)
        text_line_edit_layout.addWidget(self.text_line_edit)

        hyperlink_line_edit_layout = QHBoxLayout()
        hyperlink_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        hyperlink_line_edit_layout.setSpacing(10)
        hyperlink_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hyperlink_line_edit_layout.addWidget(self.hyperlink_line_edit_label)
        hyperlink_line_edit_layout.addWidget(self.hyperlink_line_edit)

        hyperlink_layout = QVBoxLayout()
        hyperlink_layout.setContentsMargins(0, 0, 0, 0)
        hyperlink_layout.setSpacing(0)
        hyperlink_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        hyperlink_layout.addWidget(self.hyperlink_title_label)
        hyperlink_layout.addSpacing(15)
        hyperlink_layout.addLayout(text_line_edit_layout)
        hyperlink_layout.addSpacing(5)
        hyperlink_layout.addLayout(hyperlink_line_edit_layout)
        hyperlink_layout.addSpacing(5)

        # button

        self.save_button = QPushButton(self)
        self.save_button.setText("Save")
        self.save_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_button.clicked.connect(self.onSaveClicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_button.clicked.connect(self.onCancelClicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)
        self.main_layout.addLayout(hyperlink_layout)
        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

    def onSaveClicked(self) -> None:
        self.context.text = self.text_line_edit.text()
        self.context.hyperlink = self.hyperlink_line_edit.text()

        self.accept()

    def onCancelClicked(self) -> None:
        self.reject()
