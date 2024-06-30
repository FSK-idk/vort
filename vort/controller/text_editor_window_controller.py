from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QObject

from view.window.text_editor_window_view import TextEditorWindowView


class TextEditorWindowController(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: TextEditorWindowView = TextEditorWindowView()

        self.setupAction()

        # signal

        self.ui.font_combobox.currentFontChanged.connect(self.selectFont)
        self.ui.font_combobox.lineEdit().returnPressed.connect(self.ui.editor.ui.setFocus)
        self.ui.font_combobox.activated.connect(self.ui.editor.ui.setFocus)
        self.ui.editor.fontChanged.connect(self.onFontChanged)

        self.ui.size_combobox.activated.connect(self.selectSize)
        self.ui.size_combobox.lineEdit().returnPressed.connect(self.ui.editor.ui.setFocus)
        self.ui.size_combobox.activated.connect(self.ui.editor.ui.setFocus)
        self.ui.editor.sizeChanged.connect(self.onSizeChanged)

        self.ui.editor.boldTurned.connect(self.onBoldTurned)
        self.ui.editor.italicTurned.connect(self.onItalicTurned)
        self.ui.editor.underlinedTurned.connect(self.onUnderlinedTurned)

        self.ui.color_picker.colorSelected.connect(self.selectColor)
        self.ui.color_picker.colorSelected.connect(self.ui.editor.ui.setFocus)
        self.ui.editor.colorSelected.connect(self.onColorSelected)

        self.ui.background_color_picker.colorSelected.connect(self.selectBackgroundColor)
        self.ui.background_color_picker.colorSelected.connect(self.ui.editor.ui.setFocus)
        self.ui.editor.backgroundColorSelected.connect(self.onBackgroundColorSelected)

        self.ui.editor.firstLineIndentTurned.connect(self.onFirstLineIndentTurned)

        self.ui.editor.characterCountChanged.connect(self.onCharacterCountChanged)

        self.setupDefault()

        self.ui.show()

    def setupAction(self) -> None:
        # file
        self.ui.new_document_action.triggered.connect(self.newDocument)
        self.ui.open_document_action.triggered.connect(self.openDocument)
        self.ui.close_document_action.triggered.connect(self.closeDocument)
        self.ui.save_document_action.triggered.connect(self.saveDocument)
        self.ui.exit_editor_action.triggered.connect(self.ui.close)

        # edit
        self.ui.undo_action.triggered.connect(self.ui.editor.undo)
        self.ui.redo_action.triggered.connect(self.ui.editor.redo)

        self.ui.cut_action.triggered.connect(self.ui.editor.cut)
        self.ui.copy_action.triggered.connect(self.ui.editor.copy)
        self.ui.paste_action.triggered.connect(self.ui.editor.paste)
        self.ui.paste_plain_action.triggered.connect(self.ui.editor.pastePlain)

        self.ui.select_all_action.triggered.connect(self.ui.editor.selectAll)

        self.ui.find_action.triggered.connect(self.find)
        self.ui.find_and_replace_action.triggered.connect(self.findAndReplace)

        # insert
        self.ui.insert_image_action.triggered.connect(self.insertImage)
        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # format
        self.ui.turn_bold_action.triggered.connect(self.turnBold)
        self.ui.turn_italic_action.triggered.connect(self.turnItalic)
        self.ui.turn_underlined_action.triggered.connect(self.turnUnderlined)

        self.ui.indent_paragraph_right_action.triggered.connect(self.indentParagraphRight)
        self.ui.indent_paragraph_left_action.triggered.connect(self.indentParagraphLeft)
        self.ui.turn_first_line_indent_action.triggered.connect(self.turnFirstLineIndent)

        self.ui.select_line_spacing_action.triggered.connect(self.selectLineSpacing)
        self.ui.select_paragraph_spacing_action.triggered.connect(self.selectParagraphSpacing)

        self.ui.turn_pagination_action.triggered.connect(self.turnPagination)

        # style
        self.ui.open_style_action.triggered.connect(self.openStyle)
        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # help
        self.ui.show_guide_action.triggered.connect(self.showGuide)
        self.ui.show_about_action.triggered.connect(self.showAbout)

        self.ui.test_action.triggered.connect(self.test)

    def setupDefault(self) -> None:
        self.turnBold(False)
        self.onBoldTurned(False)
        self.turnItalic(False)
        self.onItalicTurned(False)
        self.turnUnderlined(False)
        self.onUnderlinedTurned(False)
        self.selectFont(QFont())
        self.onFontChanged(QFont().family())
        self.ui.size_combobox.setEditText("16 pt")
        self.selectSize()
        self.onSizeChanged(16)
        self.ui.character_count.setText("0 characters")
        self.selectColor(QColor(Qt.GlobalColor.black))
        self.onColorSelected(QColor(Qt.GlobalColor.black))
        self.selectBackgroundColor(QColor(Qt.GlobalColor.white))
        self.onBackgroundColorSelected(QColor(Qt.GlobalColor.white))

    def onCharacterCountChanged(self, character_count) -> None:
        if character_count == 1:
            self.ui.character_count.setText("1 character")
        else:
            self.ui.character_count.setText(f"{character_count} characters")

    def newDocument(self) -> None:
        print("newDocument")

    def openDocument(self) -> None:
        print("openDocument")

    def closeDocument(self) -> None:
        print("closeDocument")

    def saveDocument(self) -> None:
        print("saveDocument")

    def find(self) -> None:
        print("find")

    def findAndReplace(self) -> None:
        print("findAndReplace")

    def turnBold(self, is_bold) -> None:
        self.ui.editor.turnBold(is_bold)

    def onBoldTurned(self, is_bold) -> None:
        self.ui.turn_bold_action.setChecked(is_bold)

    def turnItalic(self, is_italic) -> None:
        self.ui.editor.turnItalic(is_italic)

    def onItalicTurned(self, is_italic) -> None:
        self.ui.turn_italic_action.setChecked(is_italic)

    def turnUnderlined(self, is_underlined) -> None:
        self.ui.editor.turnUnderlined(is_underlined)

    def onUnderlinedTurned(self, is_underlined) -> None:
        self.ui.turn_underlined_action.setChecked(is_underlined)

    def selectFont(self, font: QFont) -> None:
        self.ui.editor.setFont(font.family())

    def onFontChanged(self, font: str) -> None:
        self.ui.font_combobox.blockSignals(True)
        self.ui.font_combobox.setCurrentFont(font)
        self.ui.font_combobox.blockSignals(False)

    def selectSize(self) -> None:
        text = self.ui.size_combobox.currentText()
        self.ui.editor.setSize(int(text[:-3]))

    def onSizeChanged(self, size: int) -> None:
        self.ui.size_combobox.blockSignals(True)
        self.ui.size_combobox.setEditText(str(size) + " pt")
        self.ui.size_combobox.blockSignals(False)

    def selectColor(self, color: QColor) -> None:
        self.ui.editor.selectColor(color)

    def onColorSelected(self, color: QColor) -> None:
        self.ui.color_picker.setColor(color)

    def selectBackgroundColor(self, color: QColor) -> None:
        self.ui.editor.selectBackgroundColor(color)

    def onBackgroundColorSelected(self, color: QColor) -> None:
        self.ui.background_color_picker.setColor(color)

    def insertImage(self) -> None:
        print("insertImage")

    def insertHyperlink(self) -> None:
        print("insertHyperlink")

    def indentParagraphRight(self) -> None:
        self.ui.editor.indentParagraphRight()

    def indentParagraphLeft(self) -> None:
        self.ui.editor.indentParagraphLeft()

    def turnFirstLineIndent(self, is_indent) -> None:
        self.ui.editor.turnFirstLineIndent(is_indent)

    def onFirstLineIndentTurned(self, is_indent) -> None:
        self.ui.turn_first_line_indent_action.setChecked(is_indent)

    def selectLineSpacing(self) -> None:
        print("selectLineSpacing")

    def selectParagraphSpacing(self) -> None:
        print("selectParagraphSpacing")

    def turnPagination(self) -> None:
        print("turnPagination")

    def openStyle(self) -> None:
        print("openStyle")

    def clearStyle(self) -> None:
        print("clearStyle")

    def showGuide(self) -> None:
        print("showGuide")

    def showAbout(self) -> None:
        print("showAbout")

    # TODO: DEBUG
    def test(self) -> None:
        self.ui.editor.test()
        pass
