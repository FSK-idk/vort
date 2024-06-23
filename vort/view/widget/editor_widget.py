from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QAbstractScrollArea, QFrame, QPushButton, QSizePolicy
from PySide6.QtGui import QTextDocument, QTextCursor, QTextFrame, QTextFrameFormat, QBrush, QColor, \
      QPalette, QPaintEvent, QPainter, QResizeEvent
from PySide6.QtCore import Qt, QSize, QEvent, QRect, QPoint, QRectF

from model.page import Page
from model.page_layout import PageLayout

from view.widget.document_layout import DocumentLayout


class EditorWidget(QAbstractScrollArea):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__page_width: float = 360
        self.__page_height: float = 480
        self.__page_margin: float = 50
        self.__page_padding: float = 20
        self.__page_spacing: float = 10

        # self.document = QTextDocument()

        self.page_layout: PageLayout = PageLayout()
        self.page_layout.setPageWidth(self.__page_width)
        self.page_layout.setPageHeight(self.__page_height)
        self.page_layout.setSpacing(self.__page_spacing)

        self.page_layout.append(Page())
        self.page_layout.append(Page())
        self.page_layout.append(Page())
        self.page_layout.append(Page())


        # self.text_edit.setFixedWidth(self.__page_width)
        # self.text_edit.setFixedHeight(self.__page_height)

        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # self.text_edit.document().setPageSize(QSize(self.__page_width, self.__page_height))

        # document_layout: DocumentLayout = DocumentLayout(self.text_edit.document())
        # self.text_edit.document().setDocumentLayout(document_layout)

        # root_frame: QTextFrame = self.text_edit.document().rootFrame()
        # root_frame_format: QTextFrameFormat = root_frame.frameFormat()
        # root_frame_format.setWidth(self.__page_width)
        # root_frame_format.setHeight(self.__page_height)
        # root_frame_format.setMargin(self.__page_margin)
        # root_frame_format.setPadding(self.__page_padding)
        # root_frame_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash)
        # root_frame_format.setBorderBrush(QBrush(Qt.GlobalColor.blue))
        # self.text_edit.document().rootFrame().setFrameFormat(root_frame_format)

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

        # page_layout_width = self.page_layout.width()
        # page_layout_height = self.page_layout.height()
        
        # viewport_height = self.viewport().height()

        # vertical_scroll_bar_range = viewport_height - page_layout_height
        # if vertical_scroll_bar_range < 0:
        #     vertical_scroll_bar_range = 0

        # self.verticalScrollBar().setRange(0, int(vertical_scroll_bar_range))

    def paintEvent(self, event: QPaintEvent) -> None:
        # print("Paint", event)
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
