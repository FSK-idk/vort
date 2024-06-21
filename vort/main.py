from PySide6.QtWidgets import QApplication

from view.window.editor_window import EditorWindow


def main() -> None:
    app = QApplication()
    app.setStyle("Fusion")

    ex = EditorWindow()
    ex.show()

    app.exec()


if __name__ == "__main__":
    main()
