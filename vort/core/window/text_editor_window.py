from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtGui import QFont, QColor, QGuiApplication

from core.widget.text_editor.component.select_component import HyperlinkSelection

from core.window.text_editor_window_ui import TextEditorWindowUI
from core.window.dialog.edit_paragraph_dialog_ui import EditParagraphDialogUI, EditParagraphDialogContext
from core.window.dialog.edit_hyperlink_dialog_ui import EditHyperlinkDialogUI, EditHyperlinkDialogContext


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

        # select

        self.ui.select_all_action.triggered.connect(self.selectAll)

        # search

        self.ui.find_action.triggered.connect(self.find)

        self.ui.find_and_replace_action.triggered.connect(self.findAndReplace)

        # insert

        self.ui.insert_text_action.triggered.connect(self.insertText)

        self.ui.insert_plain_text_action.triggered.connect(self.insertPlainText)

        self.ui.insert_image_action.triggered.connect(self.insertImage)

        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # font

        self.ui.font_family_combo_box.fontFamilyChanged.connect(self.onUserFontFamilyChanged)
        self.ui.font_family_combo_box.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.fontFamilyChanged.connect(self.onTextEditorFontFamilyChanged)

        self.ui.font_size_combo_box.fontSizeChanged.connect(self.onUserFontSizeChanged)
        self.ui.font_size_combo_box.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.fontSizeChnaged.connect(self.onTextEditorFontSizeChanged)

        # format

        self.ui.turn_bold_action.triggered.connect(self.onUserBoldTurned)
        self.ui.text_editor.boldTurned.connect(self.onTextEditorBoldTurned)

        self.ui.turn_italic_action.triggered.connect(self.onUserItalicTurned)
        self.ui.text_editor.italicTurned.connect(self.onTextEditorItalicTurned)

        self.ui.turn_underlined_action.triggered.connect(self.onUserUnderlinedTurned)
        self.ui.text_editor.underlinedTurned.connect(self.onTextEditorUnderlinedTurned)

        # color

        self.ui.foreground_color_picker.colorChanged.connect(self.onUserForegroundColorChanged)
        self.ui.foreground_color_picker.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.foregroundColorChanged.connect(self.onTextEditorForegroundColorChanged)

        self.ui.background_color_picker.colorChanged.connect(self.onUserBackgroundColorChanged)
        self.ui.background_color_picker.closed.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.backgroundColorChanged.connect(self.onTextEditorBackgroundColorChanged)

        # indent

        self.ui.turn_first_line_indent_action.triggered.connect(self.onUserFirstLineIndentTurned)
        self.ui.text_editor.firstLineIndentTurned.connect(self.onTextEditorFirstLineIndentTurned)

        self.ui.indent_right_action.triggered.connect(self.indentRight)

        self.ui.indent_left_action.triggered.connect(self.indentLeft)

        # space

        self.ui.set_line_spacing_1_action.triggered.connect(self.setLineSpacing_1)
        self.ui.set_line_spacing_1_15_action.triggered.connect(self.setLineSpacing_1_15)
        self.ui.set_line_spacing_1_5_action.triggered.connect(self.setLineSpacing_1_5)
        self.ui.set_line_spacing_2_action.triggered.connect(self.setLineSpacing_2)

        # page

        self.ui.turn_pagination_action.triggered.connect(self.turnPagination)

        # edit

        self.ui.open_edit_paragraph_action.triggered.connect(self.openEditParagraph)

        # style

        self.ui.open_style_action.triggered.connect(self.openStyle)

        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # help

        self.ui.show_guide_action.triggered.connect(self.showGuide)

        self.ui.show_about_action.triggered.connect(self.showAbout)

        # TODO: DEBUG
        self.ui.test_action.triggered.connect(self.test)
        self.ui.test2_action.triggered.connect(self.test2)

        # status

        self.ui.text_editor.characterCountChanged.connect(self.onTextEditorCharacterCountChanged)

        self.ui.zoom_slider.zoomFactorChanged.connect(self.onUserZoomFactorChanged)
        self.ui.zoom_slider.zoomFactorChanged.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.zoomFactorSelected.connect(self.onTextEditorZoomFactorChanged)

        self.setDefault()

        self.ui.show()

    def setDefault(self) -> None:
        # font

        self.onUserFontFamilyChanged(QFont().family())
        self.onTextEditorFontFamilyChanged(QFont().family())

        self.onUserFontSizeChanged(16)
        self.onTextEditorFontSizeChanged(16)

        # format

        self.onUserBoldTurned(False)
        self.onTextEditorBoldTurned(False)

        self.onUserItalicTurned(False)
        self.onTextEditorItalicTurned(False)

        self.onUserUnderlinedTurned(False)
        self.onTextEditorUnderlinedTurned(False)

        # color

        self.onUserForegroundColorChanged(QColor(Qt.GlobalColor.black))
        self.onTextEditorForegroundColorChanged(QColor(Qt.GlobalColor.black))

        self.onUserBackgroundColorChanged(QColor(Qt.GlobalColor.white))
        self.onTextEditorBackgroundColorChanged(QColor(Qt.GlobalColor.white))

        # indent

        self.onUserFirstLineIndentTurned(False)
        self.onTextEditorFirstLineIndentTurned(False)

        # space

        self.onUserLineSpacingChanged(1.0)

        # status

        self.ui.character_count.setCharacterCount(0)

        self.onUserZoomFactorChanged(1)
        self.onTextEditorZoomFactorChanged(1)

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
        self.ui.text_editor.input_component.cut()

    @Slot()
    def copy(self) -> None:
        self.ui.text_editor.input_component.copy()

    @Slot()
    def paste(self) -> None:
        self.ui.text_editor.input_component.paste()

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

    @Slot()
    def insertText(self) -> None:
        self.ui.text_editor.input_component.insertText()

    @Slot()
    def insertPlainText(self) -> None:
        self.ui.text_editor.input_component.insertPlainText()

    @Slot()
    def insertImage(self) -> None:
        self.ui.text_editor.input_component.insertImage()

    @Slot()
    def insertHyperlink(self) -> None:
        context: EditHyperlinkDialogContext = EditHyperlinkDialogContext()
        selection: HyperlinkSelection = self.ui.text_editor.select_component.selectedHyperlink()
        context.text = selection.text
        context.hyperlink = selection.hyperlink

        dialog = EditHyperlinkDialogUI(context)
        if dialog.exec():
            self.ui.text_editor.input_component.insertHyperlink(context.text, context.hyperlink)

    # font

    @Slot(str)
    def onUserFontFamilyChanged(self, font_family: str) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.font_component.setFontFamily(font_family)
        self.ui.text_editor.blockSignals(False)

    @Slot(str)
    def onTextEditorFontFamilyChanged(self, font_family: str) -> None:
        self.ui.font_family_combo_box.blockSignals(True)
        self.ui.font_family_combo_box.setFontFamily(font_family)
        self.ui.font_family_combo_box.blockSignals(False)

    @Slot(int)
    def onUserFontSizeChanged(self, font_size: int) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.font_component.setFontSize(font_size)
        self.ui.text_editor.blockSignals(False)

    @Slot(int)
    def onTextEditorFontSizeChanged(self, font_size: int) -> None:
        self.ui.font_size_combo_box.blockSignals(True)
        self.ui.font_size_combo_box.setFontSize(font_size)
        self.ui.font_size_combo_box.blockSignals(False)

    # format

    @Slot(bool)
    def onUserBoldTurned(self, is_bold) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.format_component.turnBold(is_bold)
        self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorBoldTurned(self, is_bold) -> None:
        self.ui.turn_bold_action.blockSignals(True)
        self.ui.turn_bold_action.setChecked(is_bold)
        self.ui.turn_bold_action.blockSignals(False)

    @Slot(bool)
    def onUserItalicTurned(self, is_italic) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.format_component.turnItalic(is_italic)
        self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorItalicTurned(self, is_italic) -> None:
        self.ui.turn_italic_action.blockSignals(True)
        self.ui.turn_italic_action.setChecked(is_italic)
        self.ui.turn_italic_action.blockSignals(False)

    @Slot(bool)
    def onUserUnderlinedTurned(self, is_underlined) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.format_component.turnUnderlined(is_underlined)
        self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorUnderlinedTurned(self, is_underlined) -> None:
        self.ui.turn_underlined_action.blockSignals(True)
        self.ui.turn_underlined_action.setChecked(is_underlined)
        self.ui.turn_underlined_action.blockSignals(False)

    # color

    @Slot(QColor)
    def onUserForegroundColorChanged(self, color: QColor) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.color_component.setForegroundColor(color)
        self.ui.text_editor.blockSignals(False)

    @Slot(QColor)
    def onTextEditorForegroundColorChanged(self, color: QColor) -> None:
        self.ui.foreground_color_picker.blockSignals(True)
        self.ui.foreground_color_picker.setColor(color)
        self.ui.foreground_color_picker.blockSignals(False)

    @Slot(QColor)
    def onUserBackgroundColorChanged(self, color: QColor) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.color_component.setBackgroundColor(color)
        self.ui.text_editor.blockSignals(False)

    @Slot(QColor)
    def onTextEditorBackgroundColorChanged(self, color: QColor) -> None:
        self.ui.background_color_picker.blockSignals(True)
        self.ui.background_color_picker.setColor(color)
        self.ui.background_color_picker.blockSignals(False)

    # indent

    @Slot(bool)
    def onUserFirstLineIndentTurned(self, is_indent) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.spacing_component.turnFirstLineIndent(is_indent)
        self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorFirstLineIndentTurned(self, is_indent) -> None:
        self.ui.turn_first_line_indent_action.blockSignals(True)
        self.ui.turn_first_line_indent_action.setChecked(is_indent)
        self.ui.turn_first_line_indent_action.blockSignals(False)

    @Slot(float)
    def onUserFirstLineIndentChnaged(self, indent: float) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.spacing_component.setFirstLineIndent(indent)
        self.ui.text_editor.blockSignals(False)

    @Slot(int)
    def onUserIndentChanged(self, indent: int) -> None:
        self.ui.text_editor.spacing_component.setIndent(indent)

    @Slot()
    def indentRight(self) -> None:
        self.ui.text_editor.spacing_component.indentRight()

    @Slot()
    def indentLeft(self) -> None:
        self.ui.text_editor.spacing_component.indentLeft()

    # space

    @Slot(float)
    def onUserLineSpacingChanged(self, spacing: float) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.spacing_component.setLineSpacing(spacing)
        self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onTextEditorLineSpacingChanged(self, spacing: float) -> None:
        self.ui.set_line_spacing_1_action.blockSignals(True)
        self.ui.set_line_spacing_1_15_action.blockSignals(True)
        self.ui.set_line_spacing_1_5_action.blockSignals(True)
        self.ui.set_line_spacing_2_action.blockSignals(True)

        self.ui.set_line_spacing_1_action.setChecked(spacing == 1.0)
        self.ui.set_line_spacing_1_15_action.setChecked(spacing == 1.15)
        self.ui.set_line_spacing_1_5_action.setChecked(spacing == 1.5)
        self.ui.set_line_spacing_2_action.setChecked(spacing == 2.0)

        self.ui.set_line_spacing_1_action.blockSignals(False)
        self.ui.set_line_spacing_1_15_action.blockSignals(False)
        self.ui.set_line_spacing_1_5_action.blockSignals(False)
        self.ui.set_line_spacing_2_action.blockSignals(False)

    @Slot()
    def setLineSpacing_1(self) -> None:
        self.onUserLineSpacingChanged(1.0)

    @Slot()
    def setLineSpacing_1_15(self) -> None:
        self.onUserLineSpacingChanged(1.15)

    @Slot()
    def setLineSpacing_1_5(self) -> None:
        self.onUserLineSpacingChanged(1.5)

    @Slot()
    def setLineSpacing_2(self) -> None:
        self.onUserLineSpacingChanged(2.0)

    # margin

    @Slot(float)
    def onUserParagraphTopMarginChanged(self, margin: float) -> None:
        self.ui.text_editor.spacing_component.setTopMargin(margin)

    @Slot(float)
    def onUserParagraphBottomMarginChanged(self, margin: float) -> None:
        self.ui.text_editor.spacing_component.setBottomMargin(margin)

    @Slot(float)
    def onUserParagraphLeftMarginChanged(self, margin: float) -> None:
        self.ui.text_editor.spacing_component.setLeftMargin(margin)

    @Slot(float)
    def onUserParagraphRightMarginChanged(self, margin: float) -> None:
        self.ui.text_editor.spacing_component.setRightMargin(margin)

    # page

    def turnPagination(self) -> None:
        print("turnPagination")

    # edit

    def openEditParagraph(self) -> None:
        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        context: EditParagraphDialogContext = EditParagraphDialogContext()
        context.alignment = Qt.AlignmentFlag.AlignLeft  # TODO:
        context.heading_level = 0  # TODO:
        context.is_first_line_indent_turned = self.ui.text_editor.spacing_component.isFirstLineIndentTurned()
        context.first_line_indent = self.ui.text_editor.spacing_component.firstLineIndent() * 2.54 / dpi
        context.indent = self.ui.text_editor.spacing_component.indent()
        context.line_spacing = self.ui.text_editor.spacing_component.lineSpacing()
        context.top_margin = self.ui.text_editor.spacing_component.topMargin() * 2.54 / dpi
        context.bottom_margin = self.ui.text_editor.spacing_component.bottomMargin() * 2.54 / dpi
        context.left_margin = self.ui.text_editor.spacing_component.leftMargin() * 2.54 / dpi
        context.right_margin = self.ui.text_editor.spacing_component.rightMargin() * 2.54 / dpi

        dialog = EditParagraphDialogUI(context)
        if dialog.exec():
            self.onUserFirstLineIndentTurned(context.is_first_line_indent_turned)
            self.onTextEditorFirstLineIndentTurned(context.is_first_line_indent_turned)

            if context.is_first_line_indent_turned:
                self.onUserFirstLineIndentChnaged(context.first_line_indent * dpi / 2.54)

            self.onUserIndentChanged(context.indent)

            self.onUserLineSpacingChanged(context.line_spacing)
            self.onTextEditorLineSpacingChanged(context.line_spacing)

            self.onUserParagraphTopMarginChanged(context.top_margin * dpi / 2.54)

            self.onUserParagraphBottomMarginChanged(context.bottom_margin * dpi / 2.54)

            self.onUserParagraphLeftMarginChanged(context.left_margin * dpi / 2.54)

            self.onUserParagraphRightMarginChanged(context.right_margin * dpi / 2.54)

    # style

    def openStyle(self) -> None:
        print("openStyle")

    def clearStyle(self) -> None:
        print("clearStyle")

    def showGuide(self) -> None:
        print("showGuide")

    def showAbout(self) -> None:
        print("showAbout")

    # status

    @Slot(int)
    def onTextEditorCharacterCountChanged(self, character_count: int) -> None:
        self.ui.character_count.blockSignals(True)
        self.ui.character_count.setCharacterCount(character_count)
        self.ui.character_count.blockSignals(False)

    @Slot(float)
    def onUserZoomFactorChanged(self, zoom_factor: float) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.setZoomFactor(zoom_factor)
        self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onTextEditorZoomFactorChanged(self, zoom_factor: float) -> None:
        self.ui.zoom_slider.blockSignals(True)
        self.ui.zoom_slider.setZoomFactor(zoom_factor)
        self.ui.zoom_slider.blockSignals(False)

    # TODO: DEBUG
    def test(self) -> None:
        self.ui.text_editor.test()
        pass

    def test2(self) -> None:
        self.ui.text_editor.test2()
        pass
