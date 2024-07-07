from PySide6.QtCore import Qt, Signal, QObject, QEvent
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QScrollArea
from PySide6.QtGui import QColor, QPalette

from core.window.settings.settings_widget import DoubleSpinBox, SpinBox
from core.widget.tool_bar.color_picker.color_picker import ColorPicker


class PageSettingsContext:
    def __init__(self) -> None:
        self.width: float = 21  # cm
        self.height: float = 29.7  # cm
        self.spacing: float = 1  # cm

        self.page_color: QColor = QColor("white")

        self.top_margin: float = 1  # cm
        self.bottom_margin: float = 1  # cm
        self.left_margin: float = 1  # cm
        self.right_margin: float = 1  # cm

        self.top_padding: float = 1  # cm
        self.bottom_padding: float = 1  # cm
        self.left_padding: float = 1  # cm
        self.right_padding: float = 1  # cm

        self.border_width: float = 0  # mm
        self.border_color: QColor = QColor("black")


class PageSettingsUI(QScrollArea):
    def __init__(self, context: PageSettingsContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: PageSettingsContext = context
        self.setWidgetResizable(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("transparent"))
        palette.setColor(QPalette.ColorRole.Base, palette.color(QPalette.ColorRole.Base))
        self.setPalette(palette)

        # size

        self.size_title_label: QLabel = QLabel(self)
        self.size_title_label.setText("Size")

        self.width_spin_box_label: QLabel = QLabel(self)
        self.width_spin_box_label.setText("Width")

        self.width_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.width_spin_box.setMinimum(0.0)
        self.width_spin_box.setSingleStep(0.25)
        self.width_spin_box.setDecimals(2)
        self.width_spin_box.setSuffix(" cm")
        self.width_spin_box.setValue(self.context.width)

        self.width_spin_box_error: QLabel = QLabel(self)
        self.width_spin_box_error.setText("Invalid input")
        self.width_spin_box_error.setFixedHeight(10)
        font = self.width_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.width_spin_box_error.setFont(font)
        self.width_spin_box_error.hide()

        width_spin_box_layout = QHBoxLayout()
        width_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        width_spin_box_layout.setSpacing(10)
        width_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        width_spin_box_layout.addWidget(self.width_spin_box_label)
        width_spin_box_layout.addWidget(self.width_spin_box)

        self.height_spin_box_label: QLabel = QLabel(self)
        self.height_spin_box_label.setText("Height")

        self.height_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.height_spin_box.setMinimum(0.0)
        self.height_spin_box.setSingleStep(0.25)
        self.height_spin_box.setDecimals(2)
        self.height_spin_box.setSuffix(" cm")
        self.height_spin_box.setValue(self.context.height)

        self.height_spin_box_error: QLabel = QLabel(self)
        self.height_spin_box_error.setText("Invalid input")
        self.height_spin_box_error.setFixedHeight(10)
        font = self.height_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.height_spin_box_error.setFont(font)
        self.height_spin_box_error.hide()

        height_spin_box_layout = QHBoxLayout()
        height_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        height_spin_box_layout.setSpacing(10)
        height_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        height_spin_box_layout.addWidget(self.height_spin_box_label)
        height_spin_box_layout.addWidget(self.height_spin_box)

        self.spacing: float = 1  # cm

        self.spacing_spin_box_label: QLabel = QLabel(self)
        self.spacing_spin_box_label.setText("Height")

        self.spacing_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.spacing_spin_box.setMinimum(0.0)
        self.spacing_spin_box.setSingleStep(0.25)
        self.spacing_spin_box.setDecimals(2)
        self.spacing_spin_box.setSuffix(" cm")
        self.spacing_spin_box.setValue(self.context.spacing)

        self.spacing_spin_box_error: QLabel = QLabel(self)
        self.spacing_spin_box_error.setText("Invalid input")
        self.spacing_spin_box_error.setFixedHeight(10)
        font = self.spacing_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.spacing_spin_box_error.setFont(font)
        self.spacing_spin_box_error.hide()

        spacing_spin_box_layout = QHBoxLayout()
        spacing_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        spacing_spin_box_layout.setSpacing(10)
        spacing_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        spacing_spin_box_layout.addWidget(self.spacing_spin_box_label)
        spacing_spin_box_layout.addWidget(self.spacing_spin_box)

        size_layout = QVBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(0)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        size_layout.addWidget(self.size_title_label)
        size_layout.addSpacing(15)
        size_layout.addLayout(width_spin_box_layout)
        size_layout.addWidget(self.width_spin_box_error)
        size_layout.addSpacing(5)
        size_layout.addLayout(height_spin_box_layout)
        size_layout.addWidget(self.height_spin_box_error)
        size_layout.addSpacing(5)
        size_layout.addLayout(spacing_spin_box_layout)
        size_layout.addWidget(self.spacing_spin_box_error)
        size_layout.addSpacing(5)

        # color

        self.color_title_label: QLabel = QLabel(self)
        self.color_title_label.setText("Color")

        self.page_color_line_edit_label: QLabel = QLabel(self)
        self.page_color_line_edit_label.setText("Page")

        self.page_color_red_spin_box: SpinBox = SpinBox(self)
        self.page_color_red_spin_box.setMinimum(0)
        self.page_color_red_spin_box.setMaximum(255)
        self.page_color_red_spin_box.setSuffix(" R")
        self.page_color_red_spin_box.setValue(self.context.page_color.red())
        self.page_color_red_spin_box.valueChanged.connect(self.onColorSpinBoxValueChanged)

        self.page_color_green_spin_box: SpinBox = SpinBox(self)
        self.page_color_green_spin_box.setMinimum(0)
        self.page_color_green_spin_box.setMaximum(255)
        self.page_color_green_spin_box.setSuffix(" G")
        self.page_color_green_spin_box.setValue(self.context.page_color.green())
        self.page_color_green_spin_box.valueChanged.connect(self.onColorSpinBoxValueChanged)

        self.page_color_blue_spin_box: SpinBox = SpinBox(self)
        self.page_color_blue_spin_box.setMinimum(0)
        self.page_color_blue_spin_box.setMaximum(255)
        self.page_color_blue_spin_box.setSuffix(" B")
        self.page_color_blue_spin_box.setValue(self.context.page_color.blue())
        self.page_color_blue_spin_box.valueChanged.connect(self.onColorSpinBoxValueChanged)

        self.page_color_picker: ColorPicker = ColorPicker(self)
        self.page_color_picker.setColor(self.context.page_color)
        page_color_picker_palette = self.page_color_picker.ui.palette()
        page_color_picker_palette.setColor(QPalette.ColorRole.Button, palette.color(QPalette.ColorRole.Base))
        page_color_picker_palette.setColor(QPalette.ColorRole.Window, palette.color(QPalette.ColorRole.Base))
        self.page_color_picker.ui.setPalette(page_color_picker_palette)
        self.page_color_picker.colorChanged.connect(self.onPageColorChanged)

        # connect etc

        self.color_line_edit_error: QLabel = QLabel(self)
        self.color_line_edit_error.setText("Invalid input")
        self.color_line_edit_error.setFixedHeight(10)
        font = self.color_line_edit_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.color_line_edit_error.setFont(font)
        self.color_line_edit_error.hide()

        color_picker_layout = QHBoxLayout()
        color_picker_layout.setContentsMargins(0, 0, 0, 0)
        color_picker_layout.setSpacing(10)
        color_picker_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        color_picker_layout.addWidget(self.page_color_line_edit_label)
        color_picker_layout.addWidget(self.page_color_red_spin_box)
        color_picker_layout.addWidget(self.page_color_green_spin_box)
        color_picker_layout.addWidget(self.page_color_blue_spin_box)
        color_picker_layout.addWidget(self.page_color_picker.ui)

        color_layout = QVBoxLayout()
        color_layout.setContentsMargins(0, 0, 0, 0)
        color_layout.setSpacing(0)
        color_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        color_layout.addWidget(self.color_title_label)
        color_layout.addSpacing(15)
        color_layout.addLayout(color_picker_layout)
        color_layout.addWidget(self.color_line_edit_error)
        color_layout.addSpacing(5)

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

        # padding

        self.padding_title_label: QLabel = QLabel(self)
        self.padding_title_label.setText("Padding")

        self.top_padding_spin_box_label: QLabel = QLabel(self)
        self.top_padding_spin_box_label.setText("Top padding")

        self.top_padding_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.top_padding_spin_box.setMinimum(0.0)
        self.top_padding_spin_box.setSingleStep(0.25)
        self.top_padding_spin_box.setDecimals(2)
        self.top_padding_spin_box.setSuffix(" cm")
        self.top_padding_spin_box.setValue(self.context.top_padding)

        self.top_padding_spin_box_error: QLabel = QLabel(self)
        self.top_padding_spin_box_error.setText("Invalid input")
        self.top_padding_spin_box_error.setFixedHeight(10)
        font = self.top_padding_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.top_padding_spin_box_error.setFont(font)
        self.top_padding_spin_box_error.hide()

        top_padding_spin_box_layout = QHBoxLayout()
        top_padding_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        top_padding_spin_box_layout.setSpacing(10)
        top_padding_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_padding_spin_box_layout.addWidget(self.top_padding_spin_box_label)
        top_padding_spin_box_layout.addWidget(self.top_padding_spin_box)

        self.bottom_padding_spin_box_label: QLabel = QLabel(self)
        self.bottom_padding_spin_box_label.setText("Bottom padding")

        self.bottom_padding_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.bottom_padding_spin_box.setMinimum(0.0)
        self.bottom_padding_spin_box.setSingleStep(0.25)
        self.bottom_padding_spin_box.setDecimals(2)
        self.bottom_padding_spin_box.setSuffix(" cm")
        self.bottom_padding_spin_box.setValue(self.context.bottom_padding)

        self.bottom_padding_spin_box_error: QLabel = QLabel(self)
        self.bottom_padding_spin_box_error.setText("Invalid input")
        self.bottom_padding_spin_box_error.setFixedHeight(10)
        font = self.bottom_padding_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.bottom_padding_spin_box_error.setFont(font)
        self.bottom_padding_spin_box_error.hide()

        bottom_padding_spin_box_layout = QHBoxLayout()
        bottom_padding_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        bottom_padding_spin_box_layout.setSpacing(10)
        bottom_padding_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bottom_padding_spin_box_layout.addWidget(self.bottom_padding_spin_box_label)
        bottom_padding_spin_box_layout.addWidget(self.bottom_padding_spin_box)

        self.left_padding_spin_box_label: QLabel = QLabel(self)
        self.left_padding_spin_box_label.setText("Left padding")

        self.left_padding_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.left_padding_spin_box.setMinimum(0.0)
        self.left_padding_spin_box.setSingleStep(0.25)
        self.left_padding_spin_box.setDecimals(2)
        self.left_padding_spin_box.setSuffix(" cm")
        self.left_padding_spin_box.setValue(self.context.left_padding)

        self.left_padding_spin_box_error: QLabel = QLabel(self)
        self.left_padding_spin_box_error.setText("Invalid input")
        self.left_padding_spin_box_error.setFixedHeight(10)
        font = self.left_padding_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.left_padding_spin_box_error.setFont(font)
        self.left_padding_spin_box_error.hide()

        left_padding_spin_box_layout = QHBoxLayout()
        left_padding_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        left_padding_spin_box_layout.setSpacing(10)
        left_padding_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_padding_spin_box_layout.addWidget(self.left_padding_spin_box_label)
        left_padding_spin_box_layout.addWidget(self.left_padding_spin_box)

        self.right_padding_spin_box_label: QLabel = QLabel(self)
        self.right_padding_spin_box_label.setText("Right padding")

        self.right_padding_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.right_padding_spin_box.setMinimum(0.0)
        self.right_padding_spin_box.setSingleStep(0.25)
        self.right_padding_spin_box.setDecimals(2)
        self.right_padding_spin_box.setSuffix(" cm")
        self.right_padding_spin_box.setValue(self.context.right_padding)

        self.right_padding_spin_box_error: QLabel = QLabel(self)
        self.right_padding_spin_box_error.setText("Invalid input")
        self.right_padding_spin_box_error.setFixedHeight(10)
        font = self.right_padding_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.right_padding_spin_box_error.setFont(font)
        self.right_padding_spin_box_error.hide()

        right_padding_spin_box_layout = QHBoxLayout()
        right_padding_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        right_padding_spin_box_layout.setSpacing(10)
        right_padding_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        right_padding_spin_box_layout.addWidget(self.right_padding_spin_box_label)
        right_padding_spin_box_layout.addWidget(self.right_padding_spin_box)

        padding_layout = QVBoxLayout()
        padding_layout.setContentsMargins(0, 0, 0, 0)
        padding_layout.setSpacing(0)
        padding_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        padding_layout.addWidget(self.padding_title_label)
        padding_layout.addSpacing(15)
        padding_layout.addLayout(top_padding_spin_box_layout)
        padding_layout.addWidget(self.top_padding_spin_box_error)
        padding_layout.addSpacing(5)
        padding_layout.addLayout(bottom_padding_spin_box_layout)
        padding_layout.addWidget(self.bottom_padding_spin_box_error)
        padding_layout.addSpacing(5)
        padding_layout.addLayout(left_padding_spin_box_layout)
        padding_layout.addWidget(self.left_padding_spin_box_error)
        padding_layout.addSpacing(5)
        padding_layout.addLayout(right_padding_spin_box_layout)
        padding_layout.addWidget(self.right_padding_spin_box_error)
        padding_layout.addSpacing(5)

        # border

        self.border_title_label: QLabel = QLabel(self)
        self.border_title_label.setText("Border")

        self.border_width_spin_box_label: QLabel = QLabel(self)
        self.border_width_spin_box_label.setText("Width")

        self.border_width_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.border_width_spin_box.setMinimum(0.0)
        self.border_width_spin_box.setSingleStep(0.5)
        self.border_width_spin_box.setDecimals(2)
        self.border_width_spin_box.setSuffix(" mm")
        self.border_width_spin_box.setValue(self.context.border_width)

        self.border_width_spin_box_error: QLabel = QLabel(self)
        self.border_width_spin_box_error.setText("Invalid input")
        self.border_width_spin_box_error.setFixedHeight(10)
        font = self.border_width_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.border_width_spin_box_error.setFont(font)
        self.border_width_spin_box_error.hide()

        border_width_spin_box_layout = QHBoxLayout()
        border_width_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        border_width_spin_box_layout.setSpacing(10)
        border_width_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        border_width_spin_box_layout.addWidget(self.border_width_spin_box_label)
        border_width_spin_box_layout.addWidget(self.border_width_spin_box)

        self.border_color_line_edit_label: QLabel = QLabel(self)
        self.border_color_line_edit_label.setText("Color")

        # TODO: add validator #FFFFFF
        self.border_color_line_edit: QLineEdit = QLineEdit(self)
        # self.border_color_line_edit.setValidator()

        # self.border_color: QColor = QColor("black")
        # TODO: own widget

        # self.border_color_picker: ColorPicker = ColorPicker(self)
        # connect etc

        self.border_color_line_edit_error: QLabel = QLabel(self)
        self.border_color_line_edit_error.setText("Invalid input")
        self.border_color_line_edit_error.setFixedHeight(10)
        font = self.border_color_line_edit_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.border_color_line_edit_error.setFont(font)
        self.border_color_line_edit_error.hide()

        border_color_picker_layout = QHBoxLayout()
        border_color_picker_layout.setContentsMargins(0, 0, 0, 0)
        border_color_picker_layout.setSpacing(10)
        border_color_picker_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        border_color_picker_layout.addWidget(self.border_color_line_edit_label)
        border_color_picker_layout.addWidget(self.border_color_line_edit)
        # border_color_picker_layout.addWidget(self.border_color_picker)

        border_layout = QVBoxLayout()
        border_layout.setContentsMargins(0, 0, 0, 0)
        border_layout.setSpacing(0)
        border_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        border_layout.addWidget(self.border_title_label)
        border_layout.addSpacing(15)
        border_layout.addLayout(border_width_spin_box_layout)
        border_layout.addWidget(self.border_width_spin_box_error)
        border_layout.addSpacing(5)
        border_layout.addLayout(border_color_picker_layout)
        border_layout.addWidget(self.border_color_line_edit_error)
        border_layout.addSpacing(5)

        # layout

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.addLayout(size_layout)
        left_layout.addLayout(color_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.addLayout(margin_layout)
        right_layout.addLayout(padding_layout)
        right_layout.addLayout(border_layout)

        top_layout = QHBoxLayout()
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

        is_valid = is_valid and self.width_spin_box.hasAcceptableInput()
        self.width_spin_box_error.setHidden(self.width_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.height_spin_box.hasAcceptableInput()
        self.height_spin_box_error.setHidden(self.height_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.spacing_spin_box.hasAcceptableInput()
        self.spacing_spin_box_error.setHidden(self.spacing_spin_box.hasAcceptableInput())

        is_valid = (
            is_valid
            and self.page_color_red_spin_box.hasAcceptableInput()
            and self.page_color_green_spin_box.hasAcceptableInput()
            and self.page_color_blue_spin_box.hasAcceptableInput()
        )
        self.color_line_edit_error.setHidden(
            self.page_color_red_spin_box.hasAcceptableInput()
            and self.page_color_green_spin_box.hasAcceptableInput()
            and self.page_color_blue_spin_box.hasAcceptableInput()
        )

        # if not self.indent_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.indent_spin_box_error.show()
        # else:
        #     self.indent_spin_box_error.hide()

        # if not self.line_spacing_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.line_spacing_spin_box_error.show()
        # else:
        #     self.line_spacing_spin_box_error.hide()

        # if not self.top_margin_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.top_margin_spin_box_error.show()
        # else:
        #     self.top_margin_spin_box_error.hide()

        # if not self.bottom_margin_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.bottom_margin_spin_box_error.show()
        # else:
        #     self.bottom_margin_spin_box_error.hide()

        # if not self.left_margin_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.left_margin_spin_box_error.show()
        # else:
        #     self.left_margin_spin_box_error.hide()

        # if not self.right_margin_spin_box.hasAcceptableInput():
        #     is_valid = False
        #     self.right_margin_spin_box_error.show()
        # else:
        #     self.right_margin_spin_box_error.hide()

        return is_valid

    def onPageColorChanged(self, color: QColor) -> None:
        self.page_color_red_spin_box.setValue(color.red())
        self.page_color_green_spin_box.setValue(color.green())
        self.page_color_blue_spin_box.setValue(color.blue())

    def onColorSpinBoxValueChanged(self, _: int) -> None:
        red = self.page_color_red_spin_box.value()
        green = self.page_color_green_spin_box.value()
        blue = self.page_color_blue_spin_box.value()

        self.page_color_picker.setColor(QColor(red, green, blue))
