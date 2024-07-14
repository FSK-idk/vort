import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap

from core.window.editor.document_editor_window import DocumentEditorWindow

from core.util import resource_path


import resource.resource_rc


def main() -> None:
    app = QApplication()
    app.setWindowIcon(QPixmap(":/icon/vort.png"))
    app.setStyle("Fusion")

    if not os.path.isdir(resource_path("./vort/")):
        os.mkdir(resource_path("./vort/"))

    text_editor_window: DocumentEditorWindow = DocumentEditorWindow()
    app.exec()


if __name__ == "__main__":
    main()
