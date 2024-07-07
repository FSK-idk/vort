from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QScrollArea, QLineEdit
from PySide6.QtGui import QColor, QPalette, QFont

from core.widget.basic_widget import DoubleSpinBox, ComboBox, SpinBox
from core.widget.font_combo_box.font_combo_box import FontComboBox
from core.widget.font_combo_box.font_size_combo_box import FontSizeComboBox


class FooterSettingsContext:

    def __init__(self) -> None:
        self.height: float = 0  # cm

        self.alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter

        self.font_family: str = QFont().family()
        self.font_size: int = 16
        self.foreground_color: QColor = QColor("black")
        self.background_color: QColor = QColor("white")

        self.is_pagination_turned: bool = False
        self.is_pagination_turned_off_for_first_page: bool = False
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

        # TODO: own widget
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

        self.foreground_color_line_edit_label: QLabel = QLabel(self)
        self.foreground_color_line_edit_label.setText("Foreground color")

        # TODO: add validator #FFFFFF
        self.foreground_color_line_edit: QLineEdit = QLineEdit(self)
        # self.color_line_edit.setValidator()

        # self.color: QColor = QColor("white")
        # TODO: own widget

        # self.color_picker: ColorPicker = ColorPicker(self)
        # connect etc

        self.foreground_color_line_edit_error: QLabel = QLabel(self)
        self.foreground_color_line_edit_error.setText("Invalid input")
        self.foreground_color_line_edit_error.setFixedHeight(10)
        font = self.foreground_color_line_edit_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.foreground_color_line_edit_error.setFont(font)
        self.foreground_color_line_edit_error.hide()

        foreground_color_line_edit_layout = QHBoxLayout()
        foreground_color_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        foreground_color_line_edit_layout.setSpacing(10)
        foreground_color_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        foreground_color_line_edit_layout.addWidget(self.foreground_color_line_edit_label)
        foreground_color_line_edit_layout.addWidget(self.foreground_color_line_edit)
        # color_picker_layout.addWidget(self.color_picker)

        self.background_color_line_edit_label: QLabel = QLabel(self)
        self.background_color_line_edit_label.setText("Background color")

        # TODO: add validator #FFFFFF
        self.background_color_line_edit: QLineEdit = QLineEdit(self)
        # self.color_line_edit.setValidator()

        # self.color: QColor = QColor("white")
        # TODO: own widget

        # self.color_picker: ColorPicker = ColorPicker(self)
        # connect etc

        self.background_color_line_edit_error: QLabel = QLabel(self)
        self.background_color_line_edit_error.setText("Invalid input")
        self.background_color_line_edit_error.setFixedHeight(10)
        font = self.background_color_line_edit_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.background_color_line_edit_error.setFont(font)
        self.background_color_line_edit_error.hide()

        background_color_line_edit_layout = QHBoxLayout()
        background_color_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        background_color_line_edit_layout.setSpacing(10)
        background_color_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        background_color_line_edit_layout.addWidget(self.background_color_line_edit_label)
        background_color_line_edit_layout.addWidget(self.background_color_line_edit)
        # color_picker_layout.addWidget(self.color_picker)

        self.background_color: QColor = QColor("white")

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
        font_layout.addLayout(foreground_color_line_edit_layout)
        font_layout.addWidget(self.foreground_color_line_edit_error)
        font_layout.addSpacing(5)
        font_layout.addLayout(background_color_line_edit_layout)
        font_layout.addWidget(self.background_color_line_edit_error)
        font_layout.addSpacing(5)

        # pagination

        self.pagination_title_label: QLabel = QLabel(self)
        self.pagination_title_label.setText("Pagination")

        self.pagination_check_box: QCheckBox = QCheckBox(self)
        self.pagination_check_box.setText("Turn pagination")
        self.pagination_check_box.setChecked(self.context.is_pagination_turned)
        self.pagination_check_box.stateChanged.connect(self.onPaginationCheckBoxStateChanged)

        self.first_page_pagination_check_box: QCheckBox = QCheckBox(self)
        self.first_page_pagination_check_box.setText("Turn off pagination for the first page")
        self.first_page_pagination_check_box.setChecked(self.context.is_pagination_turned_off_for_first_page)
        self.first_page_pagination_check_box.setEnabled(self.context.is_pagination_turned)
        self.pagination_check_box.stateChanged.connect(self.first_page_pagination_check_box.setEnabled)

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
        pagination_layout.addWidget(self.first_page_pagination_check_box)
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

        # group

        # check_box_group: QButtonGroup = QButtonGroup(self)
        # check_box_group.addButton(self.pagination_check_box)
        # check_box_group.addButton(self.text_check_box)
        # check_box_group.setExclusive(True)

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

    @Slot(int)
    def onPaginationCheckBoxStateChanged(self, state: int) -> None:
        if state:
            self.text_check_box.setChecked(False)

    @Slot(int)
    def onTextCheckBoxStateChanged(self, state: int) -> None:
        if state:
            self.pagination_check_box.setChecked(False)
