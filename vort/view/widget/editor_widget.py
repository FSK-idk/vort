from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QAbstractScrollArea, QFrame, QPushButton, QSizePolicy
from PySide6.QtGui import (
    QKeyEvent,
    QMouseEvent,
    QTextDocument,
    QTextCursor,
    QTextFrame,
    QTextFrameFormat,
    QBrush,
    QColor,
    QPalette,
    QPaintEvent,
    QPainter,
    QFont,
    QResizeEvent,
    QKeyEvent,
    QTextFormat,
    QTextCharFormat,
)
from PySide6.QtCore import Qt, QSize, QEvent, QRect, QPoint, QRectF, Signal

from utils.point_f import PointF
from utils.rect_f import RectF

from model import Page, PageLayout
from model.page import PAGE_WIDTH, PAGE_HEIGHT

from view.widget.document_layout import DocumentLayout, PaintContext


class EditorWidget(QAbstractScrollArea):
    cursorPositionChanged = Signal(int)
    fontWeightChanged = Signal(QFont.Weight)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.document: QTextDocument = QTextDocument()
        self.document_layout: DocumentLayout = DocumentLayout(self.document)
        self.document.setDocumentLayout(self.document_layout)

        self.text_cursor: QTextCursor = QTextCursor(self.document)

        self.document_layout.pageCountChanged.connect(self.updateScrollBar)

        # setup

        self.setupScrollBar()

        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

    def setupScrollBar(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.verticalScrollBar().setPageStep(PAGE_HEIGHT)
        self.verticalScrollBar().setSingleStep(4)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.horizontalScrollBar().setPageStep(PAGE_WIDTH)
        self.horizontalScrollBar().setSingleStep(4)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self.viewport())

        screen_x = self.horizontalScrollBar().value()
        screen_y = self.verticalScrollBar().value()

        rect_x = event.rect().x() + screen_x
        rect_y = event.rect().y() + screen_y
        rect_w = event.rect().width()
        rect_h = event.rect().height()

        rect = RectF(rect_x, rect_y, rect_w, rect_h)

        # TODO: Add palette colors
        palette: QPalette = QPalette()
        context = PaintContext(rect, self.text_cursor.position(), palette)

        self.document_layout.draw(painter, context)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.horizontalScrollBar().value()
            screen_y = self.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.document_layout.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position)
                self.viewport().repaint()

                self.cursorPositionChanged.emit(position)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        match event.key():
            case Qt.Key.Key_Up:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Up)
                self.cursorPositionChanged.emit(self.text_cursor.position())
            case Qt.Key.Key_Left:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Left)
                self.cursorPositionChanged.emit(self.text_cursor.position())
            case Qt.Key.Key_Down:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Down)
                self.cursorPositionChanged.emit(self.text_cursor.position())
            case Qt.Key.Key_Right:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Right)
                self.cursorPositionChanged.emit(self.text_cursor.position())

        if event.text():
            if event.text():
                if event.text() == "\r":  # Enter
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertBlock()
                    self.text_cursor.setPosition(self.text_cursor.block().position())
                    self.text_cursor.endEditBlock()
                elif event.text() == "\b":  # Backspace
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                elif event.text() == "\u007F":  # Delete
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                else:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertText(event.text())
                    self.text_cursor.endEditBlock()

        # TODO: debug
        # print("end?", self.text_cursor.atEnd())
        # print("start?", self.text_cursor.atStart())
        # print("cursor pos:", self.text_cursor.position())
        # print(self.document.pageCount())

        self.viewport().repaint()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.document_layout.resize(PointF(event.size().width(), event.size().height()))
        self.updateScrollBar()

    def updateScrollBar(self) -> None:
        viewport_width = self.viewport().width()
        viewport_height = self.viewport().height()

        vertical_scroll_bar_range = self.document_layout.page_layout.height() - viewport_height
        if vertical_scroll_bar_range < 0:
            vertical_scroll_bar_range = 0
        self.verticalScrollBar().setRange(0, int(vertical_scroll_bar_range))

        horizontal_scroll_bar_range = (self.document_layout.page_layout.width() - viewport_width) / 2
        if horizontal_scroll_bar_range < 0:
            horizontal_scroll_bar_range = 0
        self.horizontalScrollBar().setRange(0, int(horizontal_scroll_bar_range))

    def setBold(self, is_bold) -> None:
        font_weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(font_weight)
        self.text_cursor.mergeCharFormat(format)

    def onCursorPositionChanged(self, position) -> None:
        format: QTextCharFormat = self.document_layout.format(position)
        self.fontWeightChanged.emit(format.fontWeight())

    # TODO: DEBUG
    def test(self) -> None:
        # format_: QTextFrameFormat = self.text_edit.document().rootFrame().frameFormat()
        # print("Root Frame Format:")
        # print("width:", format_.width().rawValue())
        # print("height:", format_.height().rawValue())
        # print("margin:", format_.margin())
        # print("padding:", format_.padding())
        pass
