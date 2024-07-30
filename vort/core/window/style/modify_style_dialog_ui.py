from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QColor

from core.window.style.text_style_form import TextStyleForm

from core.widget.text_style.text_style import TextStyle
from data_base.data_base import data_base


class ModifyStyleDialogUI(QDialog):
    def __init__(self, name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Modify style")
        self.resize(650, 450)

        self.old_name = name
        self.style_data: TextStyle = data_base.selectTextStyleData(name)

        self.form: TextStyleForm = TextStyleForm(self.style_data, self)

        # buttons

        self.save_button: QPushButton = QPushButton(self)
        self.save_button.setText("Save")
        self.save_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_button.clicked.connect(self.onSaveClicked)

        self.cancel_button: QPushButton = QPushButton(self)
        self.cancel_button.setText("Close")
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_button.clicked.connect(self.onCancelClicked)

        button_layout: QHBoxLayout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def validate(self) -> bool:
        is_valid = True

        # name

        name: str = self.form.name_line_edit.text()

        is_valid = is_valid and name != ""
        self.form.name_line_edit_error_empty.setHidden(name != "")

        style_data: TextStyle = data_base.selectTextStyleData(name)

        is_valid = is_valid and (style_data.name == "" or style_data.name == self.old_name)
        self.form.name_line_edit_error_exists.setHidden(style_data.name == "" or style_data.name == self.old_name)

        # font

        if self.form.font_check_box.isChecked():
            is_valid = is_valid and self.form.font_family_combo_box.lineEdit().hasAcceptableInput()
            self.form.font_family_combo_box_error.setHidden(
                self.form.font_family_combo_box.lineEdit().hasAcceptableInput()
            )

            is_valid = is_valid and self.form.font_size_combo_box.lineEdit().hasAcceptableInput()
            self.form.font_size_combo_box_error.setHidden(self.form.font_size_combo_box.lineEdit().hasAcceptableInput())

            is_valid = (
                is_valid
                and self.form.background_color_red_spin_box.hasAcceptableInput()
                and self.form.background_color_green_spin_box.hasAcceptableInput()
                and self.form.background_color_blue_spin_box.hasAcceptableInput()
            )
            self.form.background_color_picker_error.setHidden(
                self.form.background_color_red_spin_box.hasAcceptableInput()
                and self.form.background_color_green_spin_box.hasAcceptableInput()
                and self.form.background_color_blue_spin_box.hasAcceptableInput()
            )

            is_valid = (
                is_valid
                and self.form.foreground_color_red_spin_box.hasAcceptableInput()
                and self.form.foreground_color_green_spin_box.hasAcceptableInput()
                and self.form.foreground_color_blue_spin_box.hasAcceptableInput()
            )
            self.form.foreground_color_picker_error.setHidden(
                self.form.foreground_color_red_spin_box.hasAcceptableInput()
                and self.form.foreground_color_green_spin_box.hasAcceptableInput()
                and self.form.foreground_color_blue_spin_box.hasAcceptableInput()
            )

        # paragraph

        if self.form.paragraph_check_box.isChecked():
            is_valid = is_valid and self.form.first_line_indent_spin_box.hasAcceptableInput()
            self.form.first_line_indent_spin_box_error.setHidden(
                self.form.first_line_indent_spin_box.hasAcceptableInput()
            )

            is_valid = is_valid and self.form.indent_spin_box.hasAcceptableInput()
            self.form.indent_spin_box_error.setHidden(self.form.indent_spin_box.hasAcceptableInput())

            is_valid = is_valid and self.form.line_spacing_spin_box.hasAcceptableInput()
            self.form.line_spacing_spin_box_error.setHidden(self.form.line_spacing_spin_box.hasAcceptableInput())

            is_valid = is_valid and self.form.top_margin_spin_box.hasAcceptableInput()
            self.form.top_margin_spin_box_error.setHidden(self.form.top_margin_spin_box.hasAcceptableInput())

            is_valid = is_valid and self.form.bottom_margin_spin_box.hasAcceptableInput()
            self.form.bottom_margin_spin_box_error.setHidden(self.form.bottom_margin_spin_box.hasAcceptableInput())

            is_valid = is_valid and self.form.left_margin_spin_box.hasAcceptableInput()
            self.form.left_margin_spin_box_error.setHidden(self.form.left_margin_spin_box.hasAcceptableInput())

            is_valid = is_valid and self.form.right_margin_spin_box.hasAcceptableInput()
            self.form.right_margin_spin_box_error.setHidden(self.form.right_margin_spin_box.hasAcceptableInput())

        return is_valid

    @Slot()
    def onSaveClicked(self) -> None:
        if self.validate():
            self.style_data.name = self.form.name_line_edit.text()
            self.style_data.is_font_changed = self.form.font_check_box.isChecked()
            self.style_data.font_family = self.form.font_family_combo_box.fontFamily()
            self.style_data.font_size = self.form.font_size_combo_box.fontSize()

            red = self.form.background_color_picker.color().red()
            green = self.form.background_color_picker.color().green()
            blue = self.form.background_color_picker.color().blue()
            alpha = self.form.background_color_picker.color().alpha()
            self.style_data.background_color = QColor(red, green, blue, alpha)

            red = self.form.foreground_color_picker.color().red()
            green = self.form.foreground_color_picker.color().green()
            blue = self.form.foreground_color_picker.color().blue()
            alpha = self.form.foreground_color_picker.color().alpha()
            self.style_data.foreground_color = QColor(red, green, blue, alpha)

            self.style_data.is_bold = self.form.bold_check_box.isChecked()
            self.style_data.is_italic = self.form.italic_check_box.isChecked()
            self.style_data.is_underlined = self.form.underlined_check_box.isChecked()
            self.style_data.is_paragraph_changed = self.form.paragraph_check_box.isChecked()
            self.style_data.alignment = self.form.aligment_flags[self.form.alignment_combo_box.currentIndex()]
            self.style_data.first_line_indent = self.form.first_line_indent_spin_box.value()
            self.style_data.indent = self.form.indent_spin_box.value()
            self.style_data.line_spacing = self.form.line_spacing_spin_box.value()
            self.style_data.top_margin = self.form.top_margin_spin_box.value()
            self.style_data.bottom_margin = self.form.bottom_margin_spin_box.value()
            self.style_data.left_margin = self.form.left_margin_spin_box.value()
            self.style_data.right_margin = self.form.right_margin_spin_box.value()

            data_base.updateTextStyle(self.old_name, self.style_data)

            self.accept()

    @Slot()
    def onCancelClicked(self) -> None:
        self.reject()
