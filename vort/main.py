from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap

from core.window.editor.document_editor_window import DocumentEditorWindow


import resource.resource_rc


def main() -> None:
    app = QApplication()
    app.setWindowIcon(QPixmap(":/icon/vort.png"))
    app.setStyle("Fusion")
    text_editor_window: DocumentEditorWindow = DocumentEditorWindow()
    app.exec()


if __name__ == "__main__":
    main()
