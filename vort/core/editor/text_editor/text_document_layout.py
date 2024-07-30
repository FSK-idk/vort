from enum import Enum, auto

from PySide6.QtCore import QPointF, Signal, QRectF, Qt, Slot
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
    QTextFragment,
    QTextImageFormat,
    QFont,
    QPen,
    QImage,
)

from core.editor.page_layout.page_layout import PageLayout
from core.editor.document_paint_context import DocumentPaintContext


class Hit(Enum):
    NoHit = auto()
    Text = auto()
    Image = auto()
    Hyperlink = auto()


class HitResult:
    def __init__(self) -> None:
        self.hit: Hit = Hit.NoHit
        self.position: int = -1
        self.point: QPointF = QPointF(-1.0, -1.0)
        self.hyperlink: str = ""


class ImageFormat:
    def __init__(self) -> None:
        self.rect: QRectF = QRectF()
        self.name: str = ""
        self.position: int = -1


class Selection:
    def __init__(self) -> None:
        self.start: int = -1
        self.end: int = -1
        self.format: QTextCharFormat = QTextCharFormat()


class TextDocumentLayout(QAbstractTextDocumentLayout):
    characterCountChanged: Signal = Signal(int)

    def __init__(self, document: QTextDocument, page_layout: PageLayout) -> None:
        super().__init__(document)

        self.__page_layout: PageLayout = page_layout

        self.__image_layout: list[ImageFormat] = []

        self.__character_count: int = 0

        self.__indent_step: float = 0.0

        self.__is_hyperlink_bold_turned: bool = False
        self.__is_hyperlink_bold: bool = False
        self.__is_hyperlink_italic_turned: bool = False
        self.__is_hyperlink_italic: bool = False
        self.__is_hyperlink_underlined_turned: bool = True
        self.__is_hyperlink_underlined: bool = True
        self.__is_hyperlink_foreground_color_turned: bool = True
        self.__hyperlink_foreground_color: QColor = QColor("blue")
        self.__is_hyperlink_background_color_turned: bool = False
        self.__hyperlink_background_color: QColor = QColor("transparent")

        self.__cursor_selection_foreground_color: QColor = QColor("white")
        self.__cursor_selection_background_color: QColor = QColor("blue")

        self.__page_layout.internalChanged.connect(self.onPageLayoutInternalChanged)
        self.__page_layout.externalChanged.connect(self.onPageLayoutExternalChanged)

    def characterCount(self) -> int:
        return self.__character_count

    def imageLayout(self) -> list[ImageFormat]:
        return self.__image_layout

    def indentStep(self) -> float:
        return self.__indent_step

    def setIndentStep(self, step: float) -> None:
        self.__indent_step = step

    def isHyperlinkBoldTurned(self) -> bool:
        return self.__is_hyperlink_bold_turned

    def setHyperlinkBoldTurned(self, is_turned: bool) -> None:
        self.__is_hyperlink_bold_turned = is_turned

    def isHyperlinkBold(self) -> bool:
        return self.__is_hyperlink_bold

    def setHyperlinkBold(self, is_bold: bool) -> None:
        self.__is_hyperlink_bold = is_bold

    def isHyperlinkItalicTurned(self) -> bool:
        return self.__is_hyperlink_italic_turned

    def setHyperlinkItalicTurned(self, is_turned: bool) -> None:
        self.__is_hyperlink_italic_turned = is_turned

    def isHyperlinkItalic(self) -> bool:
        return self.__is_hyperlink_italic

    def setHyperlinkItalic(self, is_italic: bool) -> None:
        self.__is_hyperlink_italic = is_italic

    def isHyperlinkUnderlinedTurned(self) -> bool:
        return self.__is_hyperlink_underlined_turned

    def setHyperlinkUnderlinedTurned(self, is_turned: bool) -> None:
        self.__is_hyperlink_underlined_turned = is_turned

    def isHyperlinkUnderlined(self) -> bool:
        return self.__is_hyperlink_underlined

    def setHyperlinkUnderlined(self, is_underlined: bool) -> None:
        self.__is_hyperlink_underlined = is_underlined

    def isHyperlinkBackgroundColorTurned(self) -> bool:
        return self.__is_hyperlink_background_color_turned

    def setHyperlinkBackgroundColorTurned(self, is_turned: bool) -> None:
        self.__is_hyperlink_background_color_turned = is_turned

    def hyperlinkBackgroundColor(self) -> QColor:
        return self.__hyperlink_background_color

    def setHyperlinkBackgroundColor(self, color: QColor) -> None:
        self.__hyperlink_background_color = color

    def isHyperlinkForegroundColorTurned(self) -> bool:
        return self.__is_hyperlink_foreground_color_turned

    def setHyperlinkForegroundColorTurned(self, is_turned: bool) -> None:
        self.__is_hyperlink_foreground_color_turned = is_turned

    def hyperlinkForegroundColor(self) -> QColor:
        return self.__hyperlink_foreground_color

    def setHyperlinkForegroundColor(self, color: QColor) -> None:
        self.__hyperlink_foreground_color = color

    def cursorSelectionForegroundColor(self) -> QColor:
        return self.__cursor_selection_foreground_color

    def setCursorSelectionForegroundColor(self, color: QColor) -> None:
        self.__cursor_selection_foreground_color = color

    def cursorSelectionBackgroundColor(self) -> QColor:
        return self.__cursor_selection_background_color

    def setCursorSelectionBackgroundColor(self, color: QColor) -> None:
        self.__cursor_selection_background_color = color

    def pointTest(self, point: QPointF) -> HitResult:
        result: HitResult = HitResult()
        result.point = point

        current_cursor_position = 0

        # check in text
        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_rect: QRectF = block_layout.boundingRect()

            if block_rect.contains(point):
                helper: QTextCursor = QTextCursor(block)

                if helper.charFormat().isImageFormat():
                    # handle below
                    break

                for j in range(block_layout.lineCount()):
                    line: QTextLine = block_layout.lineAt(j)
                    line_rect: QRectF = line.rect()

                    if line_rect.contains(point):
                        x_position = point.x()
                        line_cursor_position = line.xToCursor(x_position, QTextLine.CursorPosition.CursorBetweenCharacters)  # type: ignore
                        current_cursor_position += line_cursor_position

                        helper.setPosition(current_cursor_position)
                        result.hyperlink = helper.charFormat().anchorHref()

                        if result.hyperlink != "":
                            result.hit = Hit.Hyperlink
                        else:
                            result.hit = Hit.Text

                        result.position = current_cursor_position

                        return result

            current_cursor_position += block.length()

        # check in images
        for image_format in self.__image_layout:
            if image_format.rect.contains(point):
                result.hit = Hit.Image

                mid_x = image_format.rect.x() + image_format.rect.width() / 2
                result.position = image_format.position + (1 if point.x() > mid_x else 0)

                return result

        result.hit = Hit.NoHit
        result.position = -1

        return result

    def positionTest(self, position: int) -> QPointF:
        current_cursor_position = 0

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()

            if block.contains(position):
                for j in range(block_layout.lineCount()):
                    line: QTextLine = block_layout.lineAt(j)

                    if current_cursor_position + line.textLength() >= position:
                        a, _ = line.cursorToX(position, QTextLine.Edge.Leading)  # type: ignore

                        return QPointF(a, line.y())

                    current_cursor_position += line.textLength()

            current_cursor_position += block.length()

        return QPointF(-1, -1)

    def documentChanged(self, from_: int, charsRemoved: int, charsAdded: int) -> None:
        # it isn't as complicated as you may think

        self.__image_layout.clear()

        character_count: int = 0
        page_count: int = 1

        root_x: float = self.__page_layout.textXPosition(0)
        root_y: float = self.__page_layout.textYPosition(0)

        remaining_text_height: float = self.__page_layout.textHeight()

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_format: QTextBlockFormat = block.blockFormat()

            block_x: float = block_format.indent() * self.__indent_step + block_format.leftMargin()
            block_y: float = 0

            block_width_reduce: float = (
                block_format.indent() * self.__indent_step + block_format.leftMargin() + block_format.rightMargin()
            )

            # block parsing structure:
            #
            # if image
            #   calc
            #   calc if new page
            #   continue
            #
            # while line:
            #   if first line:
            #       calc
            #       calc if new page
            #   else:
            #       calc
            #       calc new page
            #   calc
            # calc
            # calc if new page:

            # fixup in input component guarantees that if image exists then image has its own block
            # we don't support inline images

            is_image: bool = False
            image_width: float = 0.0
            image_height: float = 0.0
            image_name: str = ""
            image_position: int = 0

            it: QTextBlock.iterator = block.begin()
            if it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.charFormat().isImageFormat():
                    fragment_format: QTextImageFormat = fragment.charFormat().toImageFormat()
                    is_image = True
                    image_width = fragment_format.width()
                    image_height = fragment_format.height()
                    image_name = fragment_format.name()
                    image_position = fragment.position()

                    it += 1

                    if it != block.end():
                        # fixup hasn't complited yet
                        return

            if is_image:
                if (remaining_text_height != self.__page_layout.textHeight()) and (
                    remaining_text_height - block_format.topMargin() - image_height - block_format.bottomMargin() < 0
                ):
                    root_x = self.__page_layout.textXPosition(page_count)
                    root_y = self.__page_layout.textYPosition(page_count)

                    remaining_text_height = self.__page_layout.textHeight()
                    page_count += 1

                block_y += block_format.topMargin()

                image_x: float = root_x + block_x
                image_y: float = root_y + block_y

                match block_format.alignment():
                    case Qt.AlignmentFlag.AlignLeft:
                        image_x += 0

                    case Qt.AlignmentFlag.AlignHCenter:
                        image_x += (self.__page_layout.textWidth() - block_width_reduce - image_width) / 2

                    case Qt.AlignmentFlag.AlignRight:
                        image_x += self.__page_layout.textWidth() - block_width_reduce - image_width

                image_format: ImageFormat = ImageFormat()
                image_format.rect = QRectF(image_x, image_y, image_width, image_height)
                image_format.name = image_name
                image_format.position = image_position

                self.__image_layout.append(image_format)

                block_layout.beginLayout()
                line: QTextLine = block_layout.createLine()
                line.setLineWidth(image_width)
                line.setPosition(QPointF(image_x, image_y))
                block_layout.endLayout()

                root_y += block_format.topMargin() + image_height + block_format.bottomMargin()
                remaining_text_height -= block_format.topMargin() + image_height + block_format.bottomMargin()

                # there is no more text or images in this block
                continue

            block_layout.beginLayout()
            line: QTextLine = block_layout.createLine()
            is_first_line = True

            while line.isValid():
                line_x: float = 0.0
                line_y: float = 0.0

                if is_first_line:
                    line.setLineWidth(self.__page_layout.textWidth() - block_width_reduce - block_format.textIndent())

                    if (remaining_text_height != self.__page_layout.textHeight()) and (
                        remaining_text_height - line.height() - block_format.topMargin() <= 0
                    ):
                        root_x = self.__page_layout.textXPosition(page_count)
                        root_y = self.__page_layout.textYPosition(page_count)

                        remaining_text_height = self.__page_layout.textHeight()
                        page_count += 1

                    block_y += block_format.topMargin()
                    line_x += block_format.textIndent()
                    remaining_text_height -= block_format.topMargin()

                    is_first_line = False

                else:
                    line.setLineWidth(self.__page_layout.textWidth() - block_width_reduce)

                    if (remaining_text_height != self.__page_layout.textHeight()) and (
                        remaining_text_height - line.height() <= 0
                    ):
                        block_y += (
                            remaining_text_height
                            + self.__page_layout.footerHeight()
                            + self.__page_layout.pageBottomPadding()
                            + self.__page_layout.borderWidth()
                            + self.__page_layout.pageBottomMargin()
                            + self.__page_layout.pageSpacing()
                            + self.__page_layout.pageTopMargin()
                            + self.__page_layout.borderWidth()
                            + self.__page_layout.pageTopPadding()
                            + self.__page_layout.headerHeight()
                        )

                        remaining_text_height = self.__page_layout.textHeight()
                        page_count += 1

                line_x += root_x + block_x
                line_y += root_y + block_y

                line_rect: QRectF = line.naturalTextRect()

                match block_format.alignment():
                    case Qt.AlignmentFlag.AlignLeft:
                        line_x += 0

                    case Qt.AlignmentFlag.AlignHCenter:
                        line_x += (self.__page_layout.textWidth() - block_width_reduce - line_rect.width()) / 2

                    case Qt.AlignmentFlag.AlignRight:
                        line_x += self.__page_layout.textWidth() - block_width_reduce - line_rect.width()

                line.setLineWidth(max(line_rect.width(), line_rect.height() / 2))
                line.setPosition(QPointF(line_x, line_y))

                block_y += line.height() * block_format.lineHeight()
                remaining_text_height -= line.height() * block_format.lineHeight()

                character_count += line.textLength()

                line = block_layout.createLine()

            root_y += block_y

            if (remaining_text_height != self.__page_layout.textHeight()) and (
                remaining_text_height - block_format.bottomMargin() <= 0
            ):
                root_x = self.__page_layout.textXPosition(page_count)
                root_y = self.__page_layout.textYPosition(page_count)

                remaining_text_height = self.__page_layout.textHeight()
                page_count += 1

            else:
                root_y += block_format.bottomMargin()
                remaining_text_height -= block_format.bottomMargin()

            block_layout.endLayout()

        difference = page_count - self.__page_layout.pageCount()
        if difference > 0:
            self.__page_layout.addPage(difference)
        elif difference < 0:
            self.__page_layout.removePage(-difference)

        if self.__character_count != character_count:
            self.__character_count = character_count
            self.characterCountChanged.emit(self.__character_count)

        self.update.emit()

    def blockBoundingRect(self, block: QTextBlock) -> QRectF:
        return block.layout().boundingRect()

    def paint(self, context: DocumentPaintContext):
        self.paintPage(context)
        self.paintText(context)
        self.paintImage(context)

        self.update.emit()

    def paintPage(self, context: DocumentPaintContext) -> None:
        painter: QPainter = context.painter
        rect: QRectF = context.rect

        old_pen: QPen = painter.pen()
        pen: QPen = QPen()
        pen.setColor(self.__page_layout.borderColor())
        pen.setWidth(int(self.__page_layout.borderWidth()))
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        for i in range(self.__page_layout.pageCount()):
            page_rect: QRectF = QRectF(
                self.__page_layout.pageXPosition(i),
                self.__page_layout.pageYPosition(i),
                self.__page_layout.pageWidth(),
                self.__page_layout.pageHeight(),
            )
            clip = page_rect.intersected(rect)
            painter.fillRect(clip, self.__page_layout.pageColor())

            if self.__page_layout.borderWidth() > 0:
                border_rect: QRectF = QRectF(
                    self.__page_layout.pageXPosition(i)
                    + self.__page_layout.pageLeftMargin()
                    + self.__page_layout.borderWidth() / 2,
                    self.__page_layout.pageYPosition(i)
                    + self.__page_layout.pageTopMargin()
                    + self.__page_layout.borderWidth() / 2,
                    self.__page_layout.pageWidth()
                    - self.__page_layout.pageLeftMargin()
                    - self.__page_layout.pageRightMargin()
                    - self.__page_layout.borderWidth(),
                    self.__page_layout.pageHeight()
                    - self.__page_layout.pageTopMargin()
                    - self.__page_layout.pageBottomMargin()
                    - self.__page_layout.borderWidth(),
                )
                painter.drawRect(border_rect)

        painter.setPen(old_pen)

    def paintText(self, context: DocumentPaintContext):
        painter: QPainter = context.painter
        rect: QRectF = context.rect
        cursor: QTextCursor = context.cursor

        cursor_position: int = cursor.position()

        cursor_selection: Selection = Selection()
        cursor_selection.start = cursor.selectionStart()
        cursor_selection.end = cursor.selectionEnd()
        cursor_selection.format = QTextCharFormat()
        cursor_selection.format.setForeground(self.__cursor_selection_foreground_color)
        cursor_selection.format.setBackground(self.__cursor_selection_background_color)

        for i in range(self.document().blockCount()):
            block: QTextBlock = self.document().findBlockByNumber(i)
            block_layout: QTextLayout = block.layout()
            block_position: int = block.position()
            block_length: int = block.length()

            # skip, we have paintImage method
            it: QTextBlock.iterator = block.begin()
            if it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.charFormat().isImageFormat():
                    continue

            format_ranges: list[QTextLayout.FormatRange] = []

            # show selections and hyperlinks
            selections: list[Selection] = []

            it: QTextBlock.iterator = block.begin()
            while it != block.end():
                fragment: QTextFragment = it.fragment()

                if fragment.charFormat().anchorHref() != "":
                    selection = Selection()
                    selection.format = fragment.charFormat()

                    if self.__is_hyperlink_bold_turned:
                        font_weight = QFont.Weight.Bold if self.__is_hyperlink_bold else QFont.Weight.Normal
                        selection.format.setFontWeight(font_weight)

                    if self.__is_hyperlink_italic_turned:
                        selection.format.setFontItalic(self.__is_hyperlink_italic)

                    if self.__is_hyperlink_underlined_turned:
                        selection.format.setUnderlineStyle(
                            QTextCharFormat.UnderlineStyle.SingleUnderline
                            if self.__is_hyperlink_underlined
                            else QTextCharFormat.UnderlineStyle.NoUnderline
                        )

                    if self.__is_hyperlink_background_color_turned:
                        selection.format.setBackground(self.__hyperlink_background_color)

                    if self.__is_hyperlink_foreground_color_turned:
                        selection.format.setForeground(self.__hyperlink_foreground_color)

                    selection.start = fragment.position()
                    selection.end = fragment.position() + fragment.length()
                    selections.append(selection)

                it += 1

            # make sure that cursor selection at the top
            selections.append(cursor_selection)

            for selection in selections:
                selection_start: int = selection.start - block_position
                selection_end: int = selection.end - block_position

                if selection_start < block_length and selection_end > 0 and selection_start < selection_end:
                    format_range: QTextLayout.FormatRange = QTextLayout.FormatRange()
                    format_range.start = selection_start  # type: ignore
                    format_range.length = selection_end - selection_start  # type: ignore
                    format_range.format = selection.format  # type: ignore
                    format_ranges.append(format_range)

            block_layout.draw(painter, QPointF(0, 0), format_ranges, rect)

            if cursor_position >= block_position and cursor_position < block_position + block_length:
                block_layout.drawCursor(painter, QPointF(0, 0), cursor_position - block_position)

    def paintImage(self, context: DocumentPaintContext):
        painter: QPainter = context.painter
        cursor: QTextCursor = context.cursor

        old_pen: QPen = painter.pen()
        old_composition_mode: QPainter.CompositionMode = painter.compositionMode()

        pen: QPen = QPen(QColor("white"))
        pen_width = 5
        pen.setWidth(pen_width)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        for image_format in self.__image_layout:
            image: QImage = self.document().resource(QTextDocument.ResourceType.ImageResource, image_format.name)
            painter.drawImage(image_format.rect, image)

            # draw cursor

            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()

            # ------|------case3------|------
            # ----------|--image--|----------
            # --|-case1-|---------|-case2-|--

            # case 1
            if selection_end == image_format.position:
                painter.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
                painter.drawLine(
                    int(image_format.rect.x() + (pen_width + 1) / 2),
                    int(image_format.rect.y() + (pen_width + 1) / 2),
                    int(image_format.rect.x() + (pen_width + 1) / 2),
                    int(image_format.rect.y() + (pen_width + 1) / 2) + int(image_format.rect.height() - pen_width),
                )
                painter.setCompositionMode(old_composition_mode)

            # case 2
            elif selection_start == image_format.position + 1:
                painter.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
                painter.drawLine(
                    int(image_format.rect.x() + (pen_width + 1) / 2) + int(image_format.rect.width() - pen_width),
                    int(image_format.rect.y() + (pen_width + 1) / 2),
                    int(image_format.rect.x() + (pen_width + 1) / 2) + int(image_format.rect.width() - pen_width),
                    int(image_format.rect.y() + (pen_width + 1) / 2) + int(image_format.rect.height() - pen_width),
                )
                painter.setCompositionMode(old_composition_mode)

            # case 3
            elif selection_start <= image_format.position and selection_end >= image_format.position + 1:
                painter.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
                painter.drawRect(
                    int(image_format.rect.x() + (pen_width + 1) / 2),
                    int(image_format.rect.y() + (pen_width + 1) / 2),
                    int(image_format.rect.width() - pen_width),
                    int(image_format.rect.height() - pen_width),
                )
                painter.setCompositionMode(old_composition_mode)

        painter.setPen(old_pen)
        painter.setCompositionMode(old_composition_mode)

    @Slot()
    def onPageLayoutInternalChanged(self) -> None:
        self.documentChanged(0, 0, 0)

    @Slot()
    def onPageLayoutExternalChanged(self) -> None:
        self.documentChanged(0, 0, 0)
