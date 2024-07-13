from PySide6.QtWidgets import QApplication

from core.window.editor.document_editor_window import DocumentEditorWindow


def main() -> None:
    app = QApplication()
    app.setStyle("Fusion")
    text_editor_window: DocumentEditorWindow = DocumentEditorWindow()
    app.exec()


if __name__ == "__main__":
    main()
