from PySide6.QtWidgets import QApplication

from core.window.text_editor_window import TextEditorWindow


def main() -> None:
    app = QApplication()
    app.setStyle("Fusion")
    text_editor_window = TextEditorWindow()
    app.exec()


if __name__ == "__main__":
    main()
