from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from controller.text_editor_window_controller import TextEditorWindowController


def main() -> None:
    app = QApplication()
    app.setStyle("Fusion")
    ex = TextEditorWindowController()

    app.exec()


if __name__ == "__main__":
    main()
