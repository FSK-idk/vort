from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtGui import QTextDocument, QTextCursor, QTextFrame, QTextFrameFormat, QBrush, QColor
from PySide6.QtCore import Qt

from view.widget.document_layout import DocumentLayout


class EditorWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__page_width: float = 360
        self.__page_height: float = 480
        self.__page_margin: float = 50
        self.__page_padding: float = 20

        # Widget

        self.text_edit: QTextEdit = QTextEdit(self)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.text_edit.setFixedWidth(self.__page_width)
        self.text_edit.setFixedHeight(self.__page_height)

        root_frame: QTextFrame = self.text_edit.document().rootFrame()
        root_frame_format: QTextFrameFormat = root_frame.frameFormat()
        root_frame_format.setWidth(self.__page_width)
        root_frame_format.setHeight(self.__page_height)
        root_frame_format.setMargin(self.__page_margin)
        root_frame_format.setPadding(self.__page_padding)
        root_frame_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash)
        root_frame_format.setBorderBrush(QBrush(Qt.GlobalColor.blue))
        self.text_edit.document().rootFrame().setFrameFormat(root_frame_format)

        # TODO: DEBUG
        self.print_info()

        # Layout

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.text_edit)

        self.setLayout(self.main_layout)

    # TODO: DEBUG
    def test(self) -> None:
        self.print_info()
        pass

    # TODO: DEBUG
    def print_info(self) -> None:
        format_: QTextFrameFormat = self.text_edit.document().rootFrame().frameFormat()
        print("Root Frame Format:")
        print("width:", format_.width().rawValue())
        print("height:", format_.height().rawValue())
        print("margin:", format_.margin())
        print("padding:", format_.padding())
