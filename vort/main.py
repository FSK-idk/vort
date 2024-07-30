import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap, QPalette, QColor

from core.window.editor.document_editor_window import DocumentEditorWindow

from core.util import resource_path


import resource_rc


def main() -> None:
    app = QApplication()
    app.setWindowIcon(QPixmap(":/icon/vort.png"))
    app.setStyle("Fusion")

    if not os.path.isdir(resource_path("./vort/")):
        os.mkdir(resource_path("./vort/"))

    darkPalette: QPalette = QPalette()
    darkPalette.setColor(QPalette.ColorRole.Window, QColor(53,53,53))
    darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Base, QColor(25,25,25))
    darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(53,53,53))
    darkPalette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Button, QColor(53,53,53))
    darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    darkPalette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(darkPalette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    text_editor_window: DocumentEditorWindow = DocumentEditorWindow()
    app.exec()


if __name__ == "__main__":
    main()
