from PySide6.QtWidgets import QMainWindow, QPushButton, QMenuBar, QMenu, QToolBar
from PySide6.QtGui import QAction


class EditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Window

        self.setWindowTitle("vort")
        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(400, 300)

        # Action

        # File

        self.new_file_action: QAction = QAction("New")
        self.new_file_action.triggered.connect(self.newFile)
        self.open_file_action: QAction = QAction("Open")
        self.open_file_action.triggered.connect(self.openFile)
        self.close_file_action: QAction = QAction("Close")
        self.close_file_action.triggered.connect(self.closeFile)

        self.exit_editor_action: QAction = QAction("Exit")
        self.exit_editor_action.triggered.connect(self.exitEditor)

        # Edit

        self.undo_last_action: QAction = QAction("Undo")
        self.undo_last_action.triggered.connect(self.undoLast)
        self.redo_last_action: QAction = QAction("Redo")
        self.redo_last_action.triggered.connect(self.redoLast)

        self.cut_text_action: QAction = QAction("Cut")
        self.cut_text_action.triggered.connect(self.cutText)
        self.copy_text_action: QAction = QAction("Copy")
        self.copy_text_action.triggered.connect(self.copyText)
        self.paste_text_action: QAction = QAction("Paste")
        self.paste_text_action.triggered.connect(self.pasteText)

        self.select_text_action: QAction = QAction("Select")
        self.select_text_action.triggered.connect(self.selectText)
        self.find_text_action: QAction = QAction("Find")
        self.find_text_action.triggered.connect(self.findText)
        self.find_and_replace_text_action: QAction = QAction("Find and Replace")
        self.find_and_replace_text_action.triggered.connect(self.findAndReplaceText)

        # Insert

        self.insert_image_action: QAction = QAction("Image")
        self.insert_image_action.triggered.connect(self.insertImage)
        self.insert_hyperlink_action: QAction = QAction("Hylerlink")
        self.insert_hyperlink_action.triggered.connect(self.insertHyperlink)

        # Help

        self.show_about_action: QAction = QAction("About")
        self.show_about_action.triggered.connect(self.showAbout)

        # Menu bar

        file_menu: QMenu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_file_action)
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.close_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_editor_action)

        edit_menu: QMenu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.undo_last_action)
        edit_menu.addAction(self.redo_last_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_text_action)
        edit_menu.addAction(self.copy_text_action)
        edit_menu.addAction(self.paste_text_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_text_action)
        edit_menu.addAction(self.find_text_action)
        edit_menu.addAction(self.find_and_replace_text_action)

        insert_menu: QMenu = self.menuBar().addMenu("Insert")
        insert_menu.addAction(self.insert_image_action)
        insert_menu.addAction(self.insert_hyperlink_action)

        help_menu: QMenu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.show_about_action)

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
