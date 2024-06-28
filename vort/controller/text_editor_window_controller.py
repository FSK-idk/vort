from view.window.text_editor_window_view import TextEditorWindowView

from controller.controller import Controller


class TextEditorWindowController(Controller):
    def __init__(self) -> None:
        super().__init__()

        self.ui: TextEditorWindowView = TextEditorWindowView(controller=self)

        self.setupAction()

        # signal

        self.ui.editor.boldTurned.connect(self.ui.turn_bold_action.setChecked)
        self.ui.editor.italicTurned.connect(self.ui.turn_italic_action.setChecked)
        self.ui.editor.underlinedTurned.connect(self.ui.turn_underlined_action.setChecked)

        self.ui.editor.characterCountChanged.connect(self.onCharacterCountChanged)

        self.ui.show()

    def setupAction(self) -> None:
        # file
        self.ui.new_document_action.triggered.connect(self.newDocument)
        self.ui.open_document_action.triggered.connect(self.openDocument)
        self.ui.close_document_action.triggered.connect(self.closeDocument)
        self.ui.exit_editor_action.triggered.connect(self.ui.close)

        # edit
        self.ui.undo_action.triggered.connect(self.ui.editor.undo)
        self.ui.redo_action.triggered.connect(self.ui.editor.redo)

        self.ui.cut_action.triggered.connect(self.ui.editor.cut)
        self.ui.copy_action.triggered.connect(self.ui.editor.copy)
        self.ui.paste_action.triggered.connect(self.ui.editor.paste)

        self.ui.select_all_action.triggered.connect(self.ui.editor.selectAll)

        self.ui.find_action.triggered.connect(self.find)
        self.ui.find_and_replace_action.triggered.connect(self.findAndReplace)

        # insert
        self.ui.insert_image_action.triggered.connect(self.insertImage)
        self.ui.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # format
        self.ui.turn_bold_action.triggered.connect(self.ui.editor.turnBold)
        self.ui.turn_italic_action.triggered.connect(self.ui.editor.turnItalic)
        self.ui.turn_underlined_action.triggered.connect(self.ui.editor.turnUnderlined)

        self.ui.indent_right_action.triggered.connect(self.indentRight)
        self.ui.indent_left_action.triggered.connect(self.indentLeft)

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

    def find(self) -> None:
        print("find")

    def findAndReplace(self) -> None:
        print("findAndReplace")

    def insertImage(self) -> None:
        print("insertImage")

    def insertHyperlink(self) -> None:
        print("insertHyperlink")

    def indentRight(self) -> None:
        print("indentRight")

    def indentLeft(self) -> None:
        print("indentLeft")

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
        print("A")
