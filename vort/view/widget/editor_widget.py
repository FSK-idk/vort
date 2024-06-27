from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QTextEdit,
    QVBoxLayout,
    QAbstractScrollArea,
    QFrame,
    QPushButton,
    QSizePolicy,
)
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
from PySide6.QtCore import Qt, QSize, QEvent, QRect, QPoint, QRectF, Signal, QFlag

from utils.point_f import PointF
from utils.rect_f import RectF

from model import Page, PageLayout
from model.page import PAGE_WIDTH, PAGE_HEIGHT

from view.widget.document_layout import DocumentLayout, Selection, PaintContext


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

    # def viewportEvent(self, event: QEvent) -> bool:
    #     if isinstance(event, ...): ...
    #     return True
    def viewportEvent(self, event: QEvent) -> bool:
        return super().viewportEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self.viewport())

        screen_x = self.horizontalScrollBar().value()
        screen_y = self.verticalScrollBar().value()

        rect_x = event.rect().x() + screen_x
        rect_y = event.rect().y() + screen_y
        rect_w = event.rect().width()
        rect_h = event.rect().height()

        rect = RectF(rect_x, rect_y, rect_w, rect_h)

        palette: QPalette = QPalette()
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor("red"))
        palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor("white"))

        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(QColor("blue"))
        format.setForeground(QColor("white"))

        selections: list[Selection] = [Selection(self.text_cursor, format)]

        context = PaintContext(rect, self.text_cursor.position(), palette, selections)
        self.document_layout.draw(painter, context)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.horizontalScrollBar().value()
            screen_y = self.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.document_layout.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
                self.viewport().repaint()

                self.cursorPositionChanged.emit(position)

            self.mouse_pressed = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.horizontalScrollBar().value()
            screen_y = self.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.document_layout.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)

                self.viewport().repaint()
                self.cursorPositionChanged.emit(position)
        pass

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        # print(event)
        pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.handleNavigationInput(event)
        self.handleHotkeys(event)
        self.handleTextInput(event)

    def handleNavigationInput(self, event: QKeyEvent) -> None:
        move_mode = None
        move_operation = None

        if Qt.KeyboardModifier.ShiftModifier in event.modifiers():
            move_mode = QTextCursor.MoveMode.KeepAnchor
        else:
            move_mode = QTextCursor.MoveMode.MoveAnchor

        if Qt.KeyboardModifier.ControlModifier in event.modifiers():
            match event.key():
                case Qt.Key.Key_Left:
                    move_operation = QTextCursor.MoveOperation.WordLeft
                case Qt.Key.Key_Right:
                    move_operation = QTextCursor.MoveOperation.WordRight
                case Qt.Key.Key_Up:
                    move_operation = QTextCursor.MoveOperation.PreviousBlock
                case Qt.Key.Key_Down:
                    move_operation = QTextCursor.MoveOperation.NextBlock
                case Qt.Key.Key_Home:
                    move_operation = QTextCursor.MoveOperation.StartOfBlock
                case Qt.Key.Key_End:
                    move_operation = QTextCursor.MoveOperation.EndOfBlock
        else:
            match event.key():
                case Qt.Key.Key_Left:
                    move_operation = QTextCursor.MoveOperation.Left
                case Qt.Key.Key_Right:
                    move_operation = QTextCursor.MoveOperation.Right
                case Qt.Key.Key_Up:
                    move_operation = QTextCursor.MoveOperation.Up
                case Qt.Key.Key_Down:
                    move_operation = QTextCursor.MoveOperation.Down
                case Qt.Key.Key_Home:
                    move_operation = QTextCursor.MoveOperation.StartOfLine
                case Qt.Key.Key_End:
                    move_operation = QTextCursor.MoveOperation.EndOfLine

        if move_mode and move_operation:
            self.text_cursor.movePosition(move_operation, move_mode)
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.viewport().repaint()

    def handleHotkeys(self, event: QKeyEvent) -> None:
        used = True

        if Qt.KeyboardModifier.ControlModifier in event.modifiers():
            match event.key():
                case Qt.Key.Key_X if self.text_cursor.hasSelection():
                    selected_text = self.text_cursor.selectedText()
                    QApplication.clipboard().setText(selected_text)
                    self.text_cursor.removeSelectedText()
                case Qt.Key.Key_C if self.text_cursor.hasSelection():
                    selected_text = self.text_cursor.selectedText()
                    QApplication.clipboard().setText(selected_text)
                case Qt.Key.Key_V:
                    copied_text = QApplication.clipboard().text()
                    self.text_cursor.insertText(copied_text)
                case Qt.Key.Key_A:
                    self.text_cursor.select(QTextCursor.SelectionType.Document)
                case Qt.Key.Key_Z:
                    self.document.undo(self.text_cursor)
                case Qt.Key.Key_Y:
                    self.document.redo(self.text_cursor)
                case _:
                    used = False

        if used:
            self.viewport().repaint()

    def handleTextInput(self, event: QKeyEvent) -> None:
        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier] and event.text():
            if event.key() == Qt.Key.Key_Enter:
                self.text_cursor.beginEditBlock()
                self.text_cursor.insertBlock()
                self.text_cursor.setPosition(self.text_cursor.block().position())
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Backspace:
                self.text_cursor.beginEditBlock()
                self.text_cursor.deletePreviousChar()
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Delete:
                self.text_cursor.beginEditBlock()
                self.text_cursor.deleteChar()
                self.text_cursor.endEditBlock()
            elif event.key() == Qt.Key.Key_Escape:
                pass  # ignore
            else:
                self.text_cursor.beginEditBlock()
                self.text_cursor.insertText(event.text())
                self.text_cursor.endEditBlock()

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

        horizontal_scroll_bar_range = self.document_layout.page_layout.width() - viewport_width
        if horizontal_scroll_bar_range < 0:
            horizontal_scroll_bar_range = 0
        self.horizontalScrollBar().setRange(0, int(horizontal_scroll_bar_range))

    def setBold(self, is_bold) -> None:
        font_weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(font_weight)
        self.text_cursor.mergeCharFormat(format)
        self.viewport().repaint()

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
