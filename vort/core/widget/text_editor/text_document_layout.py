from PySide6.QtCore import QPointF, Signal, QRect, QRectF
from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QTextDocument,
    QTextBlock,
    QTextLayout,
    QTextLine,
    QPainter,
    QTextCursor,
    QTextCharFormat,
    QColor,
    QTextBlockFormat,
    QGuiApplication,
    QTextInlineObject,
    QTextFormat,
    QTextFragment,
    QTextImageFormat,
    QImage,
)

from util import PointF, RectF

from core.widget.text_editor.page_layout import PageLayout


class Selection:
    def __init__(
        self,
        cursor: QTextCursor = QTextCursor(),
        format: QTextCharFormat = QTextCharFormat(),
    ) -> None:
        self.cursor: QTextCursor = cursor
        self.format: QTextCharFormat = format


class PaintContext:
    def __init__(
        self,
        painter: QPainter = QPainter(),
        viewport_rect: RectF = RectF(),
        cursor_position: int = -1,
        selections: list[Selection] = [],
        page_color: QColor = QColor("white"),
    ) -> None:
        self.painter = painter
        self.viewport_rect: RectF = viewport_rect
        self.cursor_position: int = cursor_position
        self.selections: list[Selection] = selections
        self.page_color: QColor = page_color


class TextDocumentLayout(QAbstractTextDocumentLayout):
    sizeChanged = Signal(PointF)
    characterCountChanged = Signal(int)

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)

        self.__character_count: int = 0
        self.page_layout: PageLayout = PageLayout()

        # TODO: to config
        dpi = QGuiApplication.screens()[0].logicalDotsPerInch()
        self.__default_indent_step: float = 1 * dpi / 2.54

        self.page_layout.sizeChanged.connect(self.sizeChanged.emit)

    def pageCount(self) -> int:
        return self.page_layout.pageCount()

    def characterCount(self) -> int:
        return self.__character_count

        -alignment
        -heading_level
        -images
        -hyperlinks

        # image_format = block.charFormat().toImageFormat()
        # print(image_format.width(), image_format.height(), image_format.name())

        # print("start:",end="")
        # k: QTextBlock.iterator = block.begin()
        # while k != block.end():
        #     frag: QTextFragment = k.fragment()
        #     if frag.charFormat().toImageFormat().isImageFormat():
        #         form: QTextImageFormat = frag.charFormat().toImageFormat()
        #         img: QImage = QImage(self.document().resource(QTextDocument.ResourceType.ImageResource, form.name()))
        #         if not img.isNull():
        #             print("got")

        #         print(form.width(),"=image",end="")

        #     print(frag.length(),end=",")

        #     k += 1
        # print("end")

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        # it isn't as complicated as you may think

        character_count: int = 0
        page_count: int = 1

        root_x = self.page_layout.pageMargin() + self.page_layout.pagePadding()
        root_y = self.page_layout.pageMargin() + self.page_layout.pagePadding()

        root_width_reduce: float = (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
        remaining_text_height: float = (
            self.page_layout.pageHeight() - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
        )

        document: QTextDocument = self.document()

        for i in range(self.document().blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_format: QTextBlockFormat = block.blockFormat()

            block_x = block_format.indent() * self.__default_indent_step + block_format.leftMargin()
            block_y = 0

            block_width_reduce: float = (
                block_format.indent() * self.__default_indent_step
                + block_format.leftMargin()
                + block_format.rightMargin()
            )

            # --line parsing
            # if first line
            #   calc
            #   if new page:
            #       do more
            # else:
            #   calc
            #   if new page:
            #       do more
            # --bottom margin parsing
            # calc
            # if new page:
            #   do more

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()
            is_first_line = True
            while line.isValid():
                if is_first_line:
                    line.setLineWidth(
                        self.page_layout.pageWidth()
                        - root_width_reduce
                        - block_width_reduce
                        - block_format.textIndent()
                    )

                    if remaining_text_height - line.height() - block_format.topMargin() <= 0:
                        if self.page_layout.pageCount() == page_count:
                            self.page_layout.addPage()
                        page_count += 1

                        root_y += (
                            remaining_text_height
                            + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                            + self.page_layout.spacing()
                        )

                        remaining_text_height = (
                            self.page_layout.pageHeight()
                            - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                        )

                        line.setLineWidth(
                            self.page_layout.pageWidth()
                            - root_width_reduce
                            - block_width_reduce
                            - block_format.textIndent()
                        )

                    block_y += block_format.topMargin()
                    line_x = block_format.textIndent()
                    line.setPosition(QPointF(root_x + block_x + line_x, root_y + block_y))
                    block_y += line.height() * block_format.lineHeight()

                    remaining_text_height -= line.height() * block_format.lineHeight() + block_format.topMargin()

                    is_first_line = False

                else:
                    line.setLineWidth(self.page_layout.pageWidth() - root_width_reduce - block_width_reduce)

                    if remaining_text_height - line.height() <= 0:
                        if self.page_layout.pageCount() == page_count:
                            self.page_layout.addPage()
                        page_count += 1

                        block_y += (
                            remaining_text_height
                            + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                            + self.page_layout.spacing()
                        )

                        remaining_text_height = (
                            self.page_layout.pageHeight()
                            - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                        )

                        line.setLineWidth(self.page_layout.pageWidth() - root_width_reduce - block_width_reduce)

                    line.setPosition(QPointF(root_x + block_x, root_y + block_y))
                    block_y += line.height() * block_format.lineHeight()

                    remaining_text_height -= line.height() * block_format.lineHeight()

                character_count += line.textLength()

                line = block_layout.createLine()

            root_y += block_y

            if remaining_text_height - block_format.bottomMargin() <= 0:
                if self.page_layout.pageCount() == page_count:
                    self.page_layout.addPage()
                page_count += 1

                root_y += (
                    remaining_text_height
                    + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                    + self.page_layout.spacing()
                )

                remaining_text_height = (
                    self.page_layout.pageHeight() - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                )

            else:
                root_y += block_format.bottomMargin()
                remaining_text_height -= block_format.bottomMargin()

            block_layout.endLayout()

        if self.page_layout.pageCount() > page_count:
            self.page_layout.removePage(self.page_layout.pageCount() - page_count)

        if self.__character_count != character_count:
            self.__character_count = character_count
            self.characterCountChanged.emit(self.__character_count)

        self.update.emit()

    def paint(self, context: PaintContext):
        self.paintPage(context)
        self.paintText(context)

        self.update.emit()

    def paintPage(self, context: PaintContext) -> None:
        painter: QPainter = context.painter
        viewport_rect: RectF = context.viewport_rect
        page_color: QColor = context.page_color

        current_x_position: float = 0
        current_y_position: float = 0

        for i in range(self.page_layout.pageCount()):
            page_rect: RectF = RectF(
                current_x_position,
                current_y_position,
                self.page_layout.pageWidth(),
                self.page_layout.pageHeight(),
            )
            clip = page_rect.toQRectF().intersected(viewport_rect.toQRectF())

            painter.fillRect(clip, page_color)

            current_y_position += self.page_layout.pageHeight() + self.page_layout.spacing()

    def paintText(self, context: PaintContext):
        painter: QPainter = context.painter
        viewport_rect: RectF = context.viewport_rect
        cursor_position: int = context.cursor_position
        selections: list[Selection] = context.selections

        carriage_position: QPointF = QPointF(0, 0)

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_position: int = block.position()
            block_length: int = block.length()

            format_ranges: list[QTextLayout.FormatRange] = []

            for selection in selections:
                selection_start: int = selection.cursor.selectionStart() - block_position
                selection_end: int = selection.cursor.selectionEnd() - block_position
                if selection_start < block_length and selection_end > 0:
                    format_range: QTextLayout.FormatRange = QTextLayout.FormatRange()
                    format_range.start = selection_start  # type: ignore
                    format_range.length = selection_end - selection_start  # type: ignore
                    format_range.format = selection.format  # type: ignore
                    format_ranges.append(format_range)

            block_layout.draw(painter, carriage_position, format_ranges, viewport_rect.toQRectF())

            if cursor_position >= block_position and cursor_position < block_position + block_length and not selections:
                block_layout.drawCursor(painter, carriage_position, cursor_position - block_position)

    def hitTest(self, point: PointF) -> int:
        current_cursor_position = 0

        document = self.document()
        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_rect: RectF = RectF.fromQRectF(block_layout.boundingRect())

            if block_rect.contains(point):
                for j in range(block_layout.lineCount()):
                    line: QTextLine = block_layout.lineAt(j)
                    line_rect: RectF = RectF.fromQRectF(line.rect())

                    if line_rect.contains(point):
                        x_position = point.xPosition()
                        line_cursor_position = line.xToCursor(
                            x_position, QTextLine.CursorPosition.CursorBetweenCharacters
                        )
                        current_cursor_position += line_cursor_position

                        return current_cursor_position

            current_cursor_position += block.length()

        return -1

    def blockTest(self, position: int) -> PointF:
        current_cursor_position = 0

        document = self.document()
        for i in range(document.blockCount()):
            block: QTextBlock = document.findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            if block.contains(position):
                for j in range(block_layout.lineCount()):
                    line: QTextLine = block_layout.lineAt(j)

                    if current_cursor_position + line.textLength() >= position:
                        a, _ = line.cursorToX(position, QTextLine.Edge.Leading)  # type: ignore
                        return PointF(a, line.y())

                    current_cursor_position += line.textLength()

            current_cursor_position += block.length()

        return PointF(-1, -1)
