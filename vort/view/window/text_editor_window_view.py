from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QComboBox, QMainWindow, QWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import QEvent

from controller.text_editor_controller import TextEditorController
from controller.controller import Controller


class TextEditorWindowView(QMainWindow):
    def __init__(self, controller: Controller, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # self

        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("vort")

        # widget

        self.editor: TextEditorController = TextEditorController(controller=controller)

        self.style_combobox = QComboBox()
        self.font_combobox = QComboBox()
        self.size_combobox = QComboBox()
        self.color_combobox = QComboBox()
        self.background_color_combobox = QComboBox()

        self.setCentralWidget(self.editor.ui)

        # setup

        self.setupAction()
        self.setupMenuBar()
        self.setupToolBar()

    def setupAction(self) -> None:
        # file
        self.new_document_action: QAction = QAction("New")
        self.open_document_action: QAction = QAction("Open")
        self.close_document_action: QAction = QAction("Close")

        self.exit_editor_action: QAction = QAction("Exit")

        # edit
        self.undo_action: QAction = QAction("Undo")
        self.redo_action: QAction = QAction("Redo")

        self.cut_action: QAction = QAction("Cut")
        self.copy_action: QAction = QAction("Copy")
        self.paste_action: QAction = QAction("Paste")

        self.select_all_action: QAction = QAction("Select All")

        self.find_action: QAction = QAction("Find")
        self.find_and_replace_action: QAction = QAction("Find and Replace")

        # insert
        self.insert_image_action: QAction = QAction("Image")
        self.insert_hyperlink_action: QAction = QAction("Hylerlink")

        # format
        self.turn_bold_action: QAction = QAction("Bold")
        self.turn_bold_action.setCheckable(True)
        self.turn_italic_action: QAction = QAction("Italic")
        self.turn_italic_action.setCheckable(True)
        self.turn_underline_action: QAction = QAction("Underline")
        self.turn_underline_action.setCheckable(True)

        self.indent_right_action: QAction = QAction("Right")
        self.indent_left_action: QAction = QAction("Left")

        self.choose_line_spacing_action: QAction = QAction("Line spacing")  # maybe new menu
        self.choose_paragraph_spacing_action: QAction = QAction("Paragraph spacing")  # maybe new menu

        self.turn_pagination_action: QAction = QAction("Pages")
        self.turn_pagination_action.setCheckable(True)

        # style
        self.open_style_action: QAction = QAction("Styles")
        self.clear_style_action: QAction = QAction("Clear")

        # help
        self.show_guide_action: QAction = QAction("Guide")
        self.show_about_action: QAction = QAction("About")

        # TODO: DEBUG
        self.test_action: QAction = QAction("Test")

    def setupMenuBar(self) -> None:
        self.menu_bar = QMenuBar()

        self.file_menu: QMenu = QMenu("File")
        self.file_menu.addAction(self.new_document_action)
        self.file_menu.addAction(self.open_document_action)
        self.file_menu.addAction(self.close_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_editor_action)
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
        self.insert_menu.addAction(self.insert_image_action)
        self.insert_menu.addAction(self.insert_hyperlink_action)
        self.menu_bar.addMenu(self.insert_menu)

        self.format_menu: QMenu = QMenu("Format")
        self.format_menu.addAction(self.turn_bold_action)
        self.format_menu.addAction(self.turn_italic_action)
        self.format_menu.addAction(self.turn_underline_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.indent_right_action)
        self.format_menu.addAction(self.indent_left_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.choose_line_spacing_action)
        self.format_menu.addAction(self.choose_paragraph_spacing_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.turn_pagination_action)
        self.menu_bar.addMenu(self.format_menu)

        self.style_menu: QMenu = QMenu("Style")
        self.style_menu.addAction(self.open_style_action)
        self.menu_bar.addMenu(self.style_menu)

        self.help_menu: QMenu = QMenu("Help")
        self.help_menu.addAction(self.show_guide_action)
        self.help_menu.addAction(self.show_about_action)
        self.menu_bar.addMenu(self.help_menu)

        # TODO: DEBUG
        self.menu_bar.addAction(self.test_action)

        self.setMenuBar(self.menu_bar)

    def setupToolBar(self) -> None:
        self.style_tool: QToolBar = QToolBar("Style")
        self.style_tool.addWidget(self.style_combobox)
        self.style_tool.addAction(self.clear_style_action)
        self.addToolBar(self.style_tool)

        self.font_tool: QToolBar = QToolBar("Font")
        self.font_tool.addWidget(self.font_combobox)
        self.font_tool.addWidget(self.size_combobox)
        self.addToolBar(self.font_tool)

        self.format_tool: QToolBar = QToolBar("Format")
        self.format_tool.addAction(self.turn_bold_action)
        self.format_tool.addAction(self.turn_italic_action)
        self.format_tool.addAction(self.turn_underline_action)
        self.addToolBar(self.format_tool)

        self.color_tool: QToolBar = QToolBar("Color")
        self.color_tool.addWidget(self.color_combobox)
        self.color_tool.addWidget(self.background_color_combobox)
        self.addToolBar(self.color_tool)

        self.indent_tool: QToolBar = QToolBar("Indent")
        self.indent_tool.addAction(self.indent_right_action)
        self.indent_tool.addAction(self.indent_left_action)
        self.addToolBar(self.indent_tool)
