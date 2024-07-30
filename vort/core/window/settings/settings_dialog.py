from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QTabWidget

from core.window.settings.page_settings import PageSettings, PageSettingsContext
from core.window.settings.paragraph_settings import ParagraphSettings, ParagraphSettingsContext
from core.window.settings.header_settings import HeaderSettings, HeaderSettingsContext
from core.window.settings.footer_settings import FooterSettings, FooterSettingsContext


class SettingsContext:
    def __init__(self) -> None:
        self.page_context: PageSettingsContext = PageSettingsContext()
        self.paragraph_context: ParagraphSettingsContext = ParagraphSettingsContext()
        self.header_context: HeaderSettingsContext = HeaderSettingsContext()
        self.footer_context: FooterSettingsContext = FooterSettingsContext()


class SettingsDialog(QDialog):
    applied = Signal(SettingsContext)

    def __init__(self, context: SettingsContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: SettingsContext = context

        self.setWindowTitle("Settings")
        self.resize(650, 400)

        self.page_settings: PageSettings = PageSettings(self.context.page_context)
        self.paragraph_settings: ParagraphSettings = ParagraphSettings(self.context.paragraph_context)
        self.header_settings: HeaderSettings = HeaderSettings(self.context.header_context)
        self.footer_settings: FooterSettings = FooterSettings(self.context.footer_context)

        self.tab_index = {"page": 0, "paragraph": 1, "header": 2, "footer": 3}

        self.tab_widget: QTabWidget = QTabWidget()
        self.tab_widget.setContentsMargins(50, 50, 50, 50)
        self.tab_widget.addTab(self.page_settings, "Page")
        self.tab_widget.addTab(self.paragraph_settings, "Paragraph")
        self.tab_widget.addTab(self.header_settings, "Header")
        self.tab_widget.addTab(self.footer_settings, "Footer")

        # buttons

        self.apply_button = QPushButton(self)
        self.apply_button.setText("Apply")
        self.apply_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.apply_button.clicked.connect(self.onApplyClicked)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ok_button.clicked.connect(self.onOkClicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_button.clicked.connect(self.onCancelClicked)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def openTab(self, name: str) -> None:
        self.tab_widget.setCurrentIndex(self.tab_index[name])

    @Slot()
    def onApplyClicked(self) -> bool:
        # validate

        invalid_tab: str = ""

        if not self.page_settings.validate() and invalid_tab == "":
            invalid_tab = "page"

        if not self.paragraph_settings.validate() and invalid_tab == "":
            invalid_tab = "paragraph"

        if not self.header_settings.validate() and invalid_tab == "":
            invalid_tab = "header"

        if not self.footer_settings.validate() and invalid_tab == "":
            invalid_tab = "footer"

        # set context

        self.context.page_context.page_width = self.page_settings.width_spin_box.value()
        self.context.page_context.page_height = self.page_settings.height_spin_box.value()
        self.context.page_context.page_spacing = self.page_settings.spacing_spin_box.value()
        self.context.page_context.page_color = self.page_settings.page_color_picker.color()
        self.context.page_context.page_top_margin = self.page_settings.top_margin_spin_box.value()
        self.context.page_context.page_bottom_margin = self.page_settings.bottom_margin_spin_box.value()
        self.context.page_context.page_left_margin = self.page_settings.left_margin_spin_box.value()
        self.context.page_context.page_right_margin = self.page_settings.right_margin_spin_box.value()
        self.context.page_context.page_top_padding = self.page_settings.top_padding_spin_box.value()
        self.context.page_context.page_bottom_padding = self.page_settings.bottom_padding_spin_box.value()
        self.context.page_context.page_left_padding = self.page_settings.left_padding_spin_box.value()
        self.context.page_context.page_right_padding = self.page_settings.right_padding_spin_box.value()
        self.context.page_context.border_width = self.page_settings.border_width_spin_box.value()
        self.context.page_context.border_color = self.page_settings.border_color_picker.color()

        self.context.paragraph_context.alignment = self.paragraph_settings.aligment_flags[
            self.paragraph_settings.alignment_combo_box.currentIndex()
        ]
        self.context.paragraph_context.first_line_indent = self.paragraph_settings.first_line_indent_spin_box.value()
        self.context.paragraph_context.indent = self.paragraph_settings.indent_spin_box.value()
        self.context.paragraph_context.indent_step = self.paragraph_settings.indent_step_spin_box.value()
        self.context.paragraph_context.line_spacing = self.paragraph_settings.line_spacing_spin_box.value()
        self.context.paragraph_context.top_margin = self.paragraph_settings.top_margin_spin_box.value()
        self.context.paragraph_context.bottom_margin = self.paragraph_settings.bottom_margin_spin_box.value()
        self.context.paragraph_context.left_margin = self.paragraph_settings.left_margin_spin_box.value()
        self.context.paragraph_context.right_margin = self.paragraph_settings.right_margin_spin_box.value()

        self.context.header_context.height = self.header_settings.height_spin_box.value()
        self.context.header_context.alignment = HeaderSettingsContext.ALIGNMENT_FLAGS[
            self.header_settings.alignment_combo_box.currentIndex()
        ]
        self.context.header_context.font_family = self.header_settings.font_family_combo_box.fontFamily()
        self.context.header_context.font_size = self.header_settings.font_size_combo_box.fontSize()
        self.context.header_context.text_background_color = self.header_settings.background_color_picker.color()
        self.context.header_context.text_foreground_color = self.header_settings.foreground_color_picker.color()
        self.context.header_context.is_first_page_included = not self.header_settings.first_page_check_box.isChecked()
        self.context.header_context.is_pagination_turned = self.header_settings.pagination_check_box.isChecked()
        self.context.header_context.pagination_starting_number = self.header_settings.starting_number_spin_box.value()
        self.context.header_context.is_text_turned = self.header_settings.text_check_box.isChecked()
        self.context.header_context.text = self.header_settings.text_line_edit.text()

        self.context.footer_context.height = self.footer_settings.height_spin_box.value()
        self.context.footer_context.alignment = FooterSettingsContext.ALIGNMENT_FLAGS[
            self.footer_settings.alignment_combo_box.currentIndex()
        ]
        self.context.footer_context.font_family = self.footer_settings.font_family_combo_box.fontFamily()
        self.context.footer_context.font_size = self.footer_settings.font_size_combo_box.fontSize()
        self.context.footer_context.text_background_color = self.footer_settings.background_color_picker.color()
        self.context.footer_context.text_foreground_color = self.footer_settings.foreground_color_picker.color()
        self.context.footer_context.is_first_page_included = not self.footer_settings.first_page_check_box.isChecked()
        self.context.footer_context.is_pagination_turned = self.footer_settings.pagination_check_box.isChecked()
        self.context.footer_context.pagination_starting_number = self.footer_settings.starting_number_spin_box.value()
        self.context.footer_context.is_text_turned = self.footer_settings.text_check_box.isChecked()
        self.context.footer_context.text = self.footer_settings.text_line_edit.text()

        if invalid_tab == "":
            self.applied.emit(self.context)
            return True
        else:
            self.openTab(invalid_tab)
            return False

    @Slot()
    def onOkClicked(self) -> None:
        if self.onApplyClicked():
            self.accept()

    @Slot()
    def onCancelClicked(self) -> None:
        self.reject()
