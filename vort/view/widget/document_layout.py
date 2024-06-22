from PySide6.QtWidgets import QPlainTextDocumentLayout 
from PySide6.QtGui import QAbstractTextDocumentLayout, QTextDocument, \
      QTextBlock, QTextLayout, QTextLine, QPainter, QTextCursor, QTextFrame, QFont, QFontMetricsF
from PySide6.QtCore import QPointF, QRectF, QSizeF, Qt

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
        for i in range(self.document().blockCount()):
            block_layout: QTextLayout = self.document().findBlockByNumber(i).layout()
            block_layout.draw(painter, QPointF(0, 0))

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
        # TODO: Add later
        print(point.toTuple())
        return 0