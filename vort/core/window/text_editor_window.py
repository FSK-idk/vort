from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtGui import QFont, QColor

from core.window.text_editor_window_ui import TextEditorWindowUI


# some code may be unnecessary, but I want everything to be consistent


class TextEditorWindow(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: TextEditorWindowUI = TextEditorWindowUI()

        # app

        self.ui.exit_application_action.triggered.connect(self.ui.close)

        # file

        self.ui.new_document_action.triggered.connect(self.newDocument)

        self.ui.open_document_action.triggered.connect(self.openDocument)

        self.ui.close_document_action.triggered.connect(self.closeDocument)

        self.ui.save_document_action.triggered.connect(self.saveDocument)

        # history

        self.ui.undo_action.triggered.connect(self.undo)

        self.ui.redo_action.triggered.connect(self.redo)

        # copy paste

        self.ui.cut_action.triggered.connect(self.cut)

        self.ui.copy_action.triggered.connect(self.copy)

        self.ui.paste_action.triggered.connect(self.paste)

        self.ui.paste_plain_action.triggered.connect(self.pastePlain)

        # select

        self.ui.select_all_action.triggered.connect(self.selectAll)

        # search

        self.ui.find_action.triggered.connect(self.find)

        self.ui.find_and_replace_action.triggered.connect(self.findAndReplace)

        # insert

        self.ui.insert_image_action.triggered.connect(self.insertImage)

        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # font

        self.ui.font_family_combo_box.fontFamilyChanged.connect(self.selectFontFamily)
        self.ui.font_family_combo_box.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.fontFamilySelected.connect(self.onFontFamilySelected)

        self.ui.font_size_combo_box.fontSizeChanged.connect(self.selectFontSize)
        self.ui.font_size_combo_box.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.fontSizeSelected.connect(self.onFontSizeSelected)

        # format

        self.ui.turn_bold_action.triggered.connect(self.turnBold)
        self.ui.text_editor.boldTurned.connect(self.onBoldTurned)

        self.ui.turn_italic_action.triggered.connect(self.turnItalic)
        self.ui.text_editor.italicTurned.connect(self.onItalicTurned)

        self.ui.turn_underlined_action.triggered.connect(self.turnUnderlined)
        self.ui.text_editor.underlinedTurned.connect(self.onUnderlinedTurned)

        # color

        self.ui.foreground_color_picker.colorChanged.connect(self.selectForegroundColor)
        self.ui.foreground_color_picker.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.foregroundColorSelected.connect(self.onForegroundColorSelected)

        self.ui.background_color_picker.colorChanged.connect(self.selectBackgroundColor)
        self.ui.background_color_picker.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.backgroundColorSelected.connect(self.onBackgroundColorSelected)

        # indent

        self.ui.turn_first_line_indent_action.triggered.connect(self.turnFirstLineIndent)
        self.ui.text_editor.firstLineIndentTurned.connect(self.onFirstLineIndentTurned)

        self.ui.indent_paragraph_right_action.triggered.connect(self.indentParagraphRight)

        self.ui.indent_paragraph_left_action.triggered.connect(self.indentParagraphLeft)

        # space

        self.ui.select_line_spacing_action.triggered.connect(self.selectLineSpacing)

        self.ui.select_paragraph_spacing_action.triggered.connect(self.selectParagraphSpacing)

        # page

        self.ui.turn_pagination_action.triggered.connect(self.turnPagination)

        # style

        self.ui.open_style_action.triggered.connect(self.openStyle)

        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # help

        self.ui.show_guide_action.triggered.connect(self.showGuide)

        self.ui.show_about_action.triggered.connect(self.showAbout)

        # TODO: DEBUG
        self.ui.test_action.triggered.connect(self.test)

        # status

        self.ui.text_editor.characterCountChanged.connect(self.onCharacterCountChanged)

        self.ui.zoom_slider.zoomFactorChanged.connect(self.selectZoomFactor)
        self.ui.zoom_slider.zoomFactorChanged.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.zoomFactorSelected.connect(self.onZoomFactorSelected)

        self.setDefault()

        self.ui.show()

    def setDefault(self) -> None:
        # font

        self.selectFontFamily(QFont().family())
        self.onFontFamilySelected(QFont().family())

        self.selectFontSize(16)
        self.onFontSizeSelected(16)

        # format

        self.turnBold(False)
        self.onBoldTurned(False)

        self.turnItalic(False)
        self.onItalicTurned(False)

        self.turnUnderlined(False)
        self.onUnderlinedTurned(False)

        # color

        self.selectForegroundColor(QColor(Qt.GlobalColor.black))
        self.onForegroundColorSelected(QColor(Qt.GlobalColor.black))

        self.selectBackgroundColor(QColor(Qt.GlobalColor.white))
        self.onBackgroundColorSelected(QColor(Qt.GlobalColor.white))

        # indent

        self.turnFirstLineIndent(False)
        self.onFirstLineIndentTurned(False)

        # status

        self.ui.character_count.setCharacterCount(0)
        self.selectZoomFactor(1)
        self.onZoomFactorSelected(1)

    def newDocument(self) -> None:
        print("newDocument")

    def openDocument(self) -> None:
        print("openDocument")

    def closeDocument(self) -> None:
        print("closeDocument")

    def saveDocument(self) -> None:
        print("saveDocument")

    # history

    @Slot()
    def undo(self) -> None:
        self.ui.text_editor.history_component.undo()

    @Slot()
    def redo(self) -> None:
        self.ui.text_editor.history_component.redo()

    # copy paste

    @Slot()
    def cut(self) -> None:
        self.ui.text_editor.copy_paste_component.cut()

    @Slot()
    def copy(self) -> None:
        self.ui.text_editor.copy_paste_component.copy()

    @Slot()
    def paste(self) -> None:
        self.ui.text_editor.copy_paste_component.paste()

    @Slot()
    def pastePlain(self) -> None:
        self.ui.text_editor.copy_paste_component.pastePlain()

    # select

    @Slot()
    def selectAll(self) -> None:
        self.ui.text_editor.select_component.selectAll()

    # search

    def find(self) -> None:
        print("find")

    def findAndReplace(self) -> None:
        print("findAndReplace")

    # insert

    def insertImage(self) -> None:
        print("insertImage")

    def insertHyperlink(self) -> None:
        print("insertHyperlink")

    # font

    @Slot(str)
    def selectFontFamily(self, font_family: str) -> None:
        self.ui.text_editor.font_component.setFontFamily(font_family)

    @Slot(str)
    def onFontFamilySelected(self, font_family: str) -> None:
        self.ui.font_family_combo_box.blockSignals(True)
        self.ui.font_family_combo_box.setFontFamily(font_family)
        self.ui.font_family_combo_box.blockSignals(False)

    @Slot(int)
    def selectFontSize(self, font_size: int) -> None:
        self.ui.text_editor.font_component.setFontSize(font_size)

    @Slot(int)
    def onFontSizeSelected(self, font_size: int) -> None:
        self.ui.font_size_combo_box.blockSignals(True)
        self.ui.font_size_combo_box.setFontSize(font_size)
        self.ui.font_size_combo_box.blockSignals(False)

    # format

    @Slot(bool)
    def turnBold(self, is_bold) -> None:
        self.ui.text_editor.format_component.turnBold(is_bold)

    @Slot(bool)
    def onBoldTurned(self, is_bold) -> None:
        self.ui.turn_bold_action.blockSignals(True)
        self.ui.turn_bold_action.setChecked(is_bold)
        self.ui.turn_bold_action.blockSignals(False)

    @Slot(bool)
    def turnItalic(self, is_italic) -> None:
        self.ui.text_editor.format_component.turnItalic(is_italic)

    @Slot(bool)
    def onItalicTurned(self, is_italic) -> None:
        self.ui.turn_italic_action.blockSignals(True)
        self.ui.turn_italic_action.setChecked(is_italic)
        self.ui.turn_italic_action.blockSignals(False)

    @Slot(bool)
    def turnUnderlined(self, is_underlined) -> None:
        self.ui.text_editor.format_component.turnUnderlined(is_underlined)

    @Slot(bool)
    def onUnderlinedTurned(self, is_underlined) -> None:
        self.ui.turn_underlined_action.blockSignals(True)
        self.ui.turn_underlined_action.setChecked(is_underlined)
        self.ui.turn_underlined_action.blockSignals(False)

    # color

    @Slot(QColor)
    def selectForegroundColor(self, color: QColor) -> None:
        self.ui.text_editor.color_component.setForegroundColor(color)

    @Slot(QColor)
    def onForegroundColorSelected(self, color: QColor) -> None:
        self.ui.foreground_color_picker.blockSignals(True)
        self.ui.foreground_color_picker.setColor(color)
        self.ui.foreground_color_picker.blockSignals(False)

    @Slot(QColor)
    def selectBackgroundColor(self, color: QColor) -> None:
        self.ui.text_editor.color_component.setBackgroundColor(color)

    @Slot(QColor)
    def onBackgroundColorSelected(self, color: QColor) -> None:
        self.ui.background_color_picker.blockSignals(True)
        self.ui.background_color_picker.setColor(color)
        self.ui.background_color_picker.blockSignals(False)

    # indent

    @Slot(bool)
    def turnFirstLineIndent(self, is_indent) -> None:
        self.ui.text_editor.indent_component.turnFirstLineIndent(is_indent)

    @Slot(bool)
    def onFirstLineIndentTurned(self, is_indent) -> None:
        self.ui.turn_first_line_indent_action.blockSignals(True)
        self.ui.turn_first_line_indent_action.setChecked(is_indent)
        self.ui.turn_first_line_indent_action.blockSignals(False)

    @Slot()
    def indentParagraphRight(self) -> None:
        self.ui.text_editor.indent_component.indentParagraphRight()

    @Slot()
    def indentParagraphLeft(self) -> None:
        self.ui.text_editor.indent_component.indentParagraphLeft()

    # select

    def selectLineSpacing(self) -> None:
        print("selectLineSpacing")

    def selectParagraphSpacing(self) -> None:
        print("selectParagraphSpacing")

    def turnPagination(self) -> None:
        print("turnPagination")

    def openStyle(self) -> None:
        print("openStyle")

    def clearStyle(self) -> None:
        print("clearStyle")

    def showGuide(self) -> None:
        print("showGuide")

    def showAbout(self) -> None:
        print("showAbout")

    @Slot(int)
    def onCharacterCountChanged(self, character_count: int) -> None:
        self.ui.character_count.blockSignals(True)
        self.ui.character_count.setCharacterCount(character_count)
        self.ui.character_count.blockSignals(False)

    @Slot(float)
    def selectZoomFactor(self, zoom_factor: float) -> None:
        self.ui.text_editor.setZoomFactor(zoom_factor)

    @Slot(float)
    def onZoomFactorSelected(self, zoom_factor: float) -> None:
        self.ui.zoom_slider.blockSignals(True)
        self.ui.zoom_slider.setZoomFactor(zoom_factor)
        self.ui.zoom_slider.blockSignals(False)

    # TODO: DEBUG
    def test(self) -> None:
        self.ui.text_editor.test()
        pass
