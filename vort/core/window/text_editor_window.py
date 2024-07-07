from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtGui import QFont, QColor, QGuiApplication, QTextDocument

from core.window.text_editor_window_ui import TextEditorWindowUI
from core.window.dialog.edit_hyperlink_dialog_ui import EditHyperlinkDialogUI, EditHyperlinkDialogContext
from core.window.settings.settings_dialog_ui import SettingsDialogUI, SettingsContext

from core.window.settings.page_settings_ui import PageSettingsContext
from core.window.settings.paragraph_settings_ui import ParagraphSettingsContext
from core.window.settings.header_settings_ui import HeaderSettingsContext
from core.window.settings.footer_settings_ui import FooterSettingsContext

from core.text_editor.component.select_component import HyperlinkSelection

from core.text_editor.document_file import DocumentFile


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

        # style

        self.ui.open_style_action.triggered.connect(self.openStyle)

        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # settings

        self.ui.open_page_settings.triggered.connect(self.openPageSettings)

        self.ui.open_paragraph_settings.triggered.connect(self.openParagraphSettings)

        self.ui.open_header_settings.triggered.connect(self.openHeaderSettings)

        self.ui.open_footer_settings.triggered.connect(self.openFooterSettings)

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

        self.setDeafultDocument()
        self.setDefaultEditor()

        self.ui.show()

    def setDeafultDocument(self) -> None:
        config: DocumentFile = DocumentFile()

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px = dpi / 2.54
        mm_to_px = dpi / 25.4

        # page layout

        config.text_document = QTextDocument()

        # page

        config.page_width = 21 * cm_to_px
        config.page_height = 29.7 * cm_to_px
        config.page_spacing = 1 * cm_to_px

        config.page_color = QColor("white")

        config.page_top_margin = 1 * cm_to_px
        config.page_bottom_margin = 1 * cm_to_px
        config.page_left_margin = 1 * cm_to_px
        config.page_right_margin = 1 * cm_to_px

        config.page_top_padding = 1 * cm_to_px
        config.page_bottom_padding = 1 * cm_to_px
        config.page_left_padding = 1 * cm_to_px
        config.page_right_padding = 1 * cm_to_px

        config.border_width = 1 * mm_to_px
        config.border_color = QColor("black")

        config.header_height = 1 * cm_to_px
        config.footer_height = 1 * cm_to_px

        # indent step

        config.default_indent_step = 1 * cm_to_px

        # header

        config.header_alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        config.header_font_family = QFont().family()
        config.header_font_size = 16

        config.header_text_background_color = QColor("transparent")
        config.header_text_foreground_color = QColor("black")

        config.is_header_turned_for_first_page = True

        config.is_header_pagination_turned = False
        config.header_pagination_starting_number = 1

        config.is_header_text_turned = True
        config.header_text = "My text"

        # footer

        config.footer_alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom

        config.footer_font_family = QFont().family()
        config.footer_font_size = 16

        config.footer_text_background_color = QColor("transparent")
        config.footer_text_foreground_color = QColor("black")

        config.is_footer_turned_for_first_page = True

        config.is_footer_pagination_turned = True
        config.footer_pagination_starting_number = 1

        config.is_footer_text_turned = False
        config.footer_text = ""

        # hyperlink

        config.is_hyperlink_bold_turned = False
        config.is_hyperlink_bold = False
        config.is_hyperlink_italic_turned = False
        config.is_hyperlink_italic = False
        config.is_hyperlink_underlined_turned = True
        config.is_hyperlink_underlined = True

        config.is_hyperlink_background_color_turned = False
        config.hyperlink_background_color = QColor("red")
        config.is_hyperlink_foreground_color_turned = True
        config.hyperlink_foreground_color = QColor("blue")

        self.ui.text_editor.setDocument(config)

    def setDefaultEditor(self) -> None:
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

        self.onUserForegroundColorChanged(QColor("black"))
        self.onTextEditorForegroundColorChanged(QColor("black"))

        self.onUserBackgroundColorChanged(QColor("transparent"))
        self.onTextEditorBackgroundColorChanged(QColor("transparent"))

        # indent

        self.onUserFirstLineIndentTurned(False)
        self.onTextEditorFirstLineIndentTurned(False)

        # space

        self.onUserParagraphAlignmentChanged(Qt.AlignmentFlag.AlignLeft)

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

    def onUserParagraphAlignmentChanged(self, alignment: Qt.AlignmentFlag) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.spacing_component.setAlignment(alignment)
        self.ui.text_editor.blockSignals(False)

    def onUserIndentStepChanged(self, step: float) -> None:
        document_context = self.ui.text_editor.documentContext()
        if document_context is None:
            return
        self.ui.text_editor.blockSignals(True)
        document_context.text_document_layout.setIndentStep(step)
        self.ui.text_editor.blockSignals(False)

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

    # style

    def openStyle(self) -> None:
        print("openStyle")

    def clearStyle(self) -> None:
        print("clearStyle")

    def showGuide(self) -> None:
        print("showGuide")

    def showAbout(self) -> None:
        print("showAbout")

    # settings

    def openSettings(self, name: str) -> None:
        document_context = self.ui.text_editor.documentContext()

        if document_context is None:
            return

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px = dpi / 2.54
        mm_to_px = dpi / 25.4

        px_to_cm = 2.54 / dpi
        px_to_mm = 25.4 / dpi

        # populate data
        page_context: PageSettingsContext = PageSettingsContext()
        page_context.page_width = document_context.page_layout.pageWidth() * px_to_cm
        page_context.page_height = document_context.page_layout.pageHeight() * px_to_cm
        page_context.page_spacing = document_context.page_layout.pageSpacing() * px_to_cm
        page_context.page_color = document_context.page_layout.pageColor()
        page_context.page_top_margin = document_context.page_layout.pageTopMargin() * px_to_cm
        page_context.page_bottom_margin = document_context.page_layout.pageBottomMargin() * px_to_cm
        page_context.page_left_margin = document_context.page_layout.pageLeftMargin() * px_to_cm
        page_context.page_right_margin = document_context.page_layout.pageRightMargin() * px_to_cm
        page_context.page_top_padding = document_context.page_layout.pageTopPadding() * px_to_cm
        page_context.page_bottom_padding = document_context.page_layout.pageBottomPadding() * px_to_cm
        page_context.page_left_padding = document_context.page_layout.pageLeftPadding() * px_to_cm
        page_context.page_right_padding = document_context.page_layout.pageRightPadding() * px_to_cm
        page_context.border_width = document_context.page_layout.borderWidth() * px_to_mm
        page_context.border_color = document_context.page_layout.borderColor()

        paragraph_context: ParagraphSettingsContext = ParagraphSettingsContext()
        paragraph_context.alignment = self.ui.text_editor.spacing_component.alignment()
        paragraph_context.is_first_line_indent_turned = self.ui.text_editor.spacing_component.isFirstLineIndentTurned()
        paragraph_context.first_line_indent = self.ui.text_editor.spacing_component.firstLineIndent() * px_to_cm
        paragraph_context.indent = self.ui.text_editor.spacing_component.indent()
        paragraph_context.indent_step = document_context.text_document_layout.indentStep() * px_to_cm
        paragraph_context.line_spacing = self.ui.text_editor.spacing_component.lineSpacing()
        paragraph_context.top_margin = self.ui.text_editor.spacing_component.topMargin() * px_to_cm
        paragraph_context.bottom_margin = self.ui.text_editor.spacing_component.bottomMargin() * px_to_cm
        paragraph_context.left_margin = self.ui.text_editor.spacing_component.leftMargin() * px_to_cm
        paragraph_context.right_margin = self.ui.text_editor.spacing_component.rightMargin() * px_to_cm

        header_context: HeaderSettingsContext = HeaderSettingsContext()
        header_context.height = document_context.page_layout.headerHeight() * px_to_cm
        header_context.alignment = document_context.text_canvas.headerLayout().alignment()
        header_context.font_family = document_context.text_canvas.headerLayout().fontFamily()
        header_context.font_size = document_context.text_canvas.headerLayout().fontSize()
        header_context.background_color = document_context.text_canvas.headerLayout().textBackgroundColor()
        header_context.foreground_color = document_context.text_canvas.headerLayout().textForegroundColor()
        header_context.is_turned_for_first_page = document_context.text_canvas.headerLayout().isTurnedForFirstPage()
        header_context.is_pagination_turned = document_context.text_canvas.headerLayout().isPaginationTurned()
        header_context.starting_number = document_context.text_canvas.headerLayout().paginationStartingNumber()
        header_context.is_text_turned = document_context.text_canvas.headerLayout().isTextTurned()
        header_context.text = document_context.text_canvas.headerLayout().text()

        footer_context: FooterSettingsContext = FooterSettingsContext()
        footer_context.height = document_context.page_layout.footerHeight() * px_to_cm
        footer_context.alignment = document_context.text_canvas.footerLayout().alignment()
        footer_context.font_family = document_context.text_canvas.footerLayout().fontFamily()
        footer_context.font_size = document_context.text_canvas.footerLayout().fontSize()
        footer_context.background_color = document_context.text_canvas.footerLayout().textBackgroundColor()
        footer_context.foreground_color = document_context.text_canvas.footerLayout().textForegroundColor()
        footer_context.is_turned_for_first_page = document_context.text_canvas.footerLayout().isTurnedForFirstPage()
        footer_context.is_pagination_turned = document_context.text_canvas.footerLayout().isPaginationTurned()
        footer_context.starting_number = document_context.text_canvas.footerLayout().paginationStartingNumber()
        footer_context.is_text_turned = document_context.text_canvas.footerLayout().isTextTurned()
        footer_context.text = document_context.text_canvas.footerLayout().text()

        settings_context = SettingsContext()
        settings_context.page_context = page_context
        settings_context.paragraph_context = paragraph_context
        settings_context.header_context = header_context
        settings_context.footer_context = footer_context

        dialog = SettingsDialogUI(settings_context, self.ui)
        dialog.openTab(name)
        dialog.applied.connect(self.onSettingsApplied)

        if dialog.exec():
            print("ok")

    def onSettingsApplied(self, context: SettingsContext) -> None:
        document_context = self.ui.text_editor.documentContext()

        if document_context is None:
            return

        print("apply")

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px = dpi / 2.54
        mm_to_px = dpi / 25.4

        page_context = context.page_context
        document_context.page_layout.setPageWidth(page_context.page_width * cm_to_px)
        document_context.page_layout.setPageHeight(page_context.page_height * cm_to_px)
        document_context.page_layout.setPageSpacing(page_context.page_spacing * cm_to_px)
        document_context.page_layout.setPageColor(page_context.page_color)
        document_context.page_layout.setPageTopMargin(page_context.page_top_margin * cm_to_px)
        document_context.page_layout.setPageBottomMargin(page_context.page_bottom_margin * cm_to_px)
        document_context.page_layout.setPageLeftMargin(page_context.page_left_margin * cm_to_px)
        document_context.page_layout.setPageRightMargin(page_context.page_right_margin * cm_to_px)
        document_context.page_layout.setPageTopPadding(page_context.page_top_padding * cm_to_px)
        document_context.page_layout.setPageBottomPadding(page_context.page_bottom_padding * cm_to_px)
        document_context.page_layout.setPageLeftPadding(page_context.page_left_padding * cm_to_px)
        document_context.page_layout.setPageRightPadding(page_context.page_right_padding * cm_to_px)
        document_context.page_layout.setBorderWidth(page_context.border_width * mm_to_px)
        document_context.page_layout.setBorderColor(page_context.border_color)

        paragraph_context = context.paragraph_context
        self.onUserParagraphAlignmentChanged(paragraph_context.alignment)
        self.onUserFirstLineIndentTurned(paragraph_context.is_first_line_indent_turned)
        self.onTextEditorFirstLineIndentTurned(paragraph_context.is_first_line_indent_turned)
        if paragraph_context.is_first_line_indent_turned:
            self.onUserFirstLineIndentChnaged(paragraph_context.first_line_indent * cm_to_px)
        self.onUserIndentChanged(paragraph_context.indent)
        self.onUserIndentStepChanged(paragraph_context.indent_step * cm_to_px)
        self.onUserLineSpacingChanged(paragraph_context.line_spacing)
        self.onTextEditorLineSpacingChanged(paragraph_context.line_spacing)
        self.onUserParagraphTopMarginChanged(paragraph_context.top_margin * cm_to_px)
        self.onUserParagraphBottomMarginChanged(paragraph_context.bottom_margin * cm_to_px)
        self.onUserParagraphLeftMarginChanged(paragraph_context.left_margin * cm_to_px)
        self.onUserParagraphRightMarginChanged(paragraph_context.right_margin * cm_to_px)

        header_context = context.header_context
        document_context.page_layout.setHeaderHeight(header_context.height * cm_to_px)
        document_context.text_canvas.headerLayout().setAlignment(header_context.alignment)
        document_context.text_canvas.headerLayout().setFontFamily(header_context.font_family)
        document_context.text_canvas.headerLayout().setFontSize(header_context.font_size)
        document_context.text_canvas.headerLayout().setTextBackgroundColor(header_context.background_color)
        document_context.text_canvas.headerLayout().setTextForegroundColor(header_context.foreground_color)
        document_context.text_canvas.headerLayout().turnForFirstPage(header_context.is_turned_for_first_page)
        document_context.text_canvas.headerLayout().turnPagination(header_context.is_pagination_turned)
        document_context.text_canvas.headerLayout().setPaginationStartingNumber(header_context.starting_number)
        document_context.text_canvas.headerLayout().turnText(header_context.is_text_turned)
        document_context.text_canvas.headerLayout().setText(header_context.text)

        footer_context = context.footer_context
        document_context.page_layout.setFooterHeight(footer_context.height * cm_to_px)
        document_context.text_canvas.footerLayout().setAlignment(footer_context.alignment)
        document_context.text_canvas.footerLayout().setFontFamily(footer_context.font_family)
        document_context.text_canvas.footerLayout().setFontSize(footer_context.font_size)
        document_context.text_canvas.footerLayout().setTextBackgroundColor(footer_context.background_color)
        document_context.text_canvas.footerLayout().setTextForegroundColor(footer_context.foreground_color)
        document_context.text_canvas.footerLayout().turnForFirstPage(footer_context.is_turned_for_first_page)
        document_context.text_canvas.footerLayout().turnPagination(footer_context.is_pagination_turned)
        document_context.text_canvas.footerLayout().setPaginationStartingNumber(footer_context.starting_number)
        document_context.text_canvas.footerLayout().turnText(footer_context.is_text_turned)
        document_context.text_canvas.footerLayout().setText(footer_context.text)

        self.ui.text_editor.repaintViewport()

    @Slot()
    def openPageSettings(self) -> None:
        self.openSettings("page")

    @Slot()
    def openParagraphSettings(self) -> None:
        self.openSettings("paragraph")

    @Slot()
    def openHeaderSettings(self) -> None:
        self.openSettings("header")

    @Slot()
    def openFooterSettings(self) -> None:
        self.openSettings("footer")

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
