from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QMainWindow, QWidget, QStatusBar, QSpacerItem
from PySide6.QtGui import QAction, QPixmap, QColor, QActionGroup, QCloseEvent

from core.widget.color_picker.color_picker_tool import ColorPickerTool

from core.widget.font_box.font_size_combo_box import FontSizeComboBox
from core.widget.font_box.font_family_combo_box import FontFamilyComboBox

from core.widget.status_bar.char_count_label import CharCountLabel
from core.widget.status_bar.zoom_slider import ZoomSlider
from core.widget.status_bar.find_line import FindLine
from core.widget.status_bar.reaplce_line import ReplaceLine

from core.widget.text_style.text_style_combo_box import TextStyleComboBox

from core.editor.document_editor.document_editor import DocumentEditor


import resource.resource_rc


class DocumentEditorWindowUI(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # self

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("vort")

        # widget

        self.text_editor: DocumentEditor = DocumentEditor(self)
        self.setCentralWidget(self.text_editor.ui)

        # setup

        self.setupAction()
        self.setupWidget()
        self.setupMenuBar()
        self.setupToolBar()
        self.setupStatusBar()

    def setupAction(self) -> None:
        # app

        self.close_application_action: QAction = QAction("Exit")
        self.close_application_action.setIcon(QPixmap(":/icon/x.svg"))
        self.close_application_action.setShortcut("Ctrl+Q")

        # file

        self.new_document_action: QAction = QAction("New...")
        self.new_document_action.setIcon(QPixmap(":/icon/folder_plus.svg"))
        self.new_document_action.setShortcut("Ctrl+N")

        self.open_document_action: QAction = QAction("Open...")
        self.open_document_action.setIcon(QPixmap(":/icon/folder_open.svg"))
        self.open_document_action.setShortcut("Ctrl+O")

        self.close_document_action: QAction = QAction("Close")
        self.close_document_action.setIcon(QPixmap(":/icon/folder_closed.svg"))
        self.close_document_action.setShortcut("Ctrl+W")

        self.save_document_action: QAction = QAction("Save")
        self.save_document_action.setIcon(QPixmap(":/icon/save.svg"))
        self.save_document_action.setShortcut("Ctrl+S")

        # history

        self.undo_action: QAction = QAction("Undo")
        self.undo_action.setIcon(QPixmap(":/icon/undo.svg"))
        self.undo_action.setShortcut("Ctrl+Z")

        self.redo_action: QAction = QAction("Redo")
        self.redo_action.setIcon(QPixmap(":/icon/redo.svg"))
        self.redo_action.setShortcut("Ctrl+Y")

        # copy paste

        self.cut_action: QAction = QAction("Cut")
        self.cut_action.setIcon(QPixmap(":/icon/scissors.svg"))
        self.cut_action.setShortcut("Ctrl+X")

        self.copy_action: QAction = QAction("Copy")
        self.copy_action.setIcon(QPixmap(":/icon/clipboard_copy.svg"))
        self.copy_action.setShortcut("Ctrl+C")

        self.paste_action: QAction = QAction("Paste")
        self.paste_action.setIcon(QPixmap(":/icon/clipboard_paste.svg"))
        self.paste_action.setShortcut("Ctrl+V")

        self.paste_plain_action: QAction = QAction("Paste plain")
        self.paste_plain_action.setShortcut("Ctrl+Shift+V")

        # select

        self.select_all_action: QAction = QAction("Select All")
        self.select_all_action.setIcon(QPixmap(":/icon/box_select.svg"))
        self.select_all_action.setShortcut("Ctrl+A")

        # insert

        self.insert_image_action: QAction = QAction("Image...")
        self.insert_image_action.setIcon(QPixmap(":/icon/image.svg"))

        self.insert_hyperlink_action: QAction = QAction("Hylerlink...")
        self.insert_hyperlink_action.setIcon(QPixmap(":/icon/link.svg"))

        # format

        self.turn_bold_action: QAction = QAction("Bold")
        self.turn_bold_action.setIcon(QPixmap(":/icon/bold.svg"))
        self.turn_bold_action.setCheckable(True)
        self.turn_bold_action.setShortcut("Ctrl+B")

        self.turn_italic_action: QAction = QAction("Italic")
        self.turn_italic_action.setIcon(QPixmap(":/icon/italic.svg"))
        self.turn_italic_action.setCheckable(True)
        self.turn_italic_action.setShortcut("Ctrl+I")

        self.turn_underlined_action: QAction = QAction("Underlined")
        self.turn_underlined_action.setIcon(QPixmap(":/icon/underlined.svg"))
        self.turn_underlined_action.setCheckable(True)
        self.turn_underlined_action.setShortcut("Ctrl+U")

        # alignment

        self.set_alignment_left_action: QAction = QAction("Left")
        self.set_alignment_left_action.setIcon(QPixmap(":/icon/align_left.svg"))
        self.set_alignment_left_action.setCheckable(True)
        self.set_alignment_left_action.setStatusTip("Align left")

        self.set_alignment_center_action: QAction = QAction("Center")
        self.set_alignment_center_action.setIcon(QPixmap(":/icon/align_center.svg"))
        self.set_alignment_center_action.setCheckable(True)
        self.set_alignment_center_action.setStatusTip("Align center")

        self.set_alignment_right_action: QAction = QAction("Right")
        self.set_alignment_right_action.setIcon(QPixmap(":/icon/align_right.svg"))
        self.set_alignment_right_action.setCheckable(True)
        self.set_alignment_right_action.setStatusTip("Align right")

        self.alignment_group: QActionGroup = QActionGroup(self)
        self.alignment_group.addAction(self.set_alignment_left_action)
        self.alignment_group.addAction(self.set_alignment_center_action)
        self.alignment_group.addAction(self.set_alignment_right_action)
        self.alignment_group.setExclusive(True)
        self.set_alignment_left_action.setChecked(True)

        # indent

        self.indent_right_action: QAction = QAction("Right")
        self.indent_right_action.setIcon(QPixmap(":/icon/indent_increase.svg"))
        self.indent_right_action.setStatusTip("Indent right")
        self.indent_right_action.setShortcut("Ctrl+]")

        self.indent_left_action: QAction = QAction("Left")
        self.indent_left_action.setIcon(QPixmap(":/icon/indent_decrease.svg"))
        self.indent_left_action.setStatusTip("Indent left")
        self.indent_left_action.setShortcut("Ctrl+[")

        # space

        self.set_line_spacing_1_action: QAction = QAction("1 line spacing")
        self.set_line_spacing_1_action.setCheckable(True)

        self.set_line_spacing_1_15_action: QAction = QAction("1.15 line spacing")
        self.set_line_spacing_1_15_action.setCheckable(True)

        self.set_line_spacing_1_5_action: QAction = QAction("1.5 line spacing")
        self.set_line_spacing_1_5_action.setCheckable(True)

        self.set_line_spacing_2_action: QAction = QAction("2 line spacing")
        self.set_line_spacing_2_action.setCheckable(True)

        self.line_space_group: QActionGroup = QActionGroup(self)
        self.line_space_group.addAction(self.set_line_spacing_1_action)
        self.line_space_group.addAction(self.set_line_spacing_1_15_action)
        self.line_space_group.addAction(self.set_line_spacing_1_5_action)
        self.line_space_group.addAction(self.set_line_spacing_2_action)
        self.line_space_group.setExclusive(True)

        # style

        self.open_style_action: QAction = QAction("Styles")
        self.open_style_action.setIcon(QPixmap(":/icon/book_type.svg"))

        self.new_style_action: QAction = QAction("New style...")
        self.new_style_action.setIcon(QPixmap(":/icon/book_plus.svg"))

        self.apply_style_action: QAction = QAction("Apply")
        self.apply_style_action.setIcon(QPixmap(":/icon/type.svg"))

        self.clear_style_action: QAction = QAction("Clear")
        self.clear_style_action.setIcon(QPixmap(":/icon/remove_formatting.svg"))

        # settings

        self.open_page_settings: QAction = QAction("Page")
        self.open_page_settings.setIcon(QPixmap(":/icon/sticky_note.svg"))

        self.open_paragraph_settings: QAction = QAction("Paragraph")
        self.open_paragraph_settings.setIcon(QPixmap(":/icon/pilcrow.svg"))

        self.open_header_settings: QAction = QAction("Header")
        self.open_header_settings.setIcon(QPixmap(":/icon/panel_top_close.svg"))

        self.open_footer_settings: QAction = QAction("Footer")
        self.open_footer_settings.setIcon(QPixmap(":/icon/panel_bottom_close.svg"))

        # help

        self.show_about_action: QAction = QAction("About")
        self.show_about_action.setIcon(QPixmap(":/icon/info.svg"))

    def setupWidget(self) -> None:
        # font

        self.font_family_combo_box = FontFamilyComboBox()
        self.font_size_combo_box = FontSizeComboBox()

        # color
        icon = QPixmap(16, 16)
        icon.fill(QColor("cyan"))

        self.foreground_color_picker = ColorPickerTool(self)
        self.foreground_color_picker.ui.setIcon(QPixmap(":/icon/pen.svg"))
        self.foreground_color_picker.ui.setColorIcon(QColor("black"))

        self.background_color_picker = ColorPickerTool(self)
        self.background_color_picker.ui.setIcon(QPixmap(":/icon/highlighter.svg"))
        self.background_color_picker.ui.setColorIcon(QColor("transparent"))

        # style

        self.style_combo_box: TextStyleComboBox = TextStyleComboBox()

        # find replace

        self.find_line: FindLine = FindLine(self)
        self.replace_line: ReplaceLine = ReplaceLine(self)

        # char count

        self.character_count: CharCountLabel = CharCountLabel(self)

        # zoom

        self.zoom_slider: ZoomSlider = ZoomSlider(self)

    def setupMenuBar(self) -> None:
        self.menu_bar = QMenuBar()

        self.file_menu: QMenu = QMenu("File")
        self.file_menu.addAction(self.new_document_action)
        self.file_menu.addAction(self.open_document_action)
        self.file_menu.addAction(self.close_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_document_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_application_action)
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
        self.menu_bar.addMenu(self.edit_menu)

        self.insert_menu: QMenu = QMenu("Insert")
        self.insert_menu.addAction(self.insert_image_action)
        self.insert_menu.addAction(self.insert_hyperlink_action)
        self.menu_bar.addMenu(self.insert_menu)

        self.alignment_menu: QMenu = QMenu("Alignment")
        self.alignment_menu.addAction(self.set_alignment_left_action)
        self.alignment_menu.addAction(self.set_alignment_center_action)
        self.alignment_menu.addAction(self.set_alignment_right_action)

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
        self.format_menu.addMenu(self.alignment_menu)
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
        self.help_menu.addAction(self.show_about_action)
        self.menu_bar.addMenu(self.help_menu)

        self.setMenuBar(self.menu_bar)

    def setupToolBar(self) -> None:
        self.style_tool: QToolBar = QToolBar("Style")
        self.style_tool.addWidget(self.style_combo_box)
        self.style_tool.addAction(self.apply_style_action)
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

        self.alignment_tool: QToolBar = QToolBar("Alignment")
        self.alignment_tool.addAction(self.set_alignment_left_action)
        self.alignment_tool.addAction(self.set_alignment_center_action)
        self.alignment_tool.addAction(self.set_alignment_right_action)
        self.addToolBar(self.alignment_tool)

        self.indent_tool: QToolBar = QToolBar("Indent")
        self.indent_tool.addAction(self.indent_right_action)
        self.indent_tool.addAction(self.indent_left_action)
        self.addToolBar(self.indent_tool)

    def setupStatusBar(self) -> None:
        self.status_bar: QStatusBar = QStatusBar()

        self.status_bar.addPermanentWidget(self.find_line)
        self.status_bar.addPermanentWidget(self.replace_line)
        self.status_bar.addPermanentWidget(QWidget(), 1)
        self.status_bar.addPermanentWidget(self.character_count)
        self.status_bar.addPermanentWidget(self.zoom_slider)

        self.setStatusBar(self.status_bar)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close_application_action.triggered.emit()
