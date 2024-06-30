from PySide6.QtCore import Qt, Signal, QMimeData, QObject
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
)
from PySide6.QtGui import (
    QKeyEvent,
    QMouseEvent,
    QTextDocument,
    QTextCursor,
    QFont,
    QResizeEvent,
    QKeyEvent,
    QTextCharFormat,
    QPaintEvent,
    QTextBlockFormat,
    QClipboard,
    QTextDocumentFragment,
    QColor,
)

from util import PointF, RectF

from core.widget.text_editor.text_editor_ui import TextEditorUI


class TextEditor(QObject):
    # font
    fontFamilySelected = Signal(str)
    fontSizeSelected = Signal(int)

    # format
    boldTurned = Signal(bool)
    italicTurned = Signal(bool)
    underlinedTurned = Signal(bool)

    # color
    foregroundColorSelected = Signal(QColor)
    backgroundColorSelected = Signal(QColor)

    # indent
    firstLineIndentTurned = Signal(bool)

    # page
    pageCountChanged = Signal(int)

    # status
    characterCountChanged = Signal(int)

    # internal
    cursorPositionChanged = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui: TextEditorUI = TextEditorUI(parent)

        self.__paragraph_indent = 48
        self.__first_line_indent = 48

        self.document: QTextDocument = QTextDocument()
        self.ui.setDocument(self.document)

        self.text_cursor: QTextCursor = QTextCursor(self.document)
        self.text_cursor.setBlockFormat(QTextBlockFormat())

        # signal

        self.cursorPositionChanged.connect(self.onCursorPositionChanged)
        self.ui.mousePressed.connect(self.onMousePressed)
        self.ui.mouseMoved.connect(self.onMouseMoved)
        self.ui.keyPressed.connect(self.onKeyPressed)
        self.ui.resized.connect(self.onResized)
        self.ui.paintedDocument.connect(self.onPaintedDocument)

        self.ui.pageCountChanged.connect(self.pageCountChanged.emit)
        self.ui.characterCountChanged.connect(self.characterCountChanged.emit)

    # TODO: DEBUG
    def test(self) -> None:
        print("test")
        # char_format: QTextCharFormat = QTextCharFormat()
        # block_format: QTextBlockFormat = QTextBlockFormat()
        # block_format.setIndent(48)
        # block_format.setTextIndent(48)
        # block_format: QTextBlockFormat = self.text_cursor.blockFormat()
        # print("indent", block_format.indent())
        # print("text indent", block_format.textIndent())
        # print("line height", block_format.lineHeight())
        # self.text_cursor.setBlockFormat(block_format)
        self.ui.viewport().repaint()
        pass

    # font

    def selectFontFamily(self, font_family: str) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontFamily(font_family)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def selectFontSize(self, font_size: int) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontPointSize(font_size)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    # format

    def turnBold(self, is_bold: bool) -> None:
        bold = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
        format: QTextCharFormat = QTextCharFormat()
        format.setFontWeight(bold)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def turnItalic(self, is_italic: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontItalic(is_italic)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def turnUnderlined(self, is_underline: bool) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setFontUnderline(is_underline)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    # color

    def selectForegroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setForeground(color)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    def selectBackgroundColor(self, color: QColor) -> None:
        format: QTextCharFormat = QTextCharFormat()
        format.setBackground(color)
        self.text_cursor.mergeCharFormat(format)
        self.text_cursor.mergeBlockCharFormat(self.text_cursor.charFormat())
        self.ui.viewport().repaint()

    # indent

    def turnFirstLineIndent(self, is_indent) -> None:
        new_indent = self.__first_line_indent if is_indent else 0
        format: QTextBlockFormat = QTextBlockFormat()
        format.setTextIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.ui.viewport().repaint()

    def indentParagraphRight(self) -> None:
        new_indent: int = self.text_cursor.blockFormat().indent() + self.__paragraph_indent
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.ui.viewport().repaint()

    def indentParagraphLeft(self) -> None:
        new_indent: int = self.text_cursor.blockFormat().indent() - self.__paragraph_indent
        if new_indent < 0:
            return
        format: QTextBlockFormat = QTextBlockFormat()
        format.setIndent(new_indent)
        self.text_cursor.mergeBlockFormat(format)
        self.ui.viewport().repaint()

    def onCursorPositionChanged(self, position: int) -> None:
        char_format: QTextCharFormat = self.text_cursor.charFormat()
        block_format: QTextBlockFormat = self.text_cursor.blockFormat()

        # font

        font_family: str = char_format.font().family()
        self.fontFamilySelected.emit(font_family)

        font_size: int = char_format.font().pointSize()
        self.fontSizeSelected.emit(font_size)

        # format

        is_bold = char_format.fontWeight() == QFont.Weight.Bold
        self.boldTurned.emit(is_bold)

        is_italic = char_format.fontItalic()
        self.italicTurned.emit(is_italic)

        is_underlined = char_format.fontUnderline()
        self.underlinedTurned.emit(is_underlined)

        # color

        foreground_color = char_format.foreground().color()
        self.foregroundColorSelected.emit(foreground_color)

        background_color = char_format.background().color()
        self.backgroundColorSelected.emit(background_color)

        # indent

        self.firstLineIndentTurned.emit(block_format.textIndent() != 0)

    def undo(self) -> None:
        self.document.undo(self.text_cursor)
        self.ui.viewport().repaint()

    def redo(self) -> None:
        self.document.redo(self.text_cursor)
        self.ui.viewport().repaint()

    def cut(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.text_cursor.removeSelectedText()
            self.ui.viewport().repaint()

    def copy(self) -> None:
        if self.text_cursor.hasSelection():
            mime_data: QMimeData = QMimeData()
            selection = self.text_cursor.selection()
            mime_data.setText(selection.toPlainText())
            mime_data.setHtml(selection.toHtml())
            QApplication.clipboard().setMimeData(mime_data)
            self.ui.viewport().repaint()

    def paste(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        if mime_data.hasHtml():
            self.text_cursor.insertFragment(QTextDocumentFragment.fromHtml(mime_data.html()))
        else:
            self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.ui.viewport().repaint()

    def pastePlain(self) -> None:
        mime_data = QApplication.clipboard().mimeData()
        self.text_cursor.insertFragment(QTextDocumentFragment.fromPlainText(mime_data.text()))
        self.ui.viewport().repaint()

    def selectAll(self) -> None:
        self.text_cursor.select(QTextCursor.SelectionType.Document)
        self.ui.viewport().repaint()

    def onMousePressed(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.ui.horizontalScrollBar().value()
            screen_y = self.ui.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.ui.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.MoveAnchor)
                self.cursorPositionChanged.emit(self.text_cursor.position())
                self.ui.viewport().repaint()

            self.mouse_pressed = True

    def onMouseMoved(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            point_position = PointF.fromQPointF(event.position())

            screen_x = self.ui.horizontalScrollBar().value()
            screen_y = self.ui.verticalScrollBar().value()

            point_position.move(PointF(screen_x, screen_y))

            position = self.ui.hitTest(point_position)

            if position != -1:
                self.text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
                self.cursorPositionChanged.emit(self.text_cursor.position())
                self.ui.viewport().repaint()

    def onKeyPressed(self, event: QKeyEvent) -> None:
        self.handleNavigationInput(event)
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
            self.ui.viewport().repaint()

    def handleTextInput(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.text():
            match event.key():
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor)  # type: ignore
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete if not self.text_cursor.hasSelection():
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor)
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case _:
                    return
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

        if event.modifiers() in [Qt.KeyboardModifier.NoModifier, Qt.KeyboardModifier.ShiftModifier] and event.text():
            match event.key():
                case Qt.Key.Key_Enter:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertBlock()
                    self.text_cursor.setPosition(self.text_cursor.block().position())
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Backspace:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deletePreviousChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Delete:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.deleteChar()
                    self.text_cursor.endEditBlock()
                case Qt.Key.Key_Escape:
                    return  # ignore
                case _:
                    self.text_cursor.beginEditBlock()
                    self.text_cursor.insertText(event.text())
                    self.text_cursor.endEditBlock()
            self.cursorPositionChanged.emit(self.text_cursor.position())
            self.ui.viewport().repaint()

    def onResized(self, event: QResizeEvent) -> None:
        self.ui.resize(PointF(event.size().width(), event.size().height()))

    def onPaintedDocument(self, event: QPaintEvent) -> None:
        rect = RectF.fromQRect(event.rect())
        self.ui.paint_document(rect, self.text_cursor)
