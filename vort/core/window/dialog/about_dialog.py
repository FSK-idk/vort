import textwrap

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
)
from PySide6.QtGui import QImage, QDesktopServices

from core.widget.picture.picture import Picture


import resource.resource_rc


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("About")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.resize(600, 300)

        # left

        self.picture: Picture = Picture(self)
        self.picture.setImage(QImage(":/icon/vort.png"))

        self.text_lable: QLabel = QLabel()
        self.text_lable.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.text_lable.setText(
            textwrap.dedent(
                """
                VORT

                Lightweight text editor written in PySide

                Copyright 2024 FSK
                """
            )
        )
        self.text_lable.setWordWrap(True)

        self.github_button: QPushButton = QPushButton(self)
        self.github_button.setText("GitHub")
        self.github_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.github_button.clicked.connect(self.onGitHubClicked)

        self.ok_button: QPushButton = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ok_button.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.github_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.addWidget(self.text_lable)
        right_layout.addStretch(1)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.picture, 1)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)

    @Slot()
    def onGitHubClicked(self) -> None:
        QDesktopServices.openUrl("https://github.com/FSK-idk/vort")
