from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QAbstractScrollArea, QFrame, QPushButton, QSizePolicy
from PySide6.QtGui import QKeyEvent, QTextDocument, QTextCursor, QTextFrame, QTextFrameFormat, QBrush, QColor, \
      QPalette, QPaintEvent, QPainter, QResizeEvent, QKeyEvent, QTextFormat
from PySide6.QtCore import Qt, QSize, QEvent, QRect, QPoint, QRectF, Signal

from model.page import Page
from model.page_layout import PageLayout

from view.widget.document_layout import DocumentLayout


class EditorWidget(QAbstractScrollArea):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__page_width: float = 250
        self.__page_height: float = 250
        self.__page_margin: float = 50
        self.__page_padding: float = 20
        self.__page_spacing: float = 10

        self.page_layout: PageLayout = PageLayout()
        self.page_layout.setPageWidth(self.__page_width)
        self.page_layout.setPageHeight(self.__page_height)
        self.page_layout.setSpacing(self.__page_spacing)

        self.page_layout.append(Page())
        self.page_layout.append(Page())
        self.page_layout.append(Page())
        self.page_layout.append(Page())

        self.document: QTextDocument = QTextDocument()
        self.document_layout: DocumentLayout = DocumentLayout(self.document)
        self.document.setDocumentLayout(self.document_layout)
        self.document.setPageSize(QSize(self.__page_width, self.__page_height))

        self.text_cursor: QTextCursor = QTextCursor(self.document)

        root_frame: QTextFrame = self.document.rootFrame()
        root_frame_format: QTextFrameFormat = root_frame.frameFormat()
        root_frame_format.setWidth(self.__page_width)
        root_frame_format.setHeight(self.__page_height)
        root_frame_format.setMargin(self.__page_margin)
        root_frame_format.setPadding(self.__page_padding)
        root_frame_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash)
        root_frame_format.setBorderBrush(QBrush(Qt.GlobalColor.blue))
        root_frame_format.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_Auto)
        self.document.rootFrame().setFrameFormat(root_frame_format)

        # TODO: DEBUG
        # self.print_info()

        # # Layout

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.verticalScrollBar().setPageStep(self.__page_height)
        self.verticalScrollBar().setSingleStep(2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.horizontalScrollBar().setPageStep(self.__page_width)
        self.horizontalScrollBar().setSingleStep(2)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event: QPaintEvent) -> None:
        # print("Paint", event)

        # Paint pages

        painter: QPainter = QPainter(self.viewport())

        screen_x = self.horizontalScrollBar().value()
        screen_y = self.verticalScrollBar().value()

        rect_x = event.rect().x() + screen_x
        rect_y = event.rect().y() + screen_y
        rect_w = event.rect().width()
        rect_h = event.rect().height()

        rect = QRect(rect_x, rect_y, rect_w, rect_h)
        paint_event: QPaintEvent = QPaintEvent(rect)
        self.page_layout.paint(painter, paint_event)

        # Paint text

        clip_x = self.page_layout.xPosition()
        clip_y = self.page_layout.yPosition()
        clip_w = event.rect().width()
        clip_h = event.rect().height()

        # painter.setRect(QRectF(clip_x, clip_y, clip_w, clip_h))
        context = DocumentLayout.PaintContext()
        context.clip: QRectF = QRectF(clip_x, clip_y, clip_w, clip_h)  # type: ignore
        context.cursorPosition: int = self.text_cursor.position()  # type: ignore
        context.palette: QPalette = QPalette()  # type: ignore
        context.palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor("red"))  # type: ignore
        context.selections: list[QTextLayout.FormatRange] = []  # type: ignore

        self.document_layout.draw(painter, context)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # print("Key Pressed", event)

        match event.key():
            case Qt.Key.Key_Up:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Up)
            case Qt.Key.Key_Left:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Left)
            case Qt.Key.Key_Down:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Down)
            case Qt.Key.Key_Right:
                self.text_cursor.movePosition(QTextCursor.MoveOperation.Right)

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
        # print("Resize", event)
        self.page_layout.onResizeEvent(event)

        page_layout_width = self.page_layout.width()
        page_layout_height = self.page_layout.height()
        
        viewport_width = self.viewport().width()
        viewport_height = self.viewport().height()

        vertical_scroll_bar_range = page_layout_height - viewport_height
        if vertical_scroll_bar_range < 0:
            vertical_scroll_bar_range = 0
        self.verticalScrollBar().setRange(0, int(vertical_scroll_bar_range))

        horizontal_scroll_bar_range = (page_layout_width - viewport_width) / 2
        if horizontal_scroll_bar_range < 0:
            horizontal_scroll_bar_range = 0
        self.horizontalScrollBar().setRange(0, int(horizontal_scroll_bar_range))


    # TODO: DEBUG
    def test(self) -> None:
        self.print_info()
        pass

    # TODO: DEBUG
    def print_info(self) -> None:
        pass
        # format_: QTextFrameFormat = self.text_edit.document().rootFrame().frameFormat()
        # print("Root Frame Format:")
        # print("width:", format_.width().rawValue())
        # print("height:", format_.height().rawValue())
        # print("margin:", format_.margin())
        # print("padding:", format_.padding())
