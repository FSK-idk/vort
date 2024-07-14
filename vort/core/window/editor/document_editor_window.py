import os

from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QColor, QGuiApplication

from core.window.editor.document_editor_window_ui import DocumentEditorWindowUI

from core.window.dialog.edit_hyperlink_dialog import EditHyperlinkDialog, EditHyperlinkDialogContext
from core.window.dialog.edit_image_dialog import EditImageDialog, EditImageDialogContext
from core.window.dialog.about_dialog import AboutDialog

from core.window.settings.settings_dialog import SettingsDialog, SettingsContext
from core.window.settings.page_settings import PageSettingsContext
from core.window.settings.paragraph_settings import ParagraphSettingsContext
from core.window.settings.header_settings import HeaderSettingsContext
from core.window.settings.footer_settings import FooterSettingsContext

from core.window.style.style_dialog_ui import StyleDialogUI
from core.window.style.new_style_dialog_ui import NewStyleDialogUI

from core.editor.document_file import DocumentFile

from core.editor.document_editor.document_editor_context import DocumentEditorContext

from data_base.data_base import data_base

from core.util import resource_path


class DocumentEditorWindow(QObject):
    # This class connects the entire user interface to the back-end application

    def __init__(self) -> None:
        super().__init__()

        data_base.init()

        if not os.path.isdir(resource_path("./vort/document/")):
            os.mkdir(resource_path("./vort/document/"))

        self.ui: DocumentEditorWindowUI = DocumentEditorWindowUI()

        # app

        self.ui.close_application_action.triggered.connect(self.closeApplication)

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

        # insert

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

        # alignment

        self.ui.set_alignment_left_action.triggered.connect(self.setAlignmentLeft)
        self.ui.set_alignment_center_action.triggered.connect(self.setAlignmentCenter)
        self.ui.set_alignment_right_action.triggered.connect(self.setAlignmentRight)
        self.ui.text_editor.alignmentChanged.connect(self.onTextEditorAlignmentChanged)

        # indent

        self.ui.indent_right_action.triggered.connect(self.indentRight)
        self.ui.indent_left_action.triggered.connect(self.indentLeft)

        # space

        self.ui.set_line_spacing_1_action.triggered.connect(self.setLineSpacing_1)
        self.ui.set_line_spacing_1_15_action.triggered.connect(self.setLineSpacing_1_15)
        self.ui.set_line_spacing_1_5_action.triggered.connect(self.setLineSpacing_1_5)
        self.ui.set_line_spacing_2_action.triggered.connect(self.setLineSpacing_2)

        # style

        self.ui.open_style_action.triggered.connect(self.openStyle)
        self.ui.new_style_action.triggered.connect(self.newStyle)
        self.ui.apply_style_action.triggered.connect(self.applyStyle)
        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # settings

        self.ui.open_page_settings.triggered.connect(self.openPageSettings)
        self.ui.open_paragraph_settings.triggered.connect(self.openParagraphSettings)
        self.ui.open_header_settings.triggered.connect(self.openHeaderSettings)
        self.ui.open_footer_settings.triggered.connect(self.openFooterSettings)

        # help

        self.ui.show_about_action.triggered.connect(self.showAbout)

        # status

        self.ui.text_editor.charCountChanged.connect(self.onTextEditorCharacterCountChanged)

        self.ui.zoom_slider.zoomFactorChanged.connect(self.onUserZoomFactorChanged)
        self.ui.zoom_slider.zoomFactorChanged.connect(self.ui.text_editor.ui.setFocus)
        self.ui.text_editor.zoomFactorSelected.connect(self.onTextEditorZoomFactorChanged)

        self.ui.find_line.findRequest.connect(self.find)

        self.ui.find_line.caseTurned.connect(self.onUserCaseTurned)
        self.ui.text_editor.caseTurned.connect(self.onTextEditorCaseTurned)

        self.ui.find_line.wholeTurned.connect(self.onUserWholeTurned)
        self.ui.text_editor.wholeTurned.connect(self.onTextEditorWholeTurned)

        self.ui.find_line.regexTurned.connect(self.onUserRegexTurned)
        self.ui.text_editor.regexTurned.connect(self.onTextEditorRegexTurned)

        self.ui.replace_line.replaceRequest.connect(self.replace)
        self.ui.replace_line.replaceAllRequest.connect(self.replaceAll)

        self.setDefaultEditor()

        self.ui.show()

        self.filepath = ""
        self.is_document_open = False
        self.is_document_changed = False
        self.ui.text_editor.contentChanged.connect(self.onContentChanged)

    def setDefaultEditor(self) -> None:
        self.ui.character_count.setCharCount(0)
        self.onUserZoomFactorChanged(1)
        self.onTextEditorZoomFactorChanged(1)

    @Slot()
    def onContentChanged(self) -> None:
        self.is_document_changed = True

    @Slot()
    def closeApplication(self) -> None:
        self.closeDocument()
        self.ui.close()

    @Slot()
    def newDocument(self) -> None:
        if self.is_document_open and self.is_document_changed:
            message: QMessageBox = QMessageBox(
                QMessageBox.Icon.Warning,
                "File not saved",
                "Do you want to save your changes?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                self.ui,
            )
            if message.exec() == QMessageBox.StandardButton.Yes:
                self.saveDocument()

        self.ui.text_editor.file_component.setDocumentFile(DocumentFile.default_file())
        self.filepath = ""
        self.is_document_open = True
        self.is_document_changed = False

    @Slot()
    def openDocument(self) -> None:
        if self.is_document_open and self.is_document_changed:
            message: QMessageBox = QMessageBox(
                QMessageBox.Icon.Warning,
                "File not saved",
                "Do you want to save your changes?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                self.ui,
            )
            if message.exec() == QMessageBox.StandardButton.Yes:
                self.saveDocument()

        filepath, _ = QFileDialog.getOpenFileName(filter="Vort file (*.vrt)", dir=resource_path("./vort/document"))

        if self.filepath != filepath:
            self.ui.text_editor.file_component.loadDocumentFile(filepath)
            self.filepath = filepath
            self.is_document_open = True
            self.is_document_changed = False

    @Slot()
    def closeDocument(self) -> None:
        if self.is_document_open:
            if self.is_document_changed:
                message: QMessageBox = QMessageBox(
                    QMessageBox.Icon.Warning,
                    "File not saved",
                    "Do you want to save your changes?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    self.ui,
                )
                if message.exec() == QMessageBox.StandardButton.Yes:
                    self.saveDocument()

            self.ui.text_editor.file_component.closeDocumentFile()

            self.filepath = ""
            self.is_document_open = False
            self.is_document_changed = False

    @Slot()
    def saveDocument(self) -> None:
        if self.is_document_open and self.is_document_changed:
            if self.filepath == "":
                filepath, _ = QFileDialog.getSaveFileName(
                    filter="Vort file (*.vrt)", dir=resource_path("./vort/document")
                )
                self.ui.text_editor.file_component.saveDocumentFile(filepath)
                self.filepath = filepath
            else:
                self.ui.text_editor.file_component.saveDocumentFile(self.filepath)

            self.is_document_changed = False

    # history

    @Slot()
    def undo(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().history_component.undo()

    @Slot()
    def redo(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().history_component.redo()

    # copy paste

    @Slot()
    def cut(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().clipboard_component.cut()

    @Slot()
    def copy(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().clipboard_component.copy()

    @Slot()
    def paste(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().clipboard_component.paste()

    @Slot()
    def pastePlain(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().clipboard_component.pastePlain()

    # select

    @Slot()
    def selectAll(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().selection_component.selectDocument()

    # search

    @Slot()
    def find(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.find(self.ui.find_line.findData())

    @Slot(bool)
    def onUserCaseTurned(self, is_case: bool) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.setCaseTurned(is_case)

    @Slot(bool)
    def onTextEditorCaseTurned(self, is_case: bool) -> None:
        self.ui.find_line.setCaseTurned(is_case)

    @Slot(bool)
    def onUserWholeTurned(self, is_whole: bool) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.setWholeTurned(is_whole)

    @Slot(bool)
    def onTextEditorWholeTurned(self, is_whole: bool) -> None:
        self.ui.find_line.setWholeTurned(is_whole)

    @Slot(bool)
    def onUserRegexTurned(self, is_regex: bool) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.setRegexTurned(is_regex)

    @Slot(bool)
    def onTextEditorRegexTurned(self, is_regex: bool) -> None:
        self.ui.find_line.setRegexTurned(is_regex)

    @Slot()
    def replace(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.replace(self.ui.replace_line.replaceData())

    @Slot()
    def replaceAll(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            editor_context.text_editor.context().finder_component.replaceAll(self.ui.replace_line.replaceData())

    # insert

    @Slot()
    def insertImage(self) -> None:
        editor_context: DocumentEditorContext | None = self.ui.text_editor.context()

        if editor_context is None:
            return

        context: EditImageDialogContext = EditImageDialogContext()

        context.image = editor_context.text_editor.context().selection_component.selectedImage()

        if not editor_context.text_editor.context().cursor.hasSelection():
            editor_context.text_editor.context().selection_component.selectImage()

        dialog: EditImageDialog = EditImageDialog(context)

        if dialog.exec():
            editor_context.text_editor.context().clipboard_component.insertImage(context.image)

    @Slot()
    def insertHyperlink(self) -> None:
        editor_context: DocumentEditorContext | None = self.ui.text_editor.context()

        if editor_context is None:
            return

        context: EditHyperlinkDialogContext = EditHyperlinkDialogContext()

        context.hyperlink = editor_context.text_editor.context().selection_component.selectedHyperlink()

        if not editor_context.text_editor.context().cursor.hasSelection():
            editor_context.text_editor.context().selection_component.selectHyperlink()

        context.text = editor_context.text_editor.context().selection_component.selectedText()

        dialog: EditHyperlinkDialog = EditHyperlinkDialog(context)

        if dialog.exec():
            editor_context.text_editor.context().clipboard_component.insertHyperlink(context.text, context.hyperlink)

    # font

    @Slot(str)
    def onUserFontFamilyChanged(self, font_family: str) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setFontFamily(font_family)
            self.ui.text_editor.blockSignals(False)

    @Slot(str)
    def onTextEditorFontFamilyChanged(self, font_family: str) -> None:
        self.ui.font_family_combo_box.setFontFamily(font_family)

    @Slot(int)
    def onUserFontSizeChanged(self, font_size: int) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setFontSize(font_size)
            self.ui.text_editor.blockSignals(False)

    @Slot(int)
    def onTextEditorFontSizeChanged(self, font_size: int) -> None:
        self.ui.font_size_combo_box.setFontSize(font_size)

    # format

    @Slot(bool)
    def onUserBoldTurned(self, is_bold) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setBold(is_bold)
            self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorBoldTurned(self, is_bold) -> None:
        self.ui.turn_bold_action.setChecked(is_bold)

    @Slot(bool)
    def onUserItalicTurned(self, is_italic) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setItalic(is_italic)
            self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorItalicTurned(self, is_italic) -> None:
        self.ui.turn_italic_action.setChecked(is_italic)

    @Slot(bool)
    def onUserUnderlinedTurned(self, is_underlined) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setUnderlined(is_underlined)
            self.ui.text_editor.blockSignals(False)

    @Slot(bool)
    def onTextEditorUnderlinedTurned(self, is_underlined) -> None:
        self.ui.turn_underlined_action.setChecked(is_underlined)

    # color

    @Slot(QColor)
    def onUserForegroundColorChanged(self, color: QColor) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setForegroundColor(color)
            self.ui.text_editor.blockSignals(False)

    @Slot(QColor)
    def onTextEditorForegroundColorChanged(self, color: QColor) -> None:
        self.ui.foreground_color_picker.setColor(color)

    @Slot(QColor)
    def onUserBackgroundColorChanged(self, color: QColor) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().char_component.setBackgroundColor(color)
            self.ui.text_editor.blockSignals(False)

    @Slot(QColor)
    def onTextEditorBackgroundColorChanged(self, color: QColor) -> None:
        self.ui.background_color_picker.setColor(color)

    # alignment

    @Slot(Qt.AlignmentFlag)
    def onUserParagraphAlignmentChanged(self, alignment: Qt.AlignmentFlag) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setAlignment(alignment)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onTextEditorAlignmentChanged(self, alignment: Qt.AlignmentFlag) -> None:
        self.ui.set_alignment_left_action.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.ui.set_alignment_center_action.setChecked(alignment == Qt.AlignmentFlag.AlignHCenter)
        self.ui.set_alignment_right_action.setChecked(alignment == Qt.AlignmentFlag.AlignRight)

    @Slot()
    def setAlignmentLeft(self) -> None:
        self.onUserParagraphAlignmentChanged(Qt.AlignmentFlag.AlignLeft)

    @Slot()
    def setAlignmentCenter(self) -> None:
        self.onUserParagraphAlignmentChanged(Qt.AlignmentFlag.AlignHCenter)

    @Slot()
    def setAlignmentRight(self) -> None:
        self.onUserParagraphAlignmentChanged(Qt.AlignmentFlag.AlignRight)

    # indent

    @Slot(float)
    def onUserFirstLineIndentChanged(self, indent: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setFirstLineIndent(indent)
            self.ui.text_editor.blockSignals(False)

    @Slot(int)
    def onUserIndentChanged(self, indent: int) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setIndent(indent)
            self.ui.text_editor.blockSignals(False)

    @Slot()
    def indentRight(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.indentRight()
            self.ui.text_editor.blockSignals(False)

    @Slot()
    def indentLeft(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.indentLeft()
            self.ui.text_editor.blockSignals(False)

    # space

    @Slot(float)
    def onUserIndentStepChanged(self, step: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().layout.setIndentStep(step)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onUserLineSpacingChanged(self, spacing: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setLineSpacing(spacing)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onTextEditorLineSpacingChanged(self, spacing: float) -> None:
        self.ui.set_line_spacing_1_action.setChecked(spacing == 1.0)
        self.ui.set_line_spacing_1_15_action.setChecked(spacing == 1.15)
        self.ui.set_line_spacing_1_5_action.setChecked(spacing == 1.5)
        self.ui.set_line_spacing_2_action.setChecked(spacing == 2.0)

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
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setTopMargin(margin)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onUserParagraphBottomMarginChanged(self, margin: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setBottomMargin(margin)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onUserParagraphLeftMarginChanged(self, margin: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setLeftMargin(margin)
            self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onUserParagraphRightMarginChanged(self, margin: float) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().paragraph_component.setRightMargin(margin)
            self.ui.text_editor.blockSignals(False)

    # style

    @Slot()
    def openStyle(self) -> None:
        dialog: StyleDialogUI = StyleDialogUI()
        dialog.exec()

    @Slot()
    def newStyle(self) -> None:
        dialog: NewStyleDialogUI = NewStyleDialogUI()
        dialog.exec()

    @Slot()
    def applyStyle(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().text_style_component.setTextStyle(self.ui.style_combo_box.style())
            self.ui.text_editor.blockSignals(False)

    @Slot()
    def clearStyle(self) -> None:
        editor_context = self.ui.text_editor.context()
        if editor_context is not None:
            self.ui.text_editor.blockSignals(True)
            editor_context.text_editor.context().text_style_component.clearTextStyle()
            self.ui.text_editor.blockSignals(False)

    # settings

    @Slot(str)
    def openSettings(self, name: str) -> None:
        editor_context: DocumentEditorContext | None = self.ui.text_editor.context()

        if editor_context is None:
            return

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()

        px_to_cm: float = 2.54 / dpi
        px_to_mm: float = 25.4 / dpi

        page_context: PageSettingsContext = PageSettingsContext()
        page_context.page_width = editor_context.page_layout.pageWidth() * px_to_cm
        page_context.page_height = editor_context.page_layout.pageHeight() * px_to_cm
        page_context.page_spacing = editor_context.page_layout.pageSpacing() * px_to_cm
        page_context.page_color = editor_context.page_layout.pageColor()
        page_context.page_top_margin = editor_context.page_layout.pageTopMargin() * px_to_cm
        page_context.page_bottom_margin = editor_context.page_layout.pageBottomMargin() * px_to_cm
        page_context.page_left_margin = editor_context.page_layout.pageLeftMargin() * px_to_cm
        page_context.page_right_margin = editor_context.page_layout.pageRightMargin() * px_to_cm
        page_context.page_top_padding = editor_context.page_layout.pageTopPadding() * px_to_cm
        page_context.page_bottom_padding = editor_context.page_layout.pageBottomPadding() * px_to_cm
        page_context.page_left_padding = editor_context.page_layout.pageLeftPadding() * px_to_cm
        page_context.page_right_padding = editor_context.page_layout.pageRightPadding() * px_to_cm
        page_context.border_width = editor_context.page_layout.borderWidth() * px_to_mm
        page_context.border_color = editor_context.page_layout.borderColor()

        paragraph_context: ParagraphSettingsContext = ParagraphSettingsContext()
        paragraph_context.alignment = editor_context.text_editor.context().paragraph_component.alignment()
        paragraph_context.first_line_indent = (
            editor_context.text_editor.context().paragraph_component.firstLineIndent() * px_to_cm
        )
        paragraph_context.indent = editor_context.text_editor.context().paragraph_component.indent()
        paragraph_context.indent_step = editor_context.text_editor.context().layout.indentStep() * px_to_cm
        paragraph_context.line_spacing = editor_context.text_editor.context().paragraph_component.lineSpacing()
        paragraph_context.top_margin = editor_context.text_editor.context().paragraph_component.topMargin() * px_to_cm
        paragraph_context.bottom_margin = (
            editor_context.text_editor.context().paragraph_component.bottomMargin() * px_to_cm
        )
        paragraph_context.left_margin = editor_context.text_editor.context().paragraph_component.leftMargin() * px_to_cm
        paragraph_context.right_margin = (
            editor_context.text_editor.context().paragraph_component.rightMargin() * px_to_cm
        )

        header_context: HeaderSettingsContext = HeaderSettingsContext()
        header_context.height = editor_context.page_layout.headerHeight() * px_to_cm
        header_context.alignment = editor_context.header_editor.context().formatting_component.alignment()
        header_context.font_family = editor_context.header_editor.context().formatting_component.fontFamily()
        header_context.font_size = editor_context.header_editor.context().formatting_component.fontSize()
        header_context.text_background_color = editor_context.header_editor.context().formatting_component.textBackgroundColor()  # type: ignore
        header_context.text_foreground_color = editor_context.header_editor.context().formatting_component.textForegroundColor()  # type: ignore
        header_context.is_first_page_included = editor_context.header_editor.context().page_component.isFirstPageIncluded()  # type: ignore
        header_context.is_pagination_turned = editor_context.header_editor.context().pagination_component.isPaginationTurned()  # type: ignore
        header_context.pagination_starting_number = editor_context.header_editor.context().pagination_component.paginationStartingNumber()  # type: ignore
        header_context.is_text_turned = editor_context.header_editor.context().text_component.isTextTurned()
        header_context.text = editor_context.header_editor.context().text_component.text()

        footer_context: FooterSettingsContext = FooterSettingsContext()
        footer_context.height = editor_context.page_layout.footerHeight() * px_to_cm
        footer_context.alignment = editor_context.footer_editor.context().formatting_component.alignment()
        footer_context.font_family = editor_context.footer_editor.context().formatting_component.fontFamily()
        footer_context.font_size = editor_context.footer_editor.context().formatting_component.fontSize()
        footer_context.text_background_color = editor_context.footer_editor.context().formatting_component.textBackgroundColor()  # type: ignore
        footer_context.text_foreground_color = editor_context.footer_editor.context().formatting_component.textForegroundColor()  # type: ignore
        footer_context.is_first_page_included = editor_context.footer_editor.context().page_component.isFirstPageIncluded()  # type: ignore
        footer_context.is_pagination_turned = editor_context.footer_editor.context().pagination_component.isPaginationTurned()  # type: ignore
        footer_context.pagination_starting_number = editor_context.footer_editor.context().pagination_component.paginationStartingNumber()  # type: ignore
        footer_context.is_text_turned = editor_context.footer_editor.context().text_component.isTextTurned()
        footer_context.text = editor_context.footer_editor.context().text_component.text()

        settings_context: SettingsContext = SettingsContext()
        settings_context.page_context = page_context
        settings_context.paragraph_context = paragraph_context
        settings_context.header_context = header_context
        settings_context.footer_context = footer_context

        dialog: SettingsDialog = SettingsDialog(settings_context, self.ui)
        dialog.openTab(name)
        dialog.applied.connect(self.onSettingsApplied)
        dialog.exec()

    @Slot(SettingsContext)
    def onSettingsApplied(self, context: SettingsContext) -> None:
        editor_context: DocumentEditorContext | None = self.ui.text_editor.context()

        if editor_context is None:
            return

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px: float = dpi / 2.54
        mm_to_px: float = dpi / 25.4

        page_context: PageSettingsContext = context.page_context
        editor_context.page_layout.setPageWidth(page_context.page_width * cm_to_px)
        editor_context.page_layout.setPageHeight(page_context.page_height * cm_to_px)
        editor_context.page_layout.setPageSpacing(page_context.page_spacing * cm_to_px)
        editor_context.page_layout.setPageColor(page_context.page_color)
        editor_context.page_layout.setPageTopMargin(page_context.page_top_margin * cm_to_px)
        editor_context.page_layout.setPageBottomMargin(page_context.page_bottom_margin * cm_to_px)
        editor_context.page_layout.setPageLeftMargin(page_context.page_left_margin * cm_to_px)
        editor_context.page_layout.setPageRightMargin(page_context.page_right_margin * cm_to_px)
        editor_context.page_layout.setPageTopPadding(page_context.page_top_padding * cm_to_px)
        editor_context.page_layout.setPageBottomPadding(page_context.page_bottom_padding * cm_to_px)
        editor_context.page_layout.setPageLeftPadding(page_context.page_left_padding * cm_to_px)
        editor_context.page_layout.setPageRightPadding(page_context.page_right_padding * cm_to_px)
        editor_context.page_layout.setBorderWidth(page_context.border_width * mm_to_px)
        editor_context.page_layout.setBorderColor(page_context.border_color)

        paragraph_context: ParagraphSettingsContext = context.paragraph_context
        self.onUserParagraphAlignmentChanged(paragraph_context.alignment)
        self.onUserFirstLineIndentChanged(paragraph_context.first_line_indent * cm_to_px)
        self.onUserIndentChanged(paragraph_context.indent)
        self.onUserIndentStepChanged(paragraph_context.indent_step * cm_to_px)
        self.onUserLineSpacingChanged(paragraph_context.line_spacing)
        self.onTextEditorLineSpacingChanged(paragraph_context.line_spacing)
        self.onUserParagraphTopMarginChanged(paragraph_context.top_margin * cm_to_px)
        self.onUserParagraphBottomMarginChanged(paragraph_context.bottom_margin * cm_to_px)
        self.onUserParagraphLeftMarginChanged(paragraph_context.left_margin * cm_to_px)
        self.onUserParagraphRightMarginChanged(paragraph_context.right_margin * cm_to_px)

        header_context: HeaderSettingsContext = context.header_context
        editor_context.page_layout.setHeaderHeight(header_context.height * cm_to_px)
        editor_context.header_editor.context().formatting_component.setAlignment(header_context.alignment)
        editor_context.header_editor.context().formatting_component.setFontFamily(header_context.font_family)
        editor_context.header_editor.context().formatting_component.setFontSize(header_context.font_size)
        editor_context.header_editor.context().formatting_component.setTextBackgroundColor(header_context.text_background_color)  # type: ignore
        editor_context.header_editor.context().formatting_component.setTextForegroundColor(header_context.text_foreground_color)  # type: ignore
        editor_context.header_editor.context().page_component.setFirstPageIncluded(header_context.is_first_page_included)  # type: ignore
        editor_context.header_editor.context().pagination_component.setPaginationTurned(header_context.is_pagination_turned)  # type: ignore
        editor_context.header_editor.context().pagination_component.setPaginationStartingNumber(header_context.pagination_starting_number)  # type: ignore
        editor_context.header_editor.context().text_component.setTextTurned(header_context.is_text_turned)
        editor_context.header_editor.context().text_component.setText(header_context.text)

        footer_context: FooterSettingsContext = context.footer_context
        editor_context.page_layout.setFooterHeight(footer_context.height * cm_to_px)
        editor_context.footer_editor.context().formatting_component.setAlignment(footer_context.alignment)
        editor_context.footer_editor.context().formatting_component.setFontFamily(footer_context.font_family)
        editor_context.footer_editor.context().formatting_component.setFontSize(footer_context.font_size)
        editor_context.footer_editor.context().formatting_component.setTextBackgroundColor(footer_context.text_background_color)  # type: ignore
        editor_context.footer_editor.context().formatting_component.setTextForegroundColor(footer_context.text_foreground_color)  # type: ignore
        editor_context.footer_editor.context().page_component.setFirstPageIncluded(footer_context.is_first_page_included)  # type: ignore
        editor_context.footer_editor.context().pagination_component.setPaginationTurned(footer_context.is_pagination_turned)  # type: ignore
        editor_context.footer_editor.context().pagination_component.setPaginationStartingNumber(footer_context.pagination_starting_number)  # type: ignore
        editor_context.footer_editor.context().text_component.setTextTurned(footer_context.is_text_turned)
        editor_context.footer_editor.context().text_component.setText(footer_context.text)

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

    # about

    def showAbout(self) -> None:
        dialog: AboutDialog = AboutDialog(self.ui)
        dialog.exec()

    # status

    @Slot(int)
    def onTextEditorCharacterCountChanged(self, character_count: int) -> None:
        self.ui.character_count.blockSignals(True)
        self.ui.character_count.setCharCount(character_count)
        self.ui.character_count.blockSignals(False)

    @Slot(float)
    def onUserZoomFactorChanged(self, zoom_factor: float) -> None:
        self.ui.text_editor.blockSignals(True)
        self.ui.text_editor.ui.setZoomFactor(zoom_factor)
        self.ui.text_editor.blockSignals(False)

    @Slot(float)
    def onTextEditorZoomFactorChanged(self, zoom_factor: float) -> None:
        self.ui.zoom_slider.blockSignals(True)
        self.ui.zoom_slider.setZoomFactor(zoom_factor)
        self.ui.zoom_slider.blockSignals(False)
