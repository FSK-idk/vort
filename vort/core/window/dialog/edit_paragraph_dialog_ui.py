from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QDialog,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
    QDoubleSpinBox,
    QComboBox,
    QSpinBox,
)


class EditParagraphDialogContext:
    def __init__(self) -> None:
        self.alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        self.heading_level: int = 0
        self.is_first_line_indent_turned: bool = False
        self.first_line_indent: float = 0.0  # cm
        self.indent: int = 0  # cm
        self.line_spacing: float = 1.0  # ratio
        self.top_margin: float = 0.0  # cm
        self.bottom_margin: float = 0.0  # cm
        self.left_margin: float = 0.0  # cm
        self.right_margin: float = 0.0  # cm


class EditParagraphDialogUI(QDialog):
    def __init__(self, context: EditParagraphDialogContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: EditParagraphDialogContext = context

        self.setWindowTitle("Edit paragraph")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # alignment

        self.alignment_title_label: QLabel = QLabel(self)
        self.alignment_title_label.setText("Alignment")

        self.alignment_combo_box_label: QLabel = QLabel(self)
        self.alignment_combo_box_label.setText("Alignment")

        self.alignment_combo_box: QComboBox = QComboBox(self)
        self.alignment_combo_box.setEditable(True)
        self.alignment_combo_box.lineEdit().setEnabled(False)
        self.aligment_flags: list[Qt.AlignmentFlag] = [
            Qt.AlignmentFlag.AlignLeft,
            Qt.AlignmentFlag.AlignCenter,
            Qt.AlignmentFlag.AlignRight,
        ]
        self.aligment_names: list[str] = ["Left", "Center", "Right"]
        self.alignment_combo_box.addItems(self.aligment_names)
        self.alignment_combo_box.setCurrentIndex(self.aligment_flags.index(context.alignment))

        alignment_combo_box_layout = QHBoxLayout()
        alignment_combo_box_layout.setContentsMargins(0, 0, 0, 0)
        alignment_combo_box_layout.setSpacing(10)
        alignment_combo_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        alignment_combo_box_layout.addWidget(self.alignment_combo_box_label)
        alignment_combo_box_layout.addWidget(self.alignment_combo_box)

        alignment_layout = QVBoxLayout()
        alignment_layout.setContentsMargins(0, 0, 0, 0)
        alignment_layout.setSpacing(0)
        alignment_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        alignment_layout.addWidget(self.alignment_title_label)
        alignment_layout.addSpacing(15)
        alignment_layout.addLayout(alignment_combo_box_layout)
        alignment_layout.addSpacing(5)

        # heading

        self.heading_title_label: QLabel = QLabel(self)
        self.heading_title_label.setText("Heading")

        self.heading_level_combo_box_label: QLabel = QLabel(self)
        self.heading_level_combo_box_label.setText("Heading level")

        self.heading_level_combo_box: QComboBox = QComboBox(self)
        self.heading_level_combo_box.setEditable(True)
        self.heading_level_combo_box.lineEdit().setEnabled(False)
        self.heading_levels: list[int] = [0, 1, 2, 3, 4, 5, 6]
        self.heading_level_names: list[str] = ["0", "1", "2", "3", "4", "5", "6"]
        self.heading_level_combo_box.addItems(self.heading_level_names)
        self.heading_level_combo_box.setCurrentIndex(self.heading_levels.index(context.heading_level))

        heading_level_combo_box_layout = QHBoxLayout()
        heading_level_combo_box_layout.setContentsMargins(0, 0, 0, 0)
        heading_level_combo_box_layout.setSpacing(10)
        heading_level_combo_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        heading_level_combo_box_layout.addWidget(self.heading_level_combo_box_label)
        heading_level_combo_box_layout.addWidget(self.heading_level_combo_box)

        heading_layout = QVBoxLayout()
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(0)
        heading_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        heading_layout.addWidget(self.heading_title_label)
        heading_layout.addSpacing(15)
        heading_layout.addLayout(heading_level_combo_box_layout)
        heading_layout.addSpacing(5)

        # indent

        self.indent_title_label: QLabel = QLabel(self)
        self.indent_title_label.setText("Indent")

        self.first_line_indent_check_box: QCheckBox = QCheckBox(self)
        self.first_line_indent_check_box.setText("Turn first line indent")
        self.first_line_indent_check_box.setChecked(self.context.is_first_line_indent_turned)

        self.first_line_indent_spin_box_label: QLabel = QLabel(self)
        self.first_line_indent_spin_box_label.setText("First line indent")

        self.first_line_indent_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.first_line_indent_spin_box.setMinimum(0.0)
        self.first_line_indent_spin_box.setSingleStep(0.25)
        self.first_line_indent_spin_box.setDecimals(2)
        self.first_line_indent_spin_box.setSuffix(" cm")
        self.first_line_indent_spin_box.setValue(self.context.first_line_indent)
        self.first_line_indent_spin_box.setEnabled(self.context.is_first_line_indent_turned)
        self.first_line_indent_check_box.stateChanged.connect(self.first_line_indent_spin_box.setEnabled)

        self.first_line_indent_spin_box_error: QLabel = QLabel(self)
        self.first_line_indent_spin_box_error.setText("Invalid input")
        self.first_line_indent_spin_box_error.setFixedHeight(10)
        font = self.first_line_indent_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.first_line_indent_spin_box_error.setFont(font)
        self.first_line_indent_spin_box_error.hide()

        self.indent_spin_box_label: QLabel = QLabel(self)
        self.indent_spin_box_label.setText("Indent")

        self.indent_spin_box: QSpinBox = QSpinBox(self)
        self.indent_spin_box.setMinimum(0)
        self.indent_spin_box.setSingleStep(1)
        self.indent_spin_box.setValue(self.context.indent)

        self.indent_spin_box_error: QLabel = QLabel(self)
        self.indent_spin_box_error.setText("Invalid input")
        self.indent_spin_box_error.setFixedHeight(10)
        font = self.indent_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.indent_spin_box_error.setFont(font)
        self.indent_spin_box_error.hide()

        first_line_indent_spin_box_layout = QHBoxLayout()
        first_line_indent_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        first_line_indent_spin_box_layout.setSpacing(10)
        first_line_indent_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        first_line_indent_spin_box_layout.addWidget(self.first_line_indent_spin_box_label)
        first_line_indent_spin_box_layout.addWidget(self.first_line_indent_spin_box)

        indent_spin_box_layout = QHBoxLayout()
        indent_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        indent_spin_box_layout.setSpacing(10)
        indent_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        indent_spin_box_layout.addWidget(self.indent_spin_box_label)
        indent_spin_box_layout.addWidget(self.indent_spin_box)

        indent_layout = QVBoxLayout()
        indent_layout.setContentsMargins(0, 0, 0, 0)
        indent_layout.setSpacing(0)
        indent_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        indent_layout.addWidget(self.indent_title_label)
        indent_layout.addSpacing(15)
        indent_layout.addWidget(self.first_line_indent_check_box)
        indent_layout.addSpacing(5)
        indent_layout.addLayout(first_line_indent_spin_box_layout)
        indent_layout.addWidget(self.first_line_indent_spin_box_error)
        indent_layout.addSpacing(5)
        indent_layout.addLayout(indent_spin_box_layout)
        indent_layout.addWidget(self.indent_spin_box_error)
        indent_layout.addSpacing(5)

        # line spacing

        self.spacing_title_label: QLabel = QLabel(self)
        self.spacing_title_label.setText("Spacing")

        self.line_spacing_spin_box_label: QLabel = QLabel(self)
        self.line_spacing_spin_box_label.setText("Line spacing")

        self.line_spacing_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.line_spacing_spin_box.setMinimum(0.0)
        self.line_spacing_spin_box.setMaximum(5.0)
        self.line_spacing_spin_box.setSingleStep(0.05)
        self.line_spacing_spin_box.setDecimals(2)
        self.line_spacing_spin_box.setValue(self.context.line_spacing)

        self.line_spacing_spin_box_error: QLabel = QLabel(self)
        self.line_spacing_spin_box_error.setText("Invalid input")
        self.line_spacing_spin_box_error.setFixedHeight(10)
        font = self.line_spacing_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.line_spacing_spin_box_error.setFont(font)
        self.line_spacing_spin_box_error.hide()

        line_spacing_spin_box_layout = QHBoxLayout()
        line_spacing_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        line_spacing_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        line_spacing_spin_box_layout.addWidget(self.line_spacing_spin_box_label)
        line_spacing_spin_box_layout.addWidget(self.line_spacing_spin_box)

        spacing_layout = QVBoxLayout()
        spacing_layout.setContentsMargins(0, 0, 0, 0)
        spacing_layout.setSpacing(0)
        spacing_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        spacing_layout.addWidget(self.spacing_title_label)
        spacing_layout.addSpacing(15)
        spacing_layout.addLayout(line_spacing_spin_box_layout)
        spacing_layout.addWidget(self.line_spacing_spin_box_error)
        spacing_layout.addSpacing(5)

        # margin

        self.margin_title_label: QLabel = QLabel(self)
        self.margin_title_label.setText("Margin")

        self.top_margin_spin_box_label: QLabel = QLabel(self)
        self.top_margin_spin_box_label.setText("Top margin")

        self.top_margin_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.top_margin_spin_box.setMinimum(0.0)
        self.top_margin_spin_box.setSingleStep(0.25)
        self.top_margin_spin_box.setDecimals(2)
        self.top_margin_spin_box.setSuffix(" cm")
        self.top_margin_spin_box.setValue(self.context.top_margin)

        self.top_margin_spin_box_error: QLabel = QLabel(self)
        self.top_margin_spin_box_error.setText("Invalid input")
        self.top_margin_spin_box_error.setFixedHeight(10)
        font = self.top_margin_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.top_margin_spin_box_error.setFont(font)
        self.top_margin_spin_box_error.hide()

        self.bottom_margin_spin_box_label: QLabel = QLabel(self)
        self.bottom_margin_spin_box_label.setText("Bottom margin")

        self.bottom_margin_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.bottom_margin_spin_box.setMinimum(0.0)
        self.bottom_margin_spin_box.setSingleStep(0.25)
        self.bottom_margin_spin_box.setDecimals(2)
        self.bottom_margin_spin_box.setSuffix(" cm")
        self.bottom_margin_spin_box.setValue(self.context.bottom_margin)

        self.bottom_margin_spin_box_error: QLabel = QLabel(self)
        self.bottom_margin_spin_box_error.setText("Invalid input")
        self.bottom_margin_spin_box_error.setFixedHeight(10)
        font = self.bottom_margin_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.bottom_margin_spin_box_error.setFont(font)
        self.bottom_margin_spin_box_error.hide()

        self.left_margin_spin_box_label: QLabel = QLabel(self)
        self.left_margin_spin_box_label.setText("Left margin")

        self.left_margin_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.left_margin_spin_box.setMinimum(0.0)
        self.left_margin_spin_box.setSingleStep(0.25)
        self.left_margin_spin_box.setDecimals(2)
        self.left_margin_spin_box.setSuffix(" cm")
        self.left_margin_spin_box.setValue(self.context.left_margin)

        self.left_margin_spin_box_error: QLabel = QLabel(self)
        self.left_margin_spin_box_error.setText("Invalid input")
        self.left_margin_spin_box_error.setFixedHeight(10)
        font = self.left_margin_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.left_margin_spin_box_error.setFont(font)
        self.left_margin_spin_box_error.hide()

        self.right_margin_spin_box_label: QLabel = QLabel(self)
        self.right_margin_spin_box_label.setText("Right margin")

        self.right_margin_spin_box: QDoubleSpinBox = QDoubleSpinBox(self)
        self.right_margin_spin_box.setMinimum(0.0)
        self.right_margin_spin_box.setSingleStep(0.25)
        self.right_margin_spin_box.setDecimals(2)
        self.right_margin_spin_box.setSuffix(" cm")
        self.right_margin_spin_box.setValue(self.context.right_margin)

        self.right_margin_spin_box_error: QLabel = QLabel(self)
        self.right_margin_spin_box_error.setText("Invalid input")
        self.right_margin_spin_box_error.setFixedHeight(10)
        font = self.right_margin_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.right_margin_spin_box_error.setFont(font)
        self.right_margin_spin_box_error.hide()

        top_margin_spin_box_layout = QHBoxLayout()
        top_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        top_margin_spin_box_layout.setSpacing(10)
        top_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_margin_spin_box_layout.addWidget(self.top_margin_spin_box_label)
        top_margin_spin_box_layout.addWidget(self.top_margin_spin_box)

        bottom_margin_spin_box_layout = QHBoxLayout()
        bottom_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        bottom_margin_spin_box_layout.setSpacing(10)
        bottom_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_margin_spin_box_layout.addWidget(self.bottom_margin_spin_box_label)
        bottom_margin_spin_box_layout.addWidget(self.bottom_margin_spin_box)

        left_margin_spin_box_layout = QHBoxLayout()
        left_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        left_margin_spin_box_layout.setSpacing(10)
        left_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_margin_spin_box_layout.addWidget(self.left_margin_spin_box_label)
        left_margin_spin_box_layout.addWidget(self.left_margin_spin_box)

        right_margin_spin_box_layout = QHBoxLayout()
        right_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        right_margin_spin_box_layout.setSpacing(10)
        right_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        right_margin_spin_box_layout.addWidget(self.right_margin_spin_box_label)
        right_margin_spin_box_layout.addWidget(self.right_margin_spin_box)

        margin_layout = QVBoxLayout()
        margin_layout.setContentsMargins(0, 0, 0, 0)
        margin_layout.setSpacing(0)
        margin_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        margin_layout.addWidget(self.margin_title_label)
        margin_layout.addSpacing(15)
        margin_layout.addLayout(top_margin_spin_box_layout)
        margin_layout.addWidget(self.top_margin_spin_box_error)
        margin_layout.addSpacing(5)
        margin_layout.addLayout(bottom_margin_spin_box_layout)
        margin_layout.addWidget(self.bottom_margin_spin_box_error)
        margin_layout.addSpacing(5)
        margin_layout.addLayout(left_margin_spin_box_layout)
        margin_layout.addWidget(self.left_margin_spin_box_error)
        margin_layout.addSpacing(5)
        margin_layout.addLayout(right_margin_spin_box_layout)
        margin_layout.addWidget(self.right_margin_spin_box_error)
        margin_layout.addSpacing(5)

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

        # layout

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.addLayout(alignment_layout)
        left_layout.addLayout(heading_layout)
        left_layout.addLayout(indent_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.addLayout(spacing_layout)
        right_layout.addLayout(margin_layout)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(20)
        top_layout.addLayout(left_layout, 1)
        top_layout.addLayout(right_layout, 1)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)
        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

    def onSaveClicked(self) -> None:
        is_valid = True

        if not self.first_line_indent_spin_box.hasAcceptableInput():
            is_valid = False
            self.first_line_indent_spin_box_error.show()
        else:
            self.first_line_indent_spin_box_error.hide()

        if not self.indent_spin_box.hasAcceptableInput():
            is_valid = False
            self.indent_spin_box_error.show()
        else:
            self.indent_spin_box_error.hide()

        if not self.line_spacing_spin_box.hasAcceptableInput():
            is_valid = False
            self.line_spacing_spin_box_error.show()
        else:
            self.line_spacing_spin_box_error.hide()

        if not self.top_margin_spin_box.hasAcceptableInput():
            is_valid = False
            self.top_margin_spin_box_error.show()
        else:
            self.top_margin_spin_box_error.hide()

        if not self.bottom_margin_spin_box.hasAcceptableInput():
            is_valid = False
            self.bottom_margin_spin_box_error.show()
        else:
            self.bottom_margin_spin_box_error.hide()

        if not self.left_margin_spin_box.hasAcceptableInput():
            is_valid = False
            self.left_margin_spin_box_error.show()
        else:
            self.left_margin_spin_box_error.hide()

        if not self.right_margin_spin_box.hasAcceptableInput():
            is_valid = False
            self.right_margin_spin_box_error.show()
        else:
            self.right_margin_spin_box_error.hide()

        if not is_valid:
            return

        self.context.alignment = self.aligment_flags[self.alignment_combo_box.currentIndex()]
        self.context.heading_level = self.heading_levels[self.heading_level_combo_box.currentIndex()]
        self.context.is_first_line_indent_turned = self.first_line_indent_check_box.isChecked()
        self.context.first_line_indent = self.first_line_indent_spin_box.value()
        self.context.indent = self.indent_spin_box.value()
        self.context.line_spacing = self.line_spacing_spin_box.value()
        self.context.top_margin = self.top_margin_spin_box.value()
        self.context.bottom_margin = self.bottom_margin_spin_box.value()
        self.context.left_margin = self.left_margin_spin_box.value()
        self.context.right_margin = self.right_margin_spin_box.value()

        self.accept()

    def onCancelClicked(self) -> None:
        self.reject()
