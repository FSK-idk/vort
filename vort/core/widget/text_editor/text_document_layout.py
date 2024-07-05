from enum import Enum

from PySide6.QtCore import QPointF, Signal, QRect, QRectF, QUrl
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


class Hit(Enum):
    NoHit = 0
    Text = 1
    Image = 2
    Hyperlink = 3


class HitResult:
    def __init__(self) -> None:
        self.hit: Hit = Hit.NoHit
        self.position: int = -1
        self.point: PointF = PointF(-1, -1)
        self.data: str = ""


class ImageLayout:
    def __init__(self, image_rect: QRectF, image_name: str, image_position: int) -> None:
        self.image_rect: QRectF = image_rect
        self.image_name: str = image_name
        self.image_position: int = image_position


class Selection:
    def __init__(
        self,
        start: int = 0,
        end: int = 0,
        format: QTextCharFormat = QTextCharFormat(),
    ) -> None:
        self.start: int = start
        self.end: int = end
        self.format: QTextCharFormat = format


class PaintContext:
    def __init__(
        self,
        painter: QPainter = QPainter(),
        viewport_rect: RectF = RectF(),
        cursor_position: int = -1,
        cursor_selection: Selection | None = None,
        page_color: QColor = QColor("white"),
    ) -> None:
        self.painter = painter
        self.viewport_rect: RectF = viewport_rect
        self.cursor_position: int = cursor_position
        self.cursor_selection: Selection | None = cursor_selection
        self.page_color: QColor = page_color


class TextDocumentLayout(QAbstractTextDocumentLayout):
    sizeChanged = Signal(PointF)
    characterCountChanged = Signal(int)

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)

        self.__character_count: int = 0
        self.page_layout: PageLayout = PageLayout()

        self.__images: list[ImageLayout] = []

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
        +images
        -hyperlinks

    # fmt: off

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        # it isn't as complicated as you may think

        self.__images: list[ImageLayout] = []

        character_count: int = 0
        page_count: int = 1

        root_x = self.page_layout.pageMargin() + self.page_layout.pagePadding()
        root_y = self.page_layout.pageMargin() + self.page_layout.pagePadding()

        root_width_reduce: float = (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
        remaining_text_height: float = (
            self.page_layout.pageHeight() - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
        )
        text_height = self.page_layout.pageHeight() - (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2

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

            # block parsing structure:
            # --line parsing
            # if image
            #   calc
            #   if new page:
            #       do more
            #   continue
            # else:
            #   if first line
            #       calc
            #       if new page:
            #           do more
            #   else:
            #       calc
            #       if new page:
            #           do more
            # --bottom margin parsing
            # calc
            # if new page:
            #   do more

            # fixup in input component guarantees that if image exists then image has its own block
            # we don't support inline images

            # width, height, name, position
            image : tuple[float, float, str, int] | None = None

            it: QTextBlock.iterator = block.begin()
            if it != block.end():
                fragment: QTextFragment = it.fragment()
                if fragment.charFormat().isImageFormat():
                    image_format: QTextImageFormat = fragment.charFormat().toImageFormat()
                    image = (image_format.width(), image_format.height(), image_format.name(), fragment.position())
                    it += 1
                    if it != block.end():
                        # fixup hasn't complited yet
                        # we don't need to change layout
                        return

            if image is not None:
                image_width, image_height, image_name, image_position = image

                if (remaining_text_height != text_height) and (remaining_text_height - image_height - block_format.topMargin() - block_format.bottomMargin() <= 0) :
                    if self.page_layout.pageCount() == page_count:
                        self.page_layout.addPage()
                    page_count += 1

                    root_y += (
                        remaining_text_height
                        + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                        + self.page_layout.spacing()
                    )

                    remaining_text_height = text_height

                block_y = block_format.topMargin()
                x_image: float = root_x + block_x
                y_image: float = root_y + block_y
                self.__images.append(ImageLayout(QRectF(x_image, y_image, image_width, image_height), image_name, image_position))

                block_layout.beginLayout()
                line: QTextLine = block_layout.createLine()
                line.setLineWidth(image_width)
                line.setPosition(QPointF(x_image, y_image))
                block_layout.endLayout()

                root_y += image_height + block_format.topMargin() + block_format.bottomMargin()
                remaining_text_height -= image_height + block_format.topMargin() + block_format.bottomMargin()

                # no more lines in this block
                continue

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

                    if (remaining_text_height != text_height) and (remaining_text_height - line.height() - block_format.topMargin() <= 0):
                        if self.page_layout.pageCount() == page_count:
                            self.page_layout.addPage()
                        page_count += 1

                        root_y += (
                            remaining_text_height
                            + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                            + self.page_layout.spacing()
                        )

                        remaining_text_height = text_height

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

                    if (remaining_text_height != text_height) and ( remaining_text_height - line.height() <= 0):
                        if self.page_layout.pageCount() == page_count:
                            self.page_layout.addPage()
                        page_count += 1

                        block_y += (
                            remaining_text_height
                            + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                            + self.page_layout.spacing()
                        )

                        remaining_text_height = text_height

                        line.setLineWidth(self.page_layout.pageWidth() - root_width_reduce - block_width_reduce)

                    line.setPosition(QPointF(root_x + block_x, root_y + block_y))
                    block_y += line.height() * block_format.lineHeight()

                    remaining_text_height -= line.height() * block_format.lineHeight()

                character_count += line.textLength()

                line = block_layout.createLine()

            root_y += block_y

            if (remaining_text_height != text_height) and ( remaining_text_height - block_format.bottomMargin() <= 0):
                if self.page_layout.pageCount() == page_count:
                    self.page_layout.addPage()
                page_count += 1

                root_y += (
                    remaining_text_height
                    + (self.page_layout.pageMargin() + self.page_layout.pagePadding()) * 2
                    + self.page_layout.spacing()
                )

                remaining_text_height = text_height

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

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def paint(self, context: PaintContext):
        self.paintPage(context)
        self.paintText(context)
        self.paintImage(context)

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
        cursor_selection: Selection | None = context.cursor_selection

        carriage_position: QPointF = QPointF(0, 0)

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_position: int = block.position()
            block_length: int = block.length()

            # don't show symbol obj 
            it: QTextBlock.iterator = block.begin()
            if it != block.end():
                fragment: QTextFragment = it.fragment()
                if fragment.charFormat().isImageFormat():
                    continue

            # show hyperlinks
            selections : list[Selection] = []

            it: QTextBlock.iterator = block.begin()
            while it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.charFormat().anchorHref() != "":
                    selection = Selection()
                    selection.format = fragment.charFormat()
                    selection.format.setFontUnderline(True)
                    # TODO: in config
                    selection.format.setForeground(QColor("blue"))
                    selection.start = fragment.position()
                    selection.end = fragment.position() + fragment.length()
                    selections.append(selection)

                it += 1

            format_ranges: list[QTextLayout.FormatRange] = []

            for selection in selections:
                selection_start: int = selection.start - block_position
                selection_end: int = selection.end - block_position
                if selection_start < block_length and selection_end > 0:
                    format_range: QTextLayout.FormatRange = QTextLayout.FormatRange()
                    format_range.start = selection_start  # type: ignore
                    format_range.length = selection_end - selection_start  # type: ignore
                    format_range.format = selection.format  # type: ignore
                    format_ranges.append(format_range)

            # show cursor selection
            if cursor_selection is not None:
                selection_start: int = cursor_selection.start - block_position
                selection_end: int = cursor_selection.end - block_position
                if selection_start < block_length and selection_end > 0:
                    format_range: QTextLayout.FormatRange = QTextLayout.FormatRange()
                    format_range.start = selection_start  # type: ignore
                    format_range.length = selection_end - selection_start  # type: ignore
                    format_range.format = cursor_selection.format  # type: ignore
                    format_ranges.append(format_range)

            block_layout.draw(painter, carriage_position, format_ranges, viewport_rect.toQRectF())

            if cursor_position >= block_position and cursor_position < block_position + block_length and cursor_selection is None:
                block_layout.drawCursor(painter, carriage_position, cursor_position - block_position)

    def paintImage(self, context: PaintContext):
        painter: QPainter = context.painter
        for image_layout in self.__images:
            painter.drawImage(image_layout.image_rect, self.document().resource(QTextDocument.ResourceType.ImageResource, image_layout.image_name))

    def hitTest(self, point: PointF) -> HitResult:
        result: HitResult = HitResult()
        result.point = point

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

                        helper: QTextCursor = QTextCursor(block)
                        helper.setPosition(current_cursor_position - block.position())
                        result.data = helper.charFormat().anchorHref()
                        if result.data != "":
                            result.hit = Hit.Hyperlink
                        else:
                            result.hit = Hit.Text

                        result.position = current_cursor_position
                        return result

            current_cursor_position += block.length()

        for image_layout in self.__images:
            if image_layout.image_rect.contains(point.toQPointF()):

                result.hit = Hit.Image
                result.position = image_layout.image_position
                return result

        result.hit = Hit.NoHit
        result.position = -1
        return result

    # TODO: return HitResult
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
