from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QComboBox, QMainWindow, QWidget, QStatusBar
from PySide6.QtGui import QAction, QPixmap, QColor, QActionGroup, QCloseEvent

from core.widget.color_picker.color_picker import ColorPicker
from core.widget.font_combo_box.font_size_combo_box import FontSizeComboBox
from core.widget.font_combo_box.font_combo_box import FontComboBox

from core.widget.status_bar_widget.character_count_label import CharacterCountLabel
from core.widget.status_bar_widget.zoom_slider import ZoomSlider

from core.text_editor.text_editor import TextEditor


class TextEditorWindowUI(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # self

        self.setGeometry(0, 0, 900, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("vort")

        # widget

        self.text_editor: TextEditor = TextEditor(self)
        self.setCentralWidget(self.text_editor.ui)

        # setup

        self.setupAction()
        self.setupWidget()
        self.setupMenuBar()
        self.setupToolBar()
        self.setupStatusBar()

    def setupAction(self) -> None:
        # app

        self.exit_application_action: QAction = QAction("Exit")
        self.exit_application_action.setStatusTip("Exit the application")
        self.exit_application_action.setShortcut("Ctrl+Q")

        # file

        self.new_document_action: QAction = QAction("New")
        self.new_document_action.setStatusTip("Create a document")
        self.new_document_action.setShortcut("Ctrl+N")

        self.open_document_action: QAction = QAction("Open")
        self.open_document_action.setStatusTip("Open a document")
        self.open_document_action.setShortcut("Ctrl+O")

        self.close_document_action: QAction = QAction("Close")
        self.close_document_action.setStatusTip("Close the document")
        self.close_document_action.setShortcut("Ctrl+W")

        self.save_document_action: QAction = QAction("Save")
        self.save_document_action.setStatusTip("Save the document")
        self.save_document_action.setShortcut("Ctrl+S")

        # history

        self.undo_action: QAction = QAction("Undo")
        self.undo_action.setStatusTip("Undo the last action")
        self.undo_action.setShortcut("Ctrl+Z")

        self.redo_action: QAction = QAction("Redo")
        self.redo_action.setStatusTip("Redo the last action")
        self.redo_action.setShortcut("Ctrl+Y")

        # copy paste

        self.cut_action: QAction = QAction("Cut")
        self.cut_action.setStatusTip("Cut the selected text")
        self.cut_action.setShortcut("Ctrl+X")

        self.copy_action: QAction = QAction("Copy")
        self.copy_action.setStatusTip("Copy the selected text")
        self.copy_action.setShortcut("Ctrl+C")

        self.paste_action: QAction = QAction("Paste")
        self.paste_action.setStatusTip("Paste text from the clipboard")
        self.paste_action.setShortcut("Ctrl+V")

        # select

        self.select_all_action: QAction = QAction("Select All")
        self.select_all_action.setStatusTip("Select the entire document")
        self.select_all_action.setShortcut("Ctrl+A")

        # search

        self.find_action: QAction = QAction("Find")
        self.find_action.setStatusTip("Find a word in the document")
        self.find_action.setShortcut("Ctrl+F")

        self.find_and_replace_action: QAction = QAction("Find and Replace")
        self.find_and_replace_action.setStatusTip("Find and replace a word in the document")
        self.find_and_replace_action.setShortcut("Ctrl+H")

        # insert

        self.insert_text_action: QAction = QAction("Text")
        self.insert_text_action.setStatusTip("Insert text")

        self.insert_plain_text_action: QAction = QAction("Plain text")
        self.insert_plain_text_action.setStatusTip("Insert plain text")
        self.insert_plain_text_action.setShortcut("Ctrl+Shift+V")

        self.insert_image_action: QAction = QAction("Image")
        self.insert_image_action.setStatusTip("Insert an image")

        self.insert_hyperlink_action: QAction = QAction("Hylerlink")
        self.insert_hyperlink_action.setStatusTip("Insert a hyperlink")

        # format

        self.turn_bold_action: QAction = QAction("Bold")
        self.turn_bold_action.setCheckable(True)
        self.turn_bold_action.setStatusTip("Make the selected text bold")
        self.turn_bold_action.setShortcut("Ctrl+B")

        self.turn_italic_action: QAction = QAction("Italic")
        self.turn_italic_action.setCheckable(True)
        self.turn_italic_action.setStatusTip("Make the selected text italic")
        self.turn_italic_action.setShortcut("Ctrl+I")

        self.turn_underlined_action: QAction = QAction("Underlined")
        self.turn_underlined_action.setCheckable(True)
        self.turn_underlined_action.setStatusTip("Make the selected text underlined")
        self.turn_underlined_action.setShortcut("Ctrl+U")

        # indent

        self.indent_right_action: QAction = QAction("Right")
        self.indent_right_action.setStatusTip("Indent right")
        self.indent_right_action.setShortcut("Ctrl+]")

        self.indent_left_action: QAction = QAction("Left")
        self.indent_left_action.setStatusTip("Indent left")
        self.indent_left_action.setShortcut("Ctrl+[")

        # space

        self.set_line_spacing_1_action: QAction = QAction("1 line spacing")
        self.set_line_spacing_1_action.setCheckable(True)
        self.set_line_spacing_1_action.setStatusTip("Set the spacing between lines to 1")

        self.set_line_spacing_1_15_action: QAction = QAction("1.15 line spacing")
        self.set_line_spacing_1_15_action.setCheckable(True)
        self.set_line_spacing_1_15_action.setStatusTip("Set the spacing between lines to 1.15")

        self.set_line_spacing_1_5_action: QAction = QAction("1.5 line spacing")
        self.set_line_spacing_1_5_action.setCheckable(True)
        self.set_line_spacing_1_5_action.setStatusTip("Set the spacing between lines to 1.5")

        self.set_line_spacing_2_action: QAction = QAction("2 line spacing")
        self.set_line_spacing_2_action.setCheckable(True)
        self.set_line_spacing_2_action.setStatusTip("Set the spacing between lines to 2")

        self.line_space_group: QActionGroup = QActionGroup(self)
        self.line_space_group.addAction(self.set_line_spacing_1_action)
        self.line_space_group.addAction(self.set_line_spacing_1_15_action)
        self.line_space_group.addAction(self.set_line_spacing_1_5_action)
        self.line_space_group.addAction(self.set_line_spacing_2_action)
        self.line_space_group.setExclusive(True)

        # style

        self.open_style_action: QAction = QAction("Styles")
        self.open_style_action.setStatusTip("Manage custom styles")

        self.new_style_action: QAction = QAction("New style")
        self.new_style_action.setStatusTip("Create new custom style")

        self.clear_style_action: QAction = QAction("Clear")
        self.clear_style_action.setStatusTip("Clear the style of the selected text")

        # settings

        self.open_page_settings: QAction = QAction("Page")
        self.open_page_settings.setStatusTip("Open page settings")

        self.open_paragraph_settings: QAction = QAction("Paragraph")
        self.open_paragraph_settings.setStatusTip("Open paragraph settings")

        self.open_header_settings: QAction = QAction("Header")
        self.open_header_settings.setStatusTip("Open header settings")

        self.open_footer_settings: QAction = QAction("Footer")
        self.open_footer_settings.setStatusTip("Open footer settings")

        # help

        self.show_guide_action: QAction = QAction("Guide")
        self.show_guide_action.setStatusTip("View the user's guide")
        self.show_guide_action.setShortcut("F1")

        self.show_about_action: QAction = QAction("About")
        self.show_about_action.setStatusTip("View application information")

        # TODO: DEBUG
        self.test_action: QAction = QAction("Test")
        self.test_action.setStatusTip("Test")

        self.test2_action: QAction = QAction("Test2")
        self.test2_action.setStatusTip("Test2")

    def setupWidget(self) -> None:

        # font

        self.font_family_combo_box = FontComboBox()

        self.font_size_combo_box = FontSizeComboBox()

        # color
        icon = QPixmap(16, 16)
        icon.fill(QColor("cyan"))

        self.foreground_color_picker = ColorPicker(self)
        self.foreground_color_picker.ui.setIcon(icon)
        self.foreground_color_picker.ui.setColorIcon(QColor("black"))

        self.background_color_picker = ColorPicker(self)
        self.background_color_picker.ui.setIcon(icon)
        self.background_color_picker.ui.setColorIcon(QColor("transparent"))

        # style

        self.style_combobox = QComboBox()  # TODO:

    def setupMenuBar(self) -> None:
        self.menu_bar = QMenuBar()

        self.file_menu: QMenu = QMenu("File")
        self.file_menu.addAction(self.new_document_action)
        self.file_menu.addAction(self.open_document_action)
        self.file_menu.addAction(self.close_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_application_action)
        self.menu_bar.addMenu(self.file_menu)

        self.edit_menu: QMenu = QMenu("Edit")
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_all_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.find_action)
        self.edit_menu.addAction(self.find_and_replace_action)
        self.menu_bar.addMenu(self.edit_menu)

        self.insert_menu: QMenu = QMenu("Insert")
        self.insert_menu.addAction(self.insert_text_action)
        self.insert_menu.addAction(self.insert_plain_text_action)
        self.insert_menu.addAction(self.insert_image_action)
        self.insert_menu.addAction(self.insert_hyperlink_action)
        self.menu_bar.addMenu(self.insert_menu)

        self.line_space_menu: QMenu = QMenu("Line spacing")
        self.line_space_menu.addAction(self.set_line_spacing_1_action)
        self.line_space_menu.addAction(self.set_line_spacing_1_15_action)
        self.line_space_menu.addAction(self.set_line_spacing_1_5_action)
        self.line_space_menu.addAction(self.set_line_spacing_2_action)

        self.format_menu: QMenu = QMenu("Format")
        self.format_menu.addAction(self.turn_bold_action)
        self.format_menu.addAction(self.turn_italic_action)
        self.format_menu.addAction(self.turn_underlined_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.indent_right_action)
        self.format_menu.addAction(self.indent_left_action)
        self.format_menu.addSeparator()
        self.format_menu.addMenu(self.line_space_menu)
        self.menu_bar.addMenu(self.format_menu)

        self.style_menu: QMenu = QMenu("Style")
        self.style_menu.addAction(self.open_style_action)
        self.style_menu.addAction(self.new_style_action)
        self.menu_bar.addMenu(self.style_menu)

        self.settings_menu: QMenu = QMenu("Settings")
        self.settings_menu.addAction(self.open_page_settings)
        self.settings_menu.addAction(self.open_paragraph_settings)
        self.settings_menu.addAction(self.open_header_settings)
        self.settings_menu.addAction(self.open_footer_settings)
        self.menu_bar.addMenu(self.settings_menu)

        self.help_menu: QMenu = QMenu("Help")
        self.help_menu.addAction(self.show_guide_action)
        self.help_menu.addAction(self.show_about_action)
        self.menu_bar.addMenu(self.help_menu)

        # TODO: DEBUG
        self.menu_bar.addAction(self.test_action)
        self.menu_bar.addAction(self.test2_action)

        self.setMenuBar(self.menu_bar)

    def setupToolBar(self) -> None:
        self.style_tool: QToolBar = QToolBar("Style")
        self.style_tool.addWidget(self.style_combobox)
        self.style_tool.addAction(self.clear_style_action)
        self.addToolBar(self.style_tool)

        self.font_tool: QToolBar = QToolBar("Font")
        self.font_tool.addWidget(self.font_family_combo_box)
        self.font_tool.addWidget(self.font_size_combo_box)
        self.addToolBar(self.font_tool)

        self.format_tool: QToolBar = QToolBar("Format")
        self.format_tool.addAction(self.turn_bold_action)
        self.format_tool.addAction(self.turn_italic_action)
        self.format_tool.addAction(self.turn_underlined_action)
        self.addToolBar(self.format_tool)

        self.color_tool: QToolBar = QToolBar("Color")
        self.color_tool.addWidget(self.foreground_color_picker.ui)
        self.color_tool.addWidget(self.background_color_picker.ui)
        self.addToolBar(self.color_tool)

        self.indent_tool: QToolBar = QToolBar("Indent")
        self.indent_tool.addAction(self.indent_right_action)
        self.indent_tool.addAction(self.indent_left_action)
        self.addToolBar(self.indent_tool)

    def setupStatusBar(self) -> None:
        self.status_bar: QStatusBar = QStatusBar()

        self.character_count: CharacterCountLabel = CharacterCountLabel()
        self.status_bar.addPermanentWidget(self.character_count)

        self.zoom_slider: ZoomSlider = ZoomSlider(self)
        self.status_bar.addPermanentWidget(self.zoom_slider)

        self.setStatusBar(self.status_bar)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.exit_application_action.triggered.emit()
