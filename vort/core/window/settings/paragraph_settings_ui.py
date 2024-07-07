from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QSpinBox, QScrollArea
from PySide6.QtGui import QColor, QPalette

from core.widget.basic_widget import DoubleSpinBox, ComboBox


class ParagraphSettingsContext:

    def __init__(self) -> None:
        self.alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft

        self.first_line_indent: float = 0.0  # cm
        self.indent: int = 0  # cm
        self.indent_step: float = 0.0  # cm

        self.line_spacing: float = 1.0  # ratio

        self.top_margin: float = 0.0  # cm
        self.bottom_margin: float = 0.0  # cm
        self.left_margin: float = 0.0  # cm
        self.right_margin: float = 0.0  # cm


class ParagraphSettingsUI(QScrollArea):
    def __init__(self, context: ParagraphSettingsContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: ParagraphSettingsContext = context
        self.setWidgetResizable(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("transparent"))
        palette.setColor(QPalette.ColorRole.Base, palette.color(QPalette.ColorRole.Base))
        self.setPalette(palette)

        # alignment

        self.alignment_title_label: QLabel = QLabel(self)
        self.alignment_title_label.setText("Alignment")

        self.alignment_combo_box_label: QLabel = QLabel(self)
        self.alignment_combo_box_label.setText("Alignment")

        self.alignment_combo_box: ComboBox = ComboBox(self)
        self.alignment_combo_box.setEditable(True)
        self.alignment_combo_box.lineEdit().setEnabled(False)
        self.aligment_flags: list[Qt.AlignmentFlag] = [
            Qt.AlignmentFlag.AlignLeft,
            Qt.AlignmentFlag.AlignHCenter,
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

        # indent

        self.indent_title_label: QLabel = QLabel(self)
        self.indent_title_label.setText("Indent")

        self.first_line_indent_spin_box_label: QLabel = QLabel(self)
        self.first_line_indent_spin_box_label.setText("First line indent")

        self.first_line_indent_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.first_line_indent_spin_box.setMinimum(0.0)
        self.first_line_indent_spin_box.setSingleStep(0.25)
        self.first_line_indent_spin_box.setDecimals(2)
        self.first_line_indent_spin_box.setSuffix(" cm")
        self.first_line_indent_spin_box.setValue(self.context.first_line_indent)

        self.first_line_indent_spin_box_error: QLabel = QLabel(self)
        self.first_line_indent_spin_box_error.setText("Invalid input")
        self.first_line_indent_spin_box_error.setFixedHeight(10)
        font = self.first_line_indent_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.first_line_indent_spin_box_error.setFont(font)
        self.first_line_indent_spin_box_error.hide()

        first_line_indent_spin_box_layout = QHBoxLayout()
        first_line_indent_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        first_line_indent_spin_box_layout.setSpacing(10)
        first_line_indent_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        first_line_indent_spin_box_layout.addWidget(self.first_line_indent_spin_box_label)
        first_line_indent_spin_box_layout.addWidget(self.first_line_indent_spin_box)

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

        indent_spin_box_layout = QHBoxLayout()
        indent_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        indent_spin_box_layout.setSpacing(10)
        indent_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        indent_spin_box_layout.addWidget(self.indent_spin_box_label)
        indent_spin_box_layout.addWidget(self.indent_spin_box)

        self.indent_step_spin_box_label: QLabel = QLabel(self)
        self.indent_step_spin_box_label.setText("Indent step")

        self.indent_step_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.indent_step_spin_box.setMinimum(0.0)
        self.indent_step_spin_box.setSingleStep(0.25)
        self.indent_step_spin_box.setDecimals(2)
        self.indent_step_spin_box.setSuffix(" cm")
        self.indent_step_spin_box.setValue(self.context.indent_step)

        self.indent_step_spin_box_error: QLabel = QLabel(self)
        self.indent_step_spin_box_error.setText("Invalid input")
        self.indent_step_spin_box_error.setFixedHeight(10)
        font = self.indent_step_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.indent_step_spin_box_error.setFont(font)
        self.indent_step_spin_box_error.hide()

        indent_step_spin_box_layout = QHBoxLayout()
        indent_step_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        indent_step_spin_box_layout.setSpacing(10)
        indent_step_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        indent_step_spin_box_layout.addWidget(self.indent_step_spin_box_label)
        indent_step_spin_box_layout.addWidget(self.indent_step_spin_box)

        indent_layout = QVBoxLayout()
        indent_layout.setContentsMargins(0, 0, 0, 0)
        indent_layout.setSpacing(0)
        indent_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        indent_layout.addWidget(self.indent_title_label)
        indent_layout.addSpacing(15)
        indent_layout.addLayout(first_line_indent_spin_box_layout)
        indent_layout.addWidget(self.first_line_indent_spin_box_error)
        indent_layout.addSpacing(5)
        indent_layout.addLayout(indent_spin_box_layout)
        indent_layout.addWidget(self.indent_spin_box_error)
        indent_layout.addSpacing(5)
        indent_layout.addLayout(indent_step_spin_box_layout)
        indent_layout.addWidget(self.indent_step_spin_box_error)
        indent_layout.addSpacing(5)

        # line spacing

        self.spacing_title_label: QLabel = QLabel(self)
        self.spacing_title_label.setText("Spacing")

        self.line_spacing_spin_box_label: QLabel = QLabel(self)
        self.line_spacing_spin_box_label.setText("Line spacing")

        self.line_spacing_spin_box: DoubleSpinBox = DoubleSpinBox(self)
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
        line_spacing_spin_box_layout.setSpacing(10)
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

        self.top_margin_spin_box: DoubleSpinBox = DoubleSpinBox(self)
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

        top_margin_spin_box_layout = QHBoxLayout()
        top_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        top_margin_spin_box_layout.setSpacing(10)
        top_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_margin_spin_box_layout.addWidget(self.top_margin_spin_box_label)
        top_margin_spin_box_layout.addWidget(self.top_margin_spin_box)

        self.bottom_margin_spin_box_label: QLabel = QLabel(self)
        self.bottom_margin_spin_box_label.setText("Bottom margin")

        self.bottom_margin_spin_box: DoubleSpinBox = DoubleSpinBox(self)
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

        bottom_margin_spin_box_layout = QHBoxLayout()
        bottom_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        bottom_margin_spin_box_layout.setSpacing(10)
        bottom_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_margin_spin_box_layout.addWidget(self.bottom_margin_spin_box_label)
        bottom_margin_spin_box_layout.addWidget(self.bottom_margin_spin_box)

        self.left_margin_spin_box_label: QLabel = QLabel(self)
        self.left_margin_spin_box_label.setText("Left margin")

        self.left_margin_spin_box: DoubleSpinBox = DoubleSpinBox(self)
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

        left_margin_spin_box_layout = QHBoxLayout()
        left_margin_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        left_margin_spin_box_layout.setSpacing(10)
        left_margin_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_margin_spin_box_layout.addWidget(self.left_margin_spin_box_label)
        left_margin_spin_box_layout.addWidget(self.left_margin_spin_box)

        self.right_margin_spin_box_label: QLabel = QLabel(self)
        self.right_margin_spin_box_label.setText("Right margin")

        self.right_margin_spin_box: DoubleSpinBox = DoubleSpinBox(self)
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

        # layout

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.addLayout(alignment_layout)
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

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addLayout(top_layout)

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(main_layout)
        self.setWidget(self.scroll_widget)

    def validate(self) -> bool:
        is_valid = True

        is_valid = is_valid and self.first_line_indent_spin_box.hasAcceptableInput()
        self.first_line_indent_spin_box_error.setHidden(self.first_line_indent_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.indent_spin_box.hasAcceptableInput()
        self.indent_spin_box_error.setHidden(self.indent_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.indent_step_spin_box.hasAcceptableInput()
        self.indent_step_spin_box_error.setHidden(self.indent_step_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.line_spacing_spin_box.hasAcceptableInput()
        self.line_spacing_spin_box_error.setHidden(self.line_spacing_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.top_margin_spin_box.hasAcceptableInput()
        self.top_margin_spin_box_error.setHidden(self.top_margin_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.bottom_margin_spin_box.hasAcceptableInput()
        self.bottom_margin_spin_box_error.setHidden(self.bottom_margin_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.left_margin_spin_box.hasAcceptableInput()
        self.left_margin_spin_box_error.setHidden(self.left_margin_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.right_margin_spin_box.hasAcceptableInput()
        self.right_margin_spin_box_error.setHidden(self.right_margin_spin_box.hasAcceptableInput())

        return is_valid
