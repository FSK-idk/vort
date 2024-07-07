from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QScrollArea, QLineEdit
from PySide6.QtGui import QColor, QPalette, QFont

from core.widget.basic_widget import DoubleSpinBox, ComboBox, SpinBox
from core.widget.font_combo_box.font_combo_box import FontComboBox
from core.widget.font_combo_box.font_size_combo_box import FontSizeComboBox
from core.widget.color_picker.color_picker import ColorPicker


class FooterSettingsContext:

    def __init__(self) -> None:
        self.height: float = 0.0  # cm

        self.alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom

        self.font_family: str = ""
        self.font_size: int = 0
        self.background_color: QColor = QColor()
        self.foreground_color: QColor = QColor()

        self.is_turned_for_first_page: bool = False

        self.is_pagination_turned: bool = False
        self.starting_number: int = 1

        self.is_text_turned: bool = False
        self.text: str = ""


class FooterSettingsUI(QScrollArea):
    def __init__(self, context: FooterSettingsContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: FooterSettingsContext = context
        self.setWidgetResizable(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("transparent"))
        palette.setColor(QPalette.ColorRole.Base, palette.color(QPalette.ColorRole.Base))
        self.setPalette(palette)

        # size

        self.size_title_label: QLabel = QLabel(self)
        self.size_title_label.setText("Size")

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

        size_layout = QVBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(0)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        size_layout.addWidget(self.size_title_label)
        size_layout.addSpacing(15)
        size_layout.addLayout(height_spin_box_layout)
        size_layout.addWidget(self.height_spin_box_error)
        size_layout.addSpacing(5)

        # alignment

        self.alignment_title_label: QLabel = QLabel(self)
        self.alignment_title_label.setText("Alignment")

        self.alignment_combo_box_label: QLabel = QLabel(self)
        self.alignment_combo_box_label.setText("Alignment")

        self.alignment_combo_box: ComboBox = ComboBox(self)
        self.alignment_combo_box.setEditable(True)
        self.alignment_combo_box.lineEdit().setEnabled(False)
        # fmt: off
        self.aligment_flags: list[Qt.AlignmentFlag] = [
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,     Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,     Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,     
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, 
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,  Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,  Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,  
        ]
        self.aligment_names: list[str] = [
            "Top Left",    "Top Center",    "Top Right",
            "Center Left", "Center",        "Center Right",
            "Bottom Left", "Bottom Center", "Bottom Right",
        ]
        # fmt: on
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

        # font

        self.font_title_label: QLabel = QLabel(self)
        self.font_title_label.setText("Font")

        self.font_family_combo_box_label: QLabel = QLabel(self)
        self.font_family_combo_box_label.setText("Family")

        self.font_family_combo_box: FontComboBox = FontComboBox(self)
        self.font_family_combo_box.setFont(context.font_family)

        self.font_family_combo_box_error: QLabel = QLabel(self)
        self.font_family_combo_box_error.setText("Invalid input")
        self.font_family_combo_box_error.setFixedHeight(10)
        font = self.font_family_combo_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.font_family_combo_box_error.setFont(font)
        self.font_family_combo_box_error.hide()

        font_family_combo_box_layout = QHBoxLayout()
        font_family_combo_box_layout.setContentsMargins(0, 0, 0, 0)
        font_family_combo_box_layout.setSpacing(10)
        font_family_combo_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font_family_combo_box_layout.addWidget(self.font_family_combo_box_label)
        font_family_combo_box_layout.addWidget(self.font_family_combo_box)

        self.font_size_combo_box_label: QLabel = QLabel(self)
        self.font_size_combo_box_label.setText("Size")

        self.font_size_combo_box: FontSizeComboBox = FontSizeComboBox(self)
        self.font_size_combo_box.setFontSize(context.font_size)

        self.font_size_combo_box_error: QLabel = QLabel(self)
        self.font_size_combo_box_error.setText("Invalid input")
        self.font_size_combo_box_error.setFixedHeight(10)
        font = self.font_size_combo_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.font_size_combo_box_error.setFont(font)
        self.font_size_combo_box_error.hide()

        font_size_combo_box_layout = QHBoxLayout()
        font_size_combo_box_layout.setContentsMargins(0, 0, 0, 0)
        font_size_combo_box_layout.setSpacing(10)
        font_size_combo_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font_size_combo_box_layout.addWidget(self.font_size_combo_box_label)
        font_size_combo_box_layout.addWidget(self.font_size_combo_box)

        self.background_color_picker_label: QLabel = QLabel(self)
        self.background_color_picker_label.setText("Background color")

        self.background_color_red_spin_box: SpinBox = SpinBox(self)
        self.background_color_red_spin_box.setMinimum(0)
        self.background_color_red_spin_box.setMaximum(255)
        self.background_color_red_spin_box.setSuffix(" R")
        self.background_color_red_spin_box.setValue(self.context.background_color.red())
        self.background_color_red_spin_box.valueChanged.connect(self.onBackgroundColorSpinBoxValueChanged)

        self.background_color_green_spin_box: SpinBox = SpinBox(self)
        self.background_color_green_spin_box.setMinimum(0)
        self.background_color_green_spin_box.setMaximum(255)
        self.background_color_green_spin_box.setSuffix(" G")
        self.background_color_green_spin_box.setValue(self.context.background_color.green())
        self.background_color_green_spin_box.valueChanged.connect(self.onBackgroundColorSpinBoxValueChanged)

        self.background_color_blue_spin_box: SpinBox = SpinBox(self)
        self.background_color_blue_spin_box.setMinimum(0)
        self.background_color_blue_spin_box.setMaximum(255)
        self.background_color_blue_spin_box.setSuffix(" B")
        self.background_color_blue_spin_box.setValue(self.context.background_color.blue())
        self.background_color_blue_spin_box.valueChanged.connect(self.onBackgroundColorSpinBoxValueChanged)

        self.background_color_picker: ColorPicker = ColorPicker(self)
        self.background_color_picker.setColor(self.context.background_color)
        background_color_picker_palette = self.background_color_picker.ui.palette()
        background_color_picker_palette.setColor(QPalette.ColorRole.Button, palette.color(QPalette.ColorRole.Base))
        background_color_picker_palette.setColor(QPalette.ColorRole.Window, palette.color(QPalette.ColorRole.Base))
        self.background_color_picker.ui.setPalette(background_color_picker_palette)
        self.background_color_picker.colorChanged.connect(self.onBackgroundColorChanged)

        self.background_color_picker_error: QLabel = QLabel(self)
        self.background_color_picker_error.setText("Invalid input")
        self.background_color_picker_error.setFixedHeight(10)
        font = self.background_color_picker_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.background_color_picker_error.setFont(font)
        self.background_color_picker_error.hide()

        background_color_picker_layout = QHBoxLayout()
        background_color_picker_layout.setContentsMargins(0, 0, 0, 0)
        background_color_picker_layout.setSpacing(10)
        background_color_picker_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        background_color_picker_layout.addWidget(self.background_color_picker_label)
        background_color_picker_layout.addWidget(self.background_color_red_spin_box)
        background_color_picker_layout.addWidget(self.background_color_green_spin_box)
        background_color_picker_layout.addWidget(self.background_color_blue_spin_box)
        background_color_picker_layout.addWidget(self.background_color_picker.ui)

        self.foreground_color_picker_label: QLabel = QLabel(self)
        self.foreground_color_picker_label.setText("Foreground color")

        self.foreground_color_red_spin_box: SpinBox = SpinBox(self)
        self.foreground_color_red_spin_box.setMinimum(0)
        self.foreground_color_red_spin_box.setMaximum(255)
        self.foreground_color_red_spin_box.setSuffix(" R")
        self.foreground_color_red_spin_box.setValue(self.context.foreground_color.red())
        self.foreground_color_red_spin_box.valueChanged.connect(self.onForegroundColorSpinBoxValueChanged)

        self.foreground_color_green_spin_box: SpinBox = SpinBox(self)
        self.foreground_color_green_spin_box.setMinimum(0)
        self.foreground_color_green_spin_box.setMaximum(255)
        self.foreground_color_green_spin_box.setSuffix(" G")
        self.foreground_color_green_spin_box.setValue(self.context.foreground_color.green())
        self.foreground_color_green_spin_box.valueChanged.connect(self.onForegroundColorSpinBoxValueChanged)

        self.foreground_color_blue_spin_box: SpinBox = SpinBox(self)
        self.foreground_color_blue_spin_box.setMinimum(0)
        self.foreground_color_blue_spin_box.setMaximum(255)
        self.foreground_color_blue_spin_box.setSuffix(" B")
        self.foreground_color_blue_spin_box.setValue(self.context.foreground_color.blue())
        self.foreground_color_blue_spin_box.valueChanged.connect(self.onForegroundColorSpinBoxValueChanged)

        self.foreground_color_picker: ColorPicker = ColorPicker(self)
        self.foreground_color_picker.setColor(self.context.foreground_color)
        foreground_color_picker_palette = self.foreground_color_picker.ui.palette()
        foreground_color_picker_palette.setColor(QPalette.ColorRole.Button, palette.color(QPalette.ColorRole.Base))
        foreground_color_picker_palette.setColor(QPalette.ColorRole.Window, palette.color(QPalette.ColorRole.Base))
        self.foreground_color_picker.ui.setPalette(foreground_color_picker_palette)
        self.foreground_color_picker.colorChanged.connect(self.onForegroundColorChanged)

        self.foreground_color_picker_error: QLabel = QLabel(self)
        self.foreground_color_picker_error.setText("Invalid input")
        self.foreground_color_picker_error.setFixedHeight(10)
        font = self.foreground_color_picker_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.foreground_color_picker_error.setFont(font)
        self.foreground_color_picker_error.hide()

        foreground_color_picker_layout = QHBoxLayout()
        foreground_color_picker_layout.setContentsMargins(0, 0, 0, 0)
        foreground_color_picker_layout.setSpacing(10)
        foreground_color_picker_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        foreground_color_picker_layout.addWidget(self.foreground_color_picker_label)
        foreground_color_picker_layout.addWidget(self.foreground_color_red_spin_box)
        foreground_color_picker_layout.addWidget(self.foreground_color_green_spin_box)
        foreground_color_picker_layout.addWidget(self.foreground_color_blue_spin_box)
        foreground_color_picker_layout.addWidget(self.foreground_color_picker.ui)

        font_layout = QVBoxLayout()
        font_layout.setContentsMargins(0, 0, 0, 0)
        font_layout.setSpacing(0)
        font_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        font_layout.addWidget(self.font_title_label)
        font_layout.addSpacing(15)
        font_layout.addLayout(font_family_combo_box_layout)
        font_layout.addWidget(self.font_family_combo_box_error)
        font_layout.addSpacing(5)
        font_layout.addLayout(font_size_combo_box_layout)
        font_layout.addWidget(self.font_size_combo_box_error)
        font_layout.addSpacing(5)
        font_layout.addLayout(background_color_picker_layout)
        font_layout.addWidget(self.background_color_picker_error)
        font_layout.addSpacing(5)
        font_layout.addLayout(foreground_color_picker_layout)
        font_layout.addWidget(self.foreground_color_picker_error)
        font_layout.addSpacing(5)

        # first page

        self.first_page_title_label: QLabel = QLabel(self)
        self.first_page_title_label.setText("First page")

        self.first_page_check_box: QCheckBox = QCheckBox(self)
        self.first_page_check_box.setText("Turn off footer for the first page")
        self.first_page_check_box.setChecked(not self.context.is_turned_for_first_page)

        first_page_layout = QVBoxLayout()
        first_page_layout.setContentsMargins(0, 0, 0, 0)
        first_page_layout.setSpacing(0)
        first_page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        first_page_layout.addWidget(self.first_page_title_label)
        first_page_layout.addSpacing(15)
        first_page_layout.addWidget(self.first_page_check_box)
        first_page_layout.addSpacing(5)

        # pagination

        self.pagination_title_label: QLabel = QLabel(self)
        self.pagination_title_label.setText("Pagination")

        self.pagination_check_box: QCheckBox = QCheckBox(self)
        self.pagination_check_box.setText("Turn pagination")
        self.pagination_check_box.setChecked(self.context.is_pagination_turned)
        self.pagination_check_box.stateChanged.connect(self.onPaginationCheckBoxStateChanged)

        self.starting_number_spin_box_label: QLabel = QLabel(self)
        self.starting_number_spin_box_label.setText("Starting number")

        self.starting_number_spin_box: SpinBox = SpinBox(self)
        self.starting_number_spin_box.setMinimum(0)
        self.starting_number_spin_box.setSingleStep(1)
        self.starting_number_spin_box.setValue(self.context.starting_number)
        self.starting_number_spin_box.setEnabled(self.context.is_pagination_turned)
        self.pagination_check_box.stateChanged.connect(self.starting_number_spin_box.setEnabled)

        self.starting_number_spin_box_error: QLabel = QLabel(self)
        self.starting_number_spin_box_error.setText("Invalid input")
        self.starting_number_spin_box_error.setFixedHeight(10)
        font = self.starting_number_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.starting_number_spin_box_error.setFont(font)
        self.starting_number_spin_box_error.hide()

        starting_number_spin_box_layout = QHBoxLayout()
        starting_number_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        starting_number_spin_box_layout.setSpacing(10)
        starting_number_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        starting_number_spin_box_layout.addWidget(self.starting_number_spin_box_label)
        starting_number_spin_box_layout.addWidget(self.starting_number_spin_box)

        pagination_layout = QVBoxLayout()
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        pagination_layout.setSpacing(0)
        pagination_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        pagination_layout.addWidget(self.pagination_title_label)
        pagination_layout.addSpacing(15)
        pagination_layout.addWidget(self.pagination_check_box)
        pagination_layout.addSpacing(5)
        pagination_layout.addLayout(starting_number_spin_box_layout)
        pagination_layout.addWidget(self.starting_number_spin_box_error)
        pagination_layout.addSpacing(5)

        # text

        self.text_title_label: QLabel = QLabel(self)
        self.text_title_label.setText("Text")

        self.text_check_box: QCheckBox = QCheckBox(self)
        self.text_check_box.setText("Turn text")
        self.text_check_box.setChecked(self.context.is_text_turned)
        self.text_check_box.stateChanged.connect(self.onTextCheckBoxStateChanged)

        self.text_line_edit_label: QLabel = QLabel(self)
        self.text_line_edit_label.setText("Text")

        self.text_line_edit: QLineEdit = QLineEdit(self)
        self.text_line_edit.setEnabled(self.context.is_text_turned)
        self.text_line_edit.setText(self.context.text)
        self.text_check_box.stateChanged.connect(self.text_line_edit.setEnabled)

        text_line_edit_layout = QHBoxLayout()
        text_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        text_line_edit_layout.setSpacing(10)
        text_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        text_line_edit_layout.addWidget(self.text_line_edit_label)
        text_line_edit_layout.addWidget(self.text_line_edit)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        text_layout.addWidget(self.text_title_label)
        text_layout.addSpacing(15)
        text_layout.addWidget(self.text_check_box)
        text_layout.addSpacing(5)
        text_layout.addLayout(text_line_edit_layout)
        text_layout.addSpacing(5)

        # layout

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.addLayout(size_layout)
        left_layout.addLayout(alignment_layout)
        left_layout.addLayout(font_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.addLayout(first_page_layout)
        right_layout.addLayout(pagination_layout)
        right_layout.addLayout(text_layout)

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

        is_valid = is_valid and self.height_spin_box.hasAcceptableInput()
        self.height_spin_box_error.setHidden(self.height_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.font_family_combo_box.lineEdit().hasAcceptableInput()
        self.font_family_combo_box_error.setHidden(self.font_family_combo_box.lineEdit().hasAcceptableInput())

        is_valid = is_valid and self.font_size_combo_box.lineEdit().hasAcceptableInput()
        self.font_size_combo_box_error.setHidden(self.font_size_combo_box.lineEdit().hasAcceptableInput())

        is_valid = (
            is_valid
            and self.background_color_red_spin_box.hasAcceptableInput()
            and self.background_color_green_spin_box.hasAcceptableInput()
            and self.background_color_blue_spin_box.hasAcceptableInput()
        )
        self.background_color_picker_error.setHidden(
            self.background_color_red_spin_box.hasAcceptableInput()
            and self.background_color_green_spin_box.hasAcceptableInput()
            and self.background_color_blue_spin_box.hasAcceptableInput()
        )

        is_valid = (
            is_valid
            and self.foreground_color_red_spin_box.hasAcceptableInput()
            and self.foreground_color_green_spin_box.hasAcceptableInput()
            and self.foreground_color_blue_spin_box.hasAcceptableInput()
        )
        self.foreground_color_picker_error.setHidden(
            self.foreground_color_red_spin_box.hasAcceptableInput()
            and self.foreground_color_green_spin_box.hasAcceptableInput()
            and self.foreground_color_blue_spin_box.hasAcceptableInput()
        )

        if self.pagination_check_box.isChecked():
            is_valid = is_valid and self.starting_number_spin_box.hasAcceptableInput()
            self.starting_number_spin_box_error.setHidden(self.starting_number_spin_box.hasAcceptableInput())

        return is_valid

    @Slot(int)
    def onPaginationCheckBoxStateChanged(self, state: int) -> None:
        if state:
            self.text_check_box.setChecked(False)

    @Slot(int)
    def onTextCheckBoxStateChanged(self, state: int) -> None:
        if state:
            self.pagination_check_box.setChecked(False)

    @Slot(QColor)
    def onBackgroundColorChanged(self, color: QColor) -> None:
        self.background_color_red_spin_box.setValue(color.red())
        self.background_color_green_spin_box.setValue(color.green())
        self.background_color_blue_spin_box.setValue(color.blue())

    @Slot(int)
    def onBackgroundColorSpinBoxValueChanged(self, _: int) -> None:
        red = self.background_color_red_spin_box.value()
        green = self.background_color_green_spin_box.value()
        blue = self.background_color_blue_spin_box.value()

        self.background_color_picker.setColor(QColor(red, green, blue))

    @Slot(QColor)
    def onForegroundColorChanged(self, color: QColor) -> None:
        self.foreground_color_red_spin_box.setValue(color.red())
        self.foreground_color_green_spin_box.setValue(color.green())
        self.foreground_color_blue_spin_box.setValue(color.blue())

    @Slot(int)
    def onForegroundColorSpinBoxValueChanged(self, _: int) -> None:
        red = self.foreground_color_red_spin_box.value()
        green = self.foreground_color_green_spin_box.value()
        blue = self.foreground_color_blue_spin_box.value()

        self.foreground_color_picker.setColor(QColor(red, green, blue))
