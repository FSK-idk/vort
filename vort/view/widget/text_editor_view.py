from PySide6.QtWidgets import QWidget, QAbstractScrollArea, QSizePolicy
from PySide6.QtGui import (
    QKeyEvent,
    QMouseEvent,
    QTextDocument,
    QTextCursor,
    QColor,
    QPalette,
    QPaintEvent,
    QPainter,
    QResizeEvent,
    QKeyEvent,
    QTextCharFormat,
)
from PySide6.QtCore import Qt, QEvent, Signal

from utils.point_f import PointF
from utils.rect_f import RectF

from model.page_model import PAGE_WIDTH, PAGE_HEIGHT

from view.widget.text_document_layout_view import TextDocumentLayoutView, Selection, PaintContext

from controller.controller import Controller


class TextEditorView(QAbstractScrollArea):
    mousePressed = Signal(QMouseEvent)
    mouseReleased = Signal(QMouseEvent)
    mouseMoved = Signal(QMouseEvent)
    keyPressed = Signal(QKeyEvent)
    keyReleased = Signal(QKeyEvent)
    resized = Signal(QResizeEvent)
    paintedDocument = Signal(QPaintEvent)

    pageCountChanged = Signal(int)
    characterCountChanged = Signal(int)

    def __init__(self, controller: Controller, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # widget

        self.document = QTextDocument()
        self.document_layout: TextDocumentLayoutView = TextDocumentLayoutView(self.document)

        # scroll bar

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.verticalScrollBar().setPageStep(PAGE_HEIGHT)
        self.verticalScrollBar().setSingleStep(4)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.horizontalScrollBar().setPageStep(PAGE_WIDTH)
        self.horizontalScrollBar().setSingleStep(4)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setupSignal()

    def setDocument(self, document: QTextDocument) -> None:
        self.document = document
        self.document_layout = TextDocumentLayoutView(document)
        self.document.setDocumentLayout(self.document_layout)

        self.setupSignal()

    def setupSignal(self) -> None:
        self.document_layout.pageCountChanged.connect(self.updateScrollBar)
        self.document_layout.pageCountChanged.connect(self.pageCountChanged.emit)
        self.document_layout.characterCountChanged.connect(self.characterCountChanged.emit)

    def paint_document(self, rect: RectF, text_cursor: QTextCursor) -> None:
        painter: QPainter = QPainter(self.viewport())

        screen_x = self.horizontalScrollBar().value()
        screen_y = self.verticalScrollBar().value()

        rect.move(PointF(screen_x, screen_y))

        palette: QPalette = QPalette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor("red"))
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor("white"))

        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(QColor("blue"))
        format.setForeground(QColor("white"))

        selections: list[Selection] = []
        if text_cursor.hasSelection():
            selections.append(Selection(text_cursor, format))

        context = PaintContext(rect, text_cursor.position(), palette, selections)
        self.document_layout.draw(painter, context)

    def hitTest(self, point: PointF) -> int:
        return self.document_layout.hitTest(point)

    def updateScrollBar(self) -> None:
        viewport_width = self.viewport().width()
        viewport_height = self.viewport().height()

        vertical_scroll_bar_range = self.document_layout.page_layout.height() - viewport_height
        if vertical_scroll_bar_range < 0:
            vertical_scroll_bar_range = 0
        self.verticalScrollBar().setRange(0, int(vertical_scroll_bar_range))

        horizontal_scroll_bar_range = self.document_layout.page_layout.width() - viewport_width
        if horizontal_scroll_bar_range < 0:
            horizontal_scroll_bar_range = 0
        self.horizontalScrollBar().setRange(0, int(horizontal_scroll_bar_range))

    def resize(self, point: PointF) -> None:
        self.document_layout.resizePageLayout(point)
        self.updateScrollBar()

    def event(self, event: QEvent) -> bool:
        if isinstance(event, QKeyEvent):
            match event.type():
                case QEvent.Type.KeyPress:
                    self.keyPressed.emit(event)
                    return True
                case QEvent.Type.KeyRelease:
                    self.keyReleased.emit(event)
                    return True
        if isinstance(event, QPaintEvent):
            match event.type():
                case QEvent.Type.Paint:
                    self.viewport().repaint()
                    return True

        return super().event(event)

    def viewportEvent(self, event: QEvent) -> bool:
        if isinstance(event, QMouseEvent):
            match event.type():
                case QEvent.Type.MouseButtonPress:
                    self.mousePressed.emit(event)
                    return True
                case QEvent.Type.MouseButtonRelease:
                    self.mouseReleased.emit(event)
                    return True
                case QEvent.Type.MouseMove:
                    self.mouseMoved.emit(event)
                    return True
        elif isinstance(event, QResizeEvent):
            match event.type():
                case QEvent.Type.Resize:
                    self.resized.emit(event)
                    return True
        elif isinstance(event, QPaintEvent):
            match event.type():
                case QEvent.Type.Paint:
                    self.paintedDocument.emit(event)
                    return True

        return super().viewportEvent(event)
