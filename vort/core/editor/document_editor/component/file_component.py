import lzma
import pickle

from PySide6.QtCore import Qt, QObject, Signal, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QTextDocument,
    QTextCursor,
    QTextCharFormat,
    QTextBlockFormat,
    QFont,
    QColor,
)

from core.editor.page_layout.page_layout import PageLayout
from core.editor.text_editor.text_document_layout import TextDocumentLayout
from core.editor.text_editor.text_document_context import TextDocumentContext
from core.editor.text_editor.text_editor import TextEditor
from core.editor.header_editor.header_document_layout import HeaderDocumentLayout
from core.editor.header_editor.header_document_context import HeaderDocumentContext
from core.editor.header_editor.header_editor import HeaderEditor
from core.editor.footer_editor.footer_document_layout import FooterDocumentLayout
from core.editor.footer_editor.footer_document_context import FooterDocumentContext
from core.editor.footer_editor.footer_editor import FooterEditor

from core.editor.document_editor.document_editor_context import DocumentEditorContext
from core.editor.document_editor.document_canvas import DocumentCanvas
from core.editor.document_file import DocumentFile


class FileComponent(QObject):
    contextChanged: Signal = Signal(DocumentEditorContext)
    contextCleared: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.__context: DocumentEditorContext | None = None

    def saveDocumentFile(self, filepath) -> None:
        try:
            with lzma.open(filepath, "wb") as f:
                pickle.dump(self.documentFile(), f)

        except FileNotFoundError:
            print("File not found")

    def loadDocumentFile(self, filepath) -> None:
        try:
            with lzma.open(filepath, "rb") as f:
                self.setDocumentFile(pickle.load(f))

        except FileNotFoundError:
            print("File not found")

    def documentFile(self) -> DocumentFile:
        file = DocumentFile()

        if self.__context is None:
            return file

        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        px_to_cm = 2.54 / dpi
        px_to_mm = 25.4 / dpi

        page_layout: PageLayout = self.__context.page_layout
        text_context: TextDocumentContext = self.__context.text_editor.context()
        header_context: HeaderDocumentContext = self.__context.header_editor.context()
        footer_context: FooterDocumentContext = self.__context.footer_editor.context()

        file.html_text = text_context.document.toHtml()
        file.png_image = {}

        for image_format in text_context.layout.imageLayout():
            name: str = image_format.name

            image: QImage = text_context.document.resource(QTextDocument.ResourceType.ImageResource, image_format.name)

            bytes_array: QByteArray = QByteArray()
            buffer: QBuffer = QBuffer(bytes_array)
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            image.save(buffer, "png")
            image_bytes: bytes = bytes_array.data()

            file.png_image[name] = image_bytes

        file.page_width = page_layout.pageWidth() * px_to_cm
        file.page_height = page_layout.pageHeight() * px_to_cm
        file.page_spacing = page_layout.pageSpacing() * px_to_cm
        file.page_color = page_layout.pageColor()
        file.page_top_margin = page_layout.pageTopMargin() * px_to_cm
        file.page_bottom_margin = page_layout.pageBottomMargin() * px_to_cm
        file.page_left_margin = page_layout.pageLeftMargin() * px_to_cm
        file.page_right_margin = page_layout.pageRightMargin() * px_to_cm
        file.page_top_padding = page_layout.pageTopPadding() * px_to_cm
        file.page_bottom_padding = page_layout.pageBottomPadding() * px_to_cm
        file.page_left_padding = page_layout.pageLeftPadding() * px_to_cm
        file.page_right_padding = page_layout.pageRightPadding() * px_to_cm
        file.border_width = page_layout.borderWidth() * px_to_mm
        file.border_color = page_layout.borderColor()
        file.header_height = page_layout.headerHeight() * px_to_cm
        file.footer_height = page_layout.footerHeight() * px_to_cm

        file.default_indent_step = text_context.layout.indentStep() * px_to_cm
        file.is_hyperlink_bold_turned = text_context.layout.isHyperlinkBoldTurned()
        file.is_hyperlink_bold = text_context.layout.isHyperlinkBold()
        file.is_hyperlink_italic_turned = text_context.layout.isHyperlinkItalicTurned()
        file.is_hyperlink_italic = text_context.layout.isHyperlinkItalic()
        file.is_hyperlink_underlined_turned = text_context.layout.isHyperlinkUnderlinedTurned()
        file.is_hyperlink_underlined = text_context.layout.isHyperlinkUnderlined()
        file.is_hyperlink_background_color_turned = text_context.layout.isHyperlinkBackgroundColorTurned()
        file.hyperlink_background_color = text_context.layout.hyperlinkBackgroundColor()
        file.is_hyperlink_foreground_color_turned = text_context.layout.isHyperlinkForegroundColorTurned()
        file.hyperlink_foreground_color = text_context.layout.hyperlinkForegroundColor()

        file.header_alignment = header_context.formatting_component.alignment()
        file.header_font_family = header_context.formatting_component.fontFamily()
        file.header_font_size = header_context.formatting_component.fontSize()
        file.header_text_background_color = header_context.formatting_component.textBackgroundColor()
        file.header_text_background_color = header_context.formatting_component.textBackgroundColor()
        file.is_header_first_page_included = header_context.page_component.isFirstPageIncluded()
        file.is_header_pagination_turned = header_context.pagination_component.isPaginationTurned()
        file.header_pagination_starting_number = header_context.pagination_component.paginationStartingNumber()
        file.is_header_text_turned = header_context.text_component.isTextTurned()
        file.header_text = header_context.text_component.text()

        file.footer_alignment = footer_context.formatting_component.alignment()
        file.footer_font_family = footer_context.formatting_component.fontFamily()
        file.footer_font_size = footer_context.formatting_component.fontSize()
        file.footer_text_background_color = footer_context.formatting_component.textBackgroundColor()
        file.footer_text_background_color = footer_context.formatting_component.textBackgroundColor()
        file.is_footer_first_page_included = footer_context.page_component.isFirstPageIncluded()
        file.is_footer_pagination_turned = footer_context.pagination_component.isPaginationTurned()
        file.footer_pagination_starting_number = footer_context.pagination_component.paginationStartingNumber()
        file.is_footer_text_turned = footer_context.text_component.isTextTurned()
        file.footer_text = footer_context.text_component.text()

        return file

    def setDocumentFile(self, file: DocumentFile) -> None:
        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()

        cm_to_px = dpi / 2.54
        mm_to_px = dpi / 25.4

        # page

        page_layout: PageLayout = PageLayout()

        page_layout.setPageWidth(file.page_width * cm_to_px)
        page_layout.setPageHeight(file.page_height * cm_to_px)
        page_layout.setPageSpacing(file.page_spacing * cm_to_px)
        page_layout.setPageColor(file.page_color)
        page_layout.setPageTopMargin(file.page_top_margin * cm_to_px)
        page_layout.setPageBottomMargin(file.page_bottom_margin * cm_to_px)
        page_layout.setPageLeftMargin(file.page_left_margin * cm_to_px)
        page_layout.setPageRightMargin(file.page_right_margin * cm_to_px)
        page_layout.setPageTopPadding(file.page_top_padding * cm_to_px)
        page_layout.setPageBottomPadding(file.page_bottom_padding * cm_to_px)
        page_layout.setPageLeftPadding(file.page_left_padding * cm_to_px)
        page_layout.setPageRightPadding(file.page_right_padding * cm_to_px)
        page_layout.setBorderWidth(file.border_width * mm_to_px)
        page_layout.setBorderColor(file.border_color)
        page_layout.setHeaderHeight(file.header_height * cm_to_px)
        page_layout.setFooterHeight(file.footer_height * cm_to_px)

        # text

        text_document: QTextDocument = QTextDocument()

        text_layout: TextDocumentLayout = TextDocumentLayout(text_document, page_layout)
        text_document.setDocumentLayout(text_layout)

        text_cursor: QTextCursor = QTextCursor(text_document)

        text_context: TextDocumentContext = TextDocumentContext(text_document, text_layout, text_cursor)

        text_editor: TextEditor = TextEditor(text_context)

        text_cursor.insertHtml(file.html_text)

        for name, image_bytes in file.png_image.items():
            bytes_array: QByteArray = QByteArray(image_bytes)
            image: QImage = QImage()
            image.loadFromData(bytes_array, "PNG")

            text_document.addResource(QTextDocument.ResourceType.ImageResource, name, image)

        # set default format if it is empty document
        if text_document.characterCount() == 1:
            char_format: QTextCharFormat = QTextCharFormat()
            char_format.setFontFamilies(["Segoe UI"])
            char_format.setFontPointSize(16)
            char_format.setBackground(QColor("transparent"))
            char_format.setForeground(QColor("black"))
            char_format.setFontWeight(QFont.Weight.Normal)
            char_format.setFontItalic(False)
            char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)

            block_format: QTextBlockFormat = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
            block_format.setTextIndent(0)
            block_format.setIndent(0)
            block_format.setLineHeight(1, 1)
            block_format.setTopMargin(0)
            block_format.setBottomMargin(0)
            block_format.setLeftMargin(0)
            block_format.setRightMargin(0)

            text_cursor.setBlockCharFormat(char_format)
            text_cursor.setCharFormat(char_format)
            text_cursor.setBlockFormat(block_format)
            text_cursor.movePosition(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)

        text_document.clearUndoRedoStacks()

        text_context.layout.setIndentStep(file.default_indent_step * cm_to_px)
        text_context.layout.setHyperlinkBoldTurned(file.is_hyperlink_bold_turned)
        text_context.layout.setHyperlinkBold(file.is_hyperlink_bold)
        text_context.layout.setHyperlinkItalicTurned(file.is_hyperlink_italic_turned)
        text_context.layout.setHyperlinkItalic(file.is_hyperlink_italic)
        text_context.layout.setHyperlinkUnderlinedTurned(file.is_hyperlink_underlined_turned)
        text_context.layout.setHyperlinkUnderlined(file.is_hyperlink_underlined)
        text_context.layout.setHyperlinkBackgroundColorTurned(file.is_hyperlink_background_color_turned)
        text_context.layout.setHyperlinkBackgroundColor(file.hyperlink_background_color)
        text_context.layout.setHyperlinkForegroundColorTurned(file.is_hyperlink_foreground_color_turned)
        text_context.layout.setHyperlinkForegroundColor(file.hyperlink_foreground_color)

        # header

        header_document: QTextDocument = QTextDocument()

        header_layout: HeaderDocumentLayout = HeaderDocumentLayout(header_document, page_layout)
        header_document.setDocumentLayout(header_layout)

        header_cursor: QTextCursor = QTextCursor(header_document)

        header_context: HeaderDocumentContext = HeaderDocumentContext(header_document, header_layout, header_cursor)

        header_editor: HeaderEditor = HeaderEditor(header_context)

        header_context.page_component.addPage(page_layout.pageCount())
        header_context.formatting_component.setAlignment(file.header_alignment)
        header_context.formatting_component.setFontFamily(file.header_font_family)
        header_context.formatting_component.setFontSize(file.header_font_size)
        header_context.formatting_component.setTextBackgroundColor(file.header_text_background_color)
        header_context.formatting_component.setTextBackgroundColor(file.header_text_background_color)
        header_context.page_component.setFirstPageIncluded(file.is_header_first_page_included)
        header_context.pagination_component.setPaginationTurned(file.is_header_pagination_turned)
        header_context.pagination_component.setPaginationStartingNumber(file.header_pagination_starting_number)
        header_context.text_component.setTextTurned(file.is_header_text_turned)
        header_context.text_component.setText(file.header_text)

        # footer

        footer_document: QTextDocument = QTextDocument()

        footer_layout: FooterDocumentLayout = FooterDocumentLayout(footer_document, page_layout)
        footer_document.setDocumentLayout(footer_layout)

        footer_cursor: QTextCursor = QTextCursor(footer_document)

        footer_context: FooterDocumentContext = FooterDocumentContext(footer_document, footer_layout, footer_cursor)

        footer_editor: FooterEditor = FooterEditor(footer_context)

        footer_context.page_component.addPage(page_layout.pageCount())
        footer_context.formatting_component.setAlignment(file.footer_alignment)
        footer_context.formatting_component.setFontFamily(file.footer_font_family)
        footer_context.formatting_component.setFontSize(file.footer_font_size)
        footer_context.formatting_component.setTextBackgroundColor(file.footer_text_background_color)
        footer_context.formatting_component.setTextBackgroundColor(file.footer_text_background_color)
        footer_context.page_component.setFirstPageIncluded(file.is_footer_first_page_included)
        footer_context.pagination_component.setPaginationTurned(file.is_footer_pagination_turned)
        footer_context.pagination_component.setPaginationStartingNumber(file.footer_pagination_starting_number)
        footer_context.text_component.setTextTurned(file.is_footer_text_turned)
        footer_context.text_component.setText(file.footer_text)

        # canvas

        canvas: DocumentCanvas = DocumentCanvas(text_context, header_context, footer_context)

        # editor

        self.__context = DocumentEditorContext(page_layout, text_editor, header_editor, footer_editor, canvas)

        self.contextChanged.emit(self.__context)

    def closeDocumentFile(self) -> None:
        self.contextCleared.emit()
