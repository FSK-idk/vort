from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QMainWindow, QWidget
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

        self.setCentralWidget(self.editor.ui)

        # setup

        self.setupAction()
        self.setupMenuBar()
        self.setupToolBar()

    def setupAction(self) -> None:
        self.new_file_action: QAction = QAction("New")
        self.open_file_action: QAction = QAction("Open")
        self.close_file_action: QAction = QAction("Close")
        self.exit_editor_action: QAction = QAction("Exit")

        self.undo_last_action: QAction = QAction("Undo")
        self.redo_last_action: QAction = QAction("Redo")
        self.cut_text_action: QAction = QAction("Cut")
        self.copy_text_action: QAction = QAction("Copy")
        self.paste_text_action: QAction = QAction("Paste")
        self.select_text_action: QAction = QAction("Select")
        self.find_text_action: QAction = QAction("Find")
        self.find_and_replace_text_action: QAction = QAction("Find and Replace")

        self.insert_image_action: QAction = QAction("Image")
        self.insert_hyperlink_action: QAction = QAction("Hylerlink")

        self.show_about_action: QAction = QAction("About")

        self.choose_style_action: QAction = QAction("Style")
        self.clear_style_action: QAction = QAction("Clear")

        self.choose_font_action: QAction = QAction("Font")
        self.choose_font_size_action: QAction = QAction("Size")

        self.bold_text_action: QAction = QAction("Bold")
        self.bold_text_action.setCheckable(True)
        self.italic_text_action: QAction = QAction("Italic")
        self.italic_text_action.setCheckable(True)
        self.underline_text_action: QAction = QAction("Underline")
        self.underline_text_action.setCheckable(True)

        self.color_text_action: QAction = QAction("Color")
        self.bg_color_text_action: QAction = QAction("BG Color")

        self.right_indent_action: QAction = QAction("Right")
        self.left_indent_action: QAction = QAction("Left")

        # TODO: DEBUG
        self.test_action: QAction = QAction("Test")

    def setupMenuBar(self) -> None:
        self.menu_bar = QMenuBar()

        self.file_menu: QMenu = QMenu("File")
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.close_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_editor_action)
        self.menu_bar.addMenu(self.file_menu)

        self.edit_menu: QMenu = QMenu("Edit")
        self.edit_menu.addAction(self.undo_last_action)
        self.edit_menu.addAction(self.redo_last_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_text_action)
        self.edit_menu.addAction(self.copy_text_action)
        self.edit_menu.addAction(self.paste_text_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_text_action)
        self.edit_menu.addAction(self.find_text_action)
        self.edit_menu.addAction(self.find_and_replace_text_action)
        self.menu_bar.addMenu(self.edit_menu)

        self.insert_menu: QMenu = QMenu("Insert")
        self.insert_menu.addAction(self.insert_image_action)
        self.insert_menu.addAction(self.insert_hyperlink_action)
        self.menu_bar.addMenu(self.insert_menu)

        self.help_menu: QMenu = QMenu("Help")
        self.help_menu.addAction(self.show_about_action)
        self.menu_bar.addMenu(self.help_menu)

        # TODO: DEBUG
        self.menu_bar.addAction(self.test_action)

        self.setMenuBar(self.menu_bar)

    def setupToolBar(self) -> None:
        self.style_tool: QToolBar = QToolBar("Style")
        self.style_tool.addAction(self.choose_style_action)
        self.style_tool.addAction(self.clear_style_action)
        self.addToolBar(self.style_tool)

        self.font_tool: QToolBar = QToolBar("Font")
        self.font_tool.addAction(self.choose_font_action)
        self.font_tool.addAction(self.choose_font_size_action)
        self.addToolBar(self.font_tool)

        self.format_tool: QToolBar = QToolBar("Format")
        self.format_tool.addAction(self.bold_text_action)
        self.format_tool.addAction(self.italic_text_action)
        self.format_tool.addAction(self.underline_text_action)
        self.addToolBar(self.format_tool)

        self.color_tool: QToolBar = QToolBar("Color")
        self.color_tool.addAction(self.color_text_action)
        self.color_tool.addAction(self.bg_color_text_action)
        self.addToolBar(self.color_tool)

        self.indent_tool: QToolBar = QToolBar("Indent")
        self.indent_tool.addAction(self.right_indent_action)
        self.indent_tool.addAction(self.left_indent_action)
        self.addToolBar(self.indent_tool)

    def event(self, event: QEvent) -> bool:
        return super().event(event)
