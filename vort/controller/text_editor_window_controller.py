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
        # file
        self.ui.new_document_action.triggered.connect(self.newDocument)
        self.ui.open_document_action.triggered.connect(self.openDocument)
        self.ui.close_document_action.triggered.connect(self.closeDocument)
        self.ui.exit_editor_action.triggered.connect(self.exitEditor)

        # edit
        self.ui.undo_action.triggered.connect(self.undo)
        self.ui.redo_action.triggered.connect(self.redo)

        self.ui.cut_action.triggered.connect(self.cut)
        self.ui.copy_action.triggered.connect(self.copy)
        self.ui.paste_action.triggered.connect(self.paste)

        self.ui.select_all_action.triggered.connect(self.selectAll)

        self.ui.find_action.triggered.connect(self.find)
        self.ui.find_and_replace_action.triggered.connect(self.findAndReplace)

        # insert
        self.ui.insert_image_action.triggered.connect(self.insertImage)
        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # format
        self.ui.turn_bold_action.triggered.connect(self.turnBold)
        self.ui.turn_italic_action.triggered.connect(self.turnItalic)
        self.ui.turn_underline_action.triggered.connect(self.turnUnderline)

        self.ui.indent_right_action.triggered.connect(self.indentRight)
        self.ui.indent_left_action.triggered.connect(self.indentLeft)

        self.ui.choose_line_spacing_action.triggered.connect(self.chooseLineSpacing)
        self.ui.choose_paragraph_spacing_action.triggered.connect(self.chooseParagraphSpacing)

        self.ui.turn_pagination_action.triggered.connect(self.turnPagination)

        # style
        self.ui.open_style_action.triggered.connect(self.openStyle)
        self.ui.clear_style_action.triggered.connect(self.clearStyle)

        # help
        self.ui.show_guide_action.triggered.connect(self.showGuide)
        self.ui.show_about_action.triggered.connect(self.showAbout)

        self.ui.test_action.triggered.connect(self.test)

    def newDocument(self) -> None:
        print("newDocument")

    def openDocument(self) -> None:
        print("openDocument")

    def closeDocument(self) -> None:
        print("closeDocument")

    def exitEditor(self) -> None:
        print("exitEditor")

    def undo(self) -> None:
        print("undo")

    def redo(self) -> None:
        print("redo")

    def cut(self) -> None:
        print("cut")

    def copy(self) -> None:
        print("copy")

    def paste(self) -> None:
        print("paste")

    def selectAll(self) -> None:
        print("selectAll")

    def find(self) -> None:
        print("find")

    def findAndReplace(self) -> None:
        print("findAndReplace")

    def insertImage(self) -> None:
        print("insertImage")

    def insertHyperlink(self) -> None:
        print("insertHyperlink")

    def turnBold(self, checked) -> None:
        print("turnBold", checked)
        self.ui.editor.setBold(checked)

    def onFontWeightChanged(self, weight: QFont.Weight) -> None:
        self.ui.turn_bold_action.setChecked(weight == QFont.Weight.Bold)

    def turnItalic(self) -> None:
        print("turnItalic")

    def turnUnderline(self) -> None:
        print("turnUnderline")

    def indentRight(self) -> None:
        print("indentRight")

    def indentLeft(self) -> None:
        print("indentLeft")

    def chooseLineSpacing(self) -> None:
        print("chooseLineSpacing")

    def chooseParagraphSpacing(self) -> None:
        print("chooseParagraphSpacing")

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
