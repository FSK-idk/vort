from PySide6.QtGui import QFont

from view.window.text_editor_window_view import TextEditorWindowView

from controller.controller import Controller


class TextEditorWindowController(Controller):
    def __init__(self) -> None:
        super().__init__()

        self.ui: TextEditorWindowView = TextEditorWindowView(controller=self)

        self.setupAction()

        # signal

        self.ui.editor.fontWeightChanged.connect(self.onFontWeightChanged)

        self.ui.show()

    def setupAction(self) -> None:
        self.ui.new_file_action.triggered.connect(self.newFile)
        self.ui.open_file_action.triggered.connect(self.openFile)
        self.ui.close_file_action.triggered.connect(self.closeFile)
        self.ui.exit_editor_action.triggered.connect(self.exitEditor)

        # edit

        self.ui.undo_last_action.triggered.connect(self.undoLast)
        self.ui.redo_last_action.triggered.connect(self.redoLast)

        self.ui.cut_text_action.triggered.connect(self.cutText)
        self.ui.copy_text_action.triggered.connect(self.copyText)
        self.ui.paste_text_action.triggered.connect(self.pasteText)

        self.ui.select_text_action.triggered.connect(self.selectText)
        self.ui.find_text_action.triggered.connect(self.findText)
        self.ui.find_and_replace_text_action.triggered.connect(self.findAndReplaceText)

        # insert

        self.ui.insert_image_action.triggered.connect(self.insertImage)
        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # help

        self.ui.show_about_action.triggered.connect(self.showAbout)

        # style

        self.ui.choose_style_action.triggered.connect(self.chooseStyle)
        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # font

        self.ui.choose_font_action.triggered.connect(self.chooseFont)
        self.ui.choose_font_size_action.triggered.connect(self.chooseFontSize)

        # format

        self.ui.bold_text_action.triggered.connect(self.boldText)
        self.ui.italic_text_action.triggered.connect(self.italicText)
        self.ui.underline_text_action.triggered.connect(self.underlineText)

        # color

        self.ui.color_text_action.triggered.connect(self.colorText)
        self.ui.bg_color_text_action.triggered.connect(self.bgColorText)

        # indent

        self.ui.right_indent_action.triggered.connect(self.rightIndent)
        self.ui.left_indent_action.triggered.connect(self.leftIndent)
        self.ui.test_action.triggered.connect(self.test)

    def newFile(self) -> None:
        print("New File")

    def openFile(self) -> None:
        print("Open File")

    def closeFile(self) -> None:
        print("Close File")

    def exitEditor(self) -> None:
        print("Exit Editor")

    def undoLast(self) -> None:
        print("Undo Last")

    def redoLast(self) -> None:
        print("Redo Last")

    def cutText(self) -> None:
        print("Cut Text")

    def copyText(self) -> None:
        print("Copy Text")

    def pasteText(self) -> None:
        print("Paste Text")

    def selectText(self) -> None:
        print("Select Text")

    def findText(self) -> None:
        print("Find Text")

    def findAndReplaceText(self) -> None:
        print("Find and Replace Text")

    def insertImage(self) -> None:
        print("Insert Image")

    def insertHyperlink(self) -> None:
        print("Insert Hyperlink")

    def showAbout(self) -> None:
        print("Show About")

    def chooseStyle(self) -> None:
        print("Choose Style")

    def clearStyle(self) -> None:
        print("Clear Style")

    def chooseFont(self) -> None:
        print("Choose Font")

    def chooseFontSize(self) -> None:
        print("Choose Font Size")

    def boldText(self, checked) -> None:
        print("Bold Text", checked)
        self.ui.editor.setBold(checked)

    def onFontWeightChanged(self, weight: QFont.Weight) -> None:
        self.ui.bold_text_action.setChecked(weight == QFont.Weight.Bold)

    def italicText(self) -> None:
        print("Italic Text")

    def underlineText(self) -> None:
        print("Underline Text")

    def colorText(self) -> None:
        print("Color Text")

    def bgColorText(self) -> None:
        print("BG Color Text")

    def rightIndent(self) -> None:
        print("Right Indent")

    def leftIndent(self) -> None:
        print("Left Indent")

    # TODO: DEBUG
    def test(self) -> None:
        self.ui.editor.test()
