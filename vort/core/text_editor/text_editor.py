from PySide6.QtCore import Qt, Signal, QObject, Slot, QRectF, QTimer, QEvent
from PySide6.QtWidgets import QWidget, QGraphicsScene, QToolTip
from PySide6.QtGui import (
    QGuiApplication,
    QKeyEvent,
    QMouseEvent,
    QTextDocument,
    QTextCursor,
    QFont,
    QKeyEvent,
    QTextCharFormat,
    QTextBlockFormat,
    QColor,
    QDesktopServices,
)

from util import PointF

from core.text_editor.text_editor_ui import TextEditorUI

from core.text_editor.component.history_component import HistoryComponent
from core.text_editor.component.select_component import SelectComponent
from core.text_editor.component.font_component import FontComponent
from core.text_editor.component.format_component import FormatComponent
from core.text_editor.component.color_component import ColorComponent
from core.text_editor.component.spacing_component import SpacingComponent
from core.text_editor.component.move_component import MoveComponent
from core.text_editor.component.input_component import InputComponent

from core.text_editor.layout.text_canvas import TextCanvas
from core.text_editor.layout.text_document_layout import TextDocumentLayout, HitResult, Hit
from core.text_editor.layout.page_layout import PageLayout

from core.text_editor.document_file import DocumentFile


# text editor only supports one cursor at a time


class DocumentContext:
    def __init__(
        self,
        text_document: QTextDocument,
        page_layout: PageLayout,
        text_document_layout: TextDocumentLayout,
        text_cursor: QTextCursor,
        text_canvas: TextCanvas,
    ) -> None:
        self.text_document: QTextDocument = text_document
        self.page_layout: PageLayout = page_layout
        self.text_document_layout: TextDocumentLayout = text_document_layout
        self.text_cursor: QTextCursor = text_cursor
        self.text_canvas: TextCanvas = text_canvas


class TextEditor(QObject):
    fontFamilyChanged = Signal(str)

    fontSizeChnaged = Signal(int)

    boldTurned = Signal(bool)
    italicTurned = Signal(bool)
    underlinedTurned = Signal(bool)

    foregroundColorChanged = Signal(QColor)
    backgroundColorChanged = Signal(QColor)

    firstLineIndentTurned = Signal(bool)

    pageCountChanged = Signal(int)

    characterCountChanged = Signal(int)
    zoomFactorSelected = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: TextEditorUI = TextEditorUI(parent)

        self.__scene: QGraphicsScene = QGraphicsScene(parent)
        self.ui.setScene(self.__scene)

        self.__document_context: DocumentContext | None = None

        # mouse cursor

        self.__last_hit_result: HitResult = HitResult()
        self.__cursor_timer: QTimer = QTimer(self)
        self.__cursor_timer.setInterval(100)
        self.__cursor_timer.timeout.connect(self.updateCursorShape)
        self.__cursor_timer.start()

        # signal

        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseReleased.connect(self.onMouseReleased)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.mouseLeft.connect(self.onMouseLeft)
        self.ui.mouseDoubleClicked.connect(self.onMouseDoubleClicked)

        self.ui.zoomFactorChanged.connect(self.zoomFactorSelected.emit)

    # TODO: DEBUG
    def test(self) -> None:
        if self.__document_context is not None:
            print(self.__document_context.page_layout.width())
            print(self.__document_context.page_layout.height())
        else:
            print("NONE")

        self.repaintViewport()
        pass

    def test2(self) -> None:

        self.repaintViewport()
        return

    def setDocument(self, document_file: DocumentFile) -> None:
        text_document = document_file.text_document

        page_layout: PageLayout = PageLayout()

        page_layout.setPageWidth(document_file.page_width)
        page_layout.setPageHeight(document_file.page_height)
        page_layout.setPageSpacing(document_file.page_spacing)
        page_layout.setPageColor(document_file.page_color)
        page_layout.setPageTopMargin(document_file.page_top_margin)
        page_layout.setPageBottomMargin(document_file.page_bottom_margin)
        page_layout.setPageLeftMargin(document_file.page_left_margin)
        page_layout.setPageRightMargin(document_file.page_right_margin)
        page_layout.setPageTopPadding(document_file.page_top_padding)
        page_layout.setPageBottomPadding(document_file.page_bottom_padding)
        page_layout.setPageLeftPadding(document_file.page_left_padding)
        page_layout.setPageRightPadding(document_file.page_right_padding)
        page_layout.setBorderWidth(document_file.border_width)
        page_layout.setBorderColor(document_file.border_color)
        page_layout.setHeaderHeight(document_file.header_height)
        page_layout.setFooterHeight(document_file.footer_height)

        self.ui.horizontalScrollBar().setPageStep(int(page_layout.pageWidth()))
        self.ui.verticalScrollBar().setPageStep(int(page_layout.pageHeight()))

        page_layout.changed.connect(self.onPageLayoutChanged)

        text_document_layout: TextDocumentLayout = TextDocumentLayout(text_document, page_layout)
        text_document.setDocumentLayout(text_document_layout)

        text_document_layout.setDefaultIndentStep(document_file.default_indent_step)
        text_document_layout.setHyperlinkBoldTurned(document_file.is_hyperlink_bold_turned)
        text_document_layout.setHyperlinkBold(document_file.is_hyperlink_bold)
        text_document_layout.setHyperlinkItalicTurned(document_file.is_hyperlink_italic_turned)
        text_document_layout.setHyperlinkItalic(document_file.is_hyperlink_italic)
        text_document_layout.setHyperlinkUnderlinedTurned(document_file.is_hyperlink_underlined_turned)
        text_document_layout.setHyperlinkUnderlined(document_file.is_hyperlink_underlined)
        text_document_layout.setHyperlinkBackgroundColorTurned(document_file.is_hyperlink_background_color_turned)
        text_document_layout.setHyperlinkBackgroundColor(document_file.hyperlink_background_color)
        text_document_layout.setHyperlinkForegroundColorTurned(document_file.is_hyperlink_foreground_color_turned)
        text_document_layout.setHyperlinkForegroundColor(document_file.hyperlink_foreground_color)

        text_document_layout.characterCountChanged.connect(self.characterCountChanged.emit)

        text_cursor: QTextCursor = QTextCursor(text_document)

        self.history_component: HistoryComponent = HistoryComponent(text_cursor)
        self.history_component.applied.connect(self.repaintViewport)
        self.history_component.applied.connect(self.onCursorPositionChanged)

        self.select_component: SelectComponent = SelectComponent(text_cursor)
        self.select_component.applied.connect(self.repaintViewport)

        self.font_component: FontComponent = FontComponent(text_cursor)
        self.font_component.applied.connect(self.repaintViewport)

        self.format_component: FormatComponent = FormatComponent(text_cursor)
        self.format_component.applied.connect(self.repaintViewport)

        self.color_component: ColorComponent = ColorComponent(text_cursor)
        self.color_component.applied.connect(self.repaintViewport)

        self.spacing_component: SpacingComponent = SpacingComponent(text_cursor)
        self.spacing_component.applied.connect(self.repaintViewport)

        self.move_component: MoveComponent = MoveComponent(text_cursor)
        self.move_component.applied.connect(self.repaintViewport)
        self.move_component.applied.connect(self.onCursorPositionChanged)

        self.input_component: InputComponent = InputComponent(text_cursor)
        self.input_component.applied.connect(self.repaintViewport)
        self.input_component.applied.connect(self.onCursorPositionChanged)

        text_canvas: TextCanvas = TextCanvas(
            page_layout,
            text_document_layout,
            text_cursor,
        )

        text_canvas.headerLayout().setAlignment(document_file.header_alignment)
        text_canvas.headerLayout().setFontFamily(document_file.header_font_family)
        text_canvas.headerLayout().setFontSize(document_file.header_font_size)
        text_canvas.headerLayout().setTextBackgroundColor(document_file.header_text_background_color)
        text_canvas.headerLayout().setTextBackgroundColor(document_file.header_text_background_color)
        text_canvas.headerLayout().turnForFirstPage(document_file.is_header_turned_for_first_page)
        text_canvas.headerLayout().turnPagination(document_file.is_header_pagination_turned)
        text_canvas.headerLayout().setPaginationStartingNumber(document_file.header_pagination_starting_number)
        text_canvas.headerLayout().turnText(document_file.is_header_text_turned)
        text_canvas.headerLayout().setText(document_file.header_text)

        text_canvas.footerLayout().setAlignment(document_file.footer_alignment)
        text_canvas.footerLayout().setFontFamily(document_file.footer_font_family)
        text_canvas.footerLayout().setFontSize(document_file.footer_font_size)
        text_canvas.footerLayout().setTextBackgroundColor(document_file.footer_text_background_color)
        text_canvas.footerLayout().setTextBackgroundColor(document_file.footer_text_background_color)
        text_canvas.footerLayout().turnForFirstPage(document_file.is_footer_turned_for_first_page)
        text_canvas.footerLayout().turnPagination(document_file.is_footer_pagination_turned)
        text_canvas.footerLayout().setPaginationStartingNumber(document_file.footer_pagination_starting_number)
        text_canvas.footerLayout().turnText(document_file.is_footer_text_turned)
        text_canvas.footerLayout().setText(document_file.footer_text)

        self.__scene.addWidget(text_canvas)

        self.__document_context = DocumentContext(
            text_document, page_layout, text_document_layout, text_cursor, text_canvas
        )

    def documentContext(self) -> DocumentContext | None:
        return self.__document_context

    def setZoomFactor(self, zoom_factor: float) -> None:
        self.ui.setZoomFactor(zoom_factor)

    @Slot()
    def updateCursorShape(self) -> None:
        if self.__last_hit_result.hit == Hit.Text:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        elif self.__last_hit_result.hit == Hit.Image:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        elif self.__last_hit_result.hit == Hit.Hyperlink:
            if Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers():
                QGuiApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
            else:
                QGuiApplication.setOverrideCursor(Qt.CursorShape.IBeamCursor)
        else:
            QGuiApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    @Slot()
    def repaintViewport(self):
        self.ui.viewport().repaint()

    @Slot()
    def onPageLayoutChanged(self) -> None:
        if self.__document_context is not None:
            if (
                self.__scene.sceneRect().width != self.__document_context.page_layout.width()
                or self.__scene.sceneRect().height != self.__document_context.page_layout.height()
            ):
                self.__scene.setSceneRect(
                    QRectF(
                        0, 0, self.__document_context.page_layout.width(), self.__document_context.page_layout.height()
                    )
                )

    @Slot()
    def onCursorPositionChanged(self) -> None:
        if self.__document_context is None:
            return

        position: int = self.__document_context.text_cursor.position()
        block_point: PointF = self.__document_context.text_document_layout.positionTest(position)
        self.ui.ensureVisible(block_point.xPosition(), block_point.yPosition(), 1, 1)

        char_format: QTextCharFormat = self.__document_context.text_cursor.charFormat()
        block_format: QTextBlockFormat = self.__document_context.text_cursor.blockFormat()

        # font

        font_family: str = char_format.font().family()
        self.fontFamilyChanged.emit(font_family)

        font_size: int = char_format.font().pointSize()
        self.fontSizeChnaged.emit(font_size)

        # format

        is_bold = char_format.fontWeight() == QFont.Weight.Bold
        self.boldTurned.emit(is_bold)

        is_italic = char_format.fontItalic()
        self.italicTurned.emit(is_italic)

        is_underlined = char_format.fontUnderline()
        self.underlinedTurned.emit(is_underlined)

        # color

        foreground_color = char_format.foreground().color()
        self.foregroundColorChanged.emit(foreground_color)

        background_color = char_format.background().color()
        self.backgroundColorChanged.emit(background_color)

        # indent

        is_indent = block_format.textIndent() != 0
        self.firstLineIndentTurned.emit(is_indent)

    @Slot(QMouseEvent)
    def onMousePressed(self, event: QMouseEvent) -> None:
        if self.__document_context is None:
            return

        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__document_context.text_document_layout.pointTest(point)
        self.__last_hit_result = hit_result

        if event.button() == Qt.MouseButton.LeftButton:
            if self.__last_hit_result.hit == Hit.NoHit:
                self.__document_context.text_cursor.clearSelection()
                self.repaintViewport()
            self.move_component.pointPress(hit_result)

    @Slot(QMouseEvent)
    def onMouseReleased(self, event: QMouseEvent) -> None:
        if self.__document_context is None:
            return

        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__document_context.text_document_layout.pointTest(point)
        self.__last_hit_result = hit_result

        if (
            hit_result.hit == Hit.Hyperlink
            and Qt.KeyboardModifier.ControlModifier == QGuiApplication.queryKeyboardModifiers()
        ):
            QDesktopServices.openUrl(hit_result.hyperlink)

    @Slot(QMouseEvent)
    def onMouseDoubleClicked(self, event: QMouseEvent) -> None:
        if self.__document_context is None:
            return

        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__document_context.text_document_layout.pointTest(point)
        self.__last_hit_result = hit_result

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.select_component.selectWord(hit_result)

    @Slot(QMouseEvent)
    def onMouseMoved(self, event: QMouseEvent) -> None:
        if self.__document_context is None:
            return

        point = PointF.fromQPointF(self.ui.mapToScene(event.position().toPoint()))
        hit_result = self.__document_context.text_document_layout.pointTest(point)
        self.__last_hit_result = hit_result

        self.is_tool_tip_shown = False
        if hit_result.hit == Hit.Hyperlink and not self.is_tool_tip_shown:
            QToolTip.showText(event.globalPos(), hit_result.hyperlink)

        if hit_result.hit != Hit.Hyperlink:
            QToolTip.hideText()
            self.is_tool_tip_shown = False

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move_component.pointMove(hit_result)

    @Slot(QEvent)
    def onMouseLeft(self, event: QEvent) -> None:
        if self.__document_context is None:
            return

        self.__last_hit_result = HitResult()

    @Slot(QKeyEvent)
    def onKeyPressed(self, event: QKeyEvent) -> None:
        if self.__document_context is None:
            return

        self.move_component.keyPress(event.key())
        self.input_component.input(event)
