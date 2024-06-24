from PySide6.QtWidgets import QPlainTextDocumentLayout
from PySide6.QtGui import QAbstractTextDocumentLayout, QTextDocument, \
      QTextBlock, QTextLayout, QTextLine, QPainter, QTextCursor, QTextFrame, QFont, QFontMetricsF, QPalette, QTextFrameFormat
from PySide6.QtCore import QPointF, QRectF, QSizeF, Qt, QObject


class DocumentLayout(QAbstractTextDocumentLayout):
    def __init__(self, doc: QTextDocument) -> None:
        super().__init__(doc)

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        padding: float = self.document().rootFrame().frameFormat().padding()
        margin: float = self.document().rootFrame().frameFormat().margin()

        height: float = margin + padding
        left_position: float = margin + padding

        for i in range(self.document().blockCount()):
            block_layout: QTextLayout = self.document().findBlockByNumber(i).layout()
    
            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()

            line_width = self.document().rootFrame().frameFormat().width().rawValue() - left_position * 2
            while line.isValid():
                line.setLineWidth(line_width)
                line.setPosition(QPointF(left_position, height))
                height += line.height()
                line: QTextLine = block_layout.createLine()
            block_layout.endLayout()

        self.update.emit()

    def draw(self, painter: QPainter, context: QAbstractTextDocumentLayout.PaintContext):
        clip: QRectF = context.clip  # type: ignore
        cursor_position: int = context.cursorPosition  # type: ignore
        palette: QPalette = context.palette  # type: ignore
        selections: list[QTextLayout.FormatRange] = context.selections  # type: ignore

        carriage_position: QPointF = QPointF(0, 0)
        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            block_position: int = block.position()
            block_length: int = block.length()

            if cursor_position >= block_position and cursor_position < block_position + block_length:
                block_layout.drawCursor(painter, carriage_position, cursor_position - block_position)

            block_layout.draw(painter, carriage_position, selections, clip)

        # print("block count:", self.document().findBlockByNumber(self.document().blockCount()-1).isValid(), ", cursor pos:", cursor_position, ", clip:", clip)

        painter.drawLine(clip.topRight(), clip.bottomRight());

        self.update.emit()

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def frameBoundingRect(self, frame: QTextFrame) -> QRectF:
        first_block: QTextBlock = frame.firstCursorPosition().block()
        last_block: QTextBlock = frame.lastCursorPosition().block()
        first_rect: QRectF = self.blockBoundingRect(first_block)
        last_rect: QRectF = self.blockBoundingRect(last_block)
        frame_rect: QRectF = first_rect.united(last_rect)
        return frame_rect

    def documentSize(self) -> QSizeF:
        root_frame: QTextFrame = self.document().rootFrame()
        root_frame_rect: QRectF = self.frameBoundingRect(root_frame)
        return root_frame_rect.size()

    def hitTest(self, point: QPointF, accuracy: Qt.HitTestAccuracy) -> int:
        print(point.toTuple())
        return 0
        # root_frame: QTextFrame = self.document().rootFrame()
        # root_frame_format: QTextFrameFormat = root_frame.frameFormat()
        # position: int = 0

        # print(root_frame.children())

        # position = 0

        # print(position)
        # return position
