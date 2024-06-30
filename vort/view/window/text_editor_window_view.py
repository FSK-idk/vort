from PySide6.QtWidgets import (
    QMenuBar,
    QMenu,
    QToolBar,
    QComboBox,
    QMainWindow,
    QWidget,
    QStatusBar,
    QLabel,
    QFontComboBox,
    QLineEdit,
    QColorDialog,
    QCompleter,
)
from PySide6.QtGui import QAction, QPixmap, QRegularExpressionValidator, QColor
from PySide6.QtCore import QEvent, QObject, Qt, QRegularExpression, QRegularExpressionMatch

from controller.text_editor_controller import TextEditorController

from view.widget.color_picker import ColorPicker


class TextEditorWindowView(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # self

        self.setGeometry(0, 0, 900, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("vort")

        # widget

        self.editor: TextEditorController = TextEditorController()

        self.style_combobox = QComboBox()
        self.font_combobox = QFontComboBox()
        self.size_combobox = QComboBox()

        self.size_combobox.setEditable(True)
        self.size_combobox.setCompleter(QCompleter())
        self.size_combobox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.size_combobox.lineEdit().setValidator(QRegularExpressionValidator("[1-9][0-9]?( pt)?$"))
        default_sizes = [6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 36, 42, 48]
        self.size_combobox.addItems([str(size) + " pt" for size in default_sizes])
        self.no_point_re: QRegularExpression = QRegularExpression("[1-9][0-9]?$")
        self.size_combobox.lineEdit().returnPressed.connect(self.addPointSuffix)

        self.color_picker = ColorPicker("Color")
        self.background_color_picker = ColorPicker("Bg Color")

        self.setCentralWidget(self.editor.ui)

        # setup

        self.setupAction()
        self.setupMenuBar()
        self.setupToolBar()
        self.setupStatusBar()

    def setupAction(self) -> None:
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

        self.exit_editor_action: QAction = QAction("Exit")
        self.exit_editor_action.setStatusTip("Exit the application")
        self.exit_editor_action.setShortcut("Ctrl+Q")

        # edit
        self.undo_action: QAction = QAction("Undo")
        self.undo_action.setStatusTip("Undo the last action")
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action: QAction = QAction("Redo")
        self.redo_action.setStatusTip("Redo the last action")
        self.redo_action.setShortcut("Ctrl+Y")

        self.cut_action: QAction = QAction("Cut")
        self.cut_action.setStatusTip("Cut the selected text")
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action: QAction = QAction("Copy")
        self.copy_action.setStatusTip("Copy the selected text")
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action: QAction = QAction("Paste")
        self.paste_action.setStatusTip("Paste text from the clipboard")
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_plain_action: QAction = QAction("Paste Plain")
        self.paste_plain_action.setStatusTip("Paste plain text from the clipboard")
        self.paste_plain_action.setShortcut("Ctrl+Shift+V")

        self.select_all_action: QAction = QAction("Select All")
        self.select_all_action.setStatusTip("Select the entire document")
        self.select_all_action.setShortcut("Ctrl+A")

        self.find_action: QAction = QAction("Find")
        self.find_action.setStatusTip("Find a word in the document")
        self.find_action.setShortcut("Ctrl+F")
        self.find_and_replace_action: QAction = QAction("Find and Replace")
        self.find_and_replace_action.setStatusTip("Find and replace a word in the document")
        self.find_and_replace_action.setShortcut("Ctrl+H")

        # insert
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
        self.turn_underlined_action: QAction = QAction("Underline")
        self.turn_underlined_action.setCheckable(True)
        self.turn_underlined_action.setStatusTip("Make the selected text underlined")
        self.turn_underlined_action.setShortcut("Ctrl+U")

        self.indent_right_action: QAction = QAction("Right")
        self.indent_right_action.setStatusTip("Indent right")
        self.indent_right_action.setShortcut("Ctrl+]")
        self.indent_left_action: QAction = QAction("Left")
        self.indent_left_action.setStatusTip("Indent left")
        self.indent_left_action.setShortcut("Ctrl+[")

        self.select_line_spacing_action: QAction = QAction("Line spacing")  # maybe new menu
        self.select_line_spacing_action.setStatusTip("Select the spacing between lines")
        self.select_paragraph_spacing_action: QAction = QAction("Paragraph spacing")  # maybe new menu
        self.select_paragraph_spacing_action.setStatusTip("Select the spacing between paragraphs")

        self.turn_pagination_action: QAction = QAction("Pages")
        self.turn_pagination_action.setCheckable(True)
        self.turn_pagination_action.setStatusTip("Show pages")

        # style
        self.open_style_action: QAction = QAction("Styles")
        self.open_style_action.setStatusTip("Manage custom styles")
        self.clear_style_action: QAction = QAction("Clear")
        self.clear_style_action.setStatusTip("Clear the style of the selected text")

        # help
        self.show_guide_action: QAction = QAction("Guide")
        self.show_guide_action.setStatusTip("View the user's guide")
        self.show_guide_action.setShortcut("F1")
        self.show_about_action: QAction = QAction("About")
        self.show_about_action.setStatusTip("View application information")

        # TODO: DEBUG
        self.test_action: QAction = QAction("Test")
        self.test_action.setStatusTip("Test")

    def setupMenuBar(self) -> None:
        self.menu_bar = QMenuBar()

        self.file_menu: QMenu = QMenu("File")
        self.file_menu.addAction(self.new_document_action)
        self.file_menu.addAction(self.open_document_action)
        self.file_menu.addAction(self.close_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_document_action)
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
        self.edit_menu.addAction(self.paste_plain_action)
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
        self.format_menu.addAction(self.turn_underlined_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.indent_right_action)
        self.format_menu.addAction(self.indent_left_action)
        self.format_menu.addSeparator()
        self.format_menu.addAction(self.select_line_spacing_action)
        self.format_menu.addAction(self.select_paragraph_spacing_action)
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
        self.format_tool.addAction(self.turn_underlined_action)
        self.addToolBar(self.format_tool)

        self.color_tool: QToolBar = QToolBar("Color")
        self.color_tool.addWidget(self.color_picker)
        self.color_tool.addWidget(self.background_color_picker)
        self.addToolBar(self.color_tool)

        self.indent_tool: QToolBar = QToolBar("Indent")
        self.indent_tool.addAction(self.indent_right_action)
        self.indent_tool.addAction(self.indent_left_action)
        self.addToolBar(self.indent_tool)

    def setupStatusBar(self) -> None:
        self.status_bar: QStatusBar = QStatusBar()

        self.character_count = QLabel()
        self.status_bar.addPermanentWidget(self.character_count)

        self.setStatusBar(self.status_bar)

    def addPointSuffix(self) -> None:
        rem: QRegularExpressionMatch = self.no_point_re.match(self.size_combobox.currentText())
        if rem.hasMatch():
            self.size_combobox.setEditText(self.size_combobox.currentText() + " pt")
