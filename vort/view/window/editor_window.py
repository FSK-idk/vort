from PySide6.QtWidgets import QMainWindow, QPushButton


class EditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.btn = QPushButton(self)

        self.setCentralWidget(self.btn)

        self.setWindowTitle("vort")
        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(400, 300)
