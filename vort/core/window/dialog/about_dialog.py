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
    QScrollArea
)
from PySide6.QtGui import QImage, QDesktopServices

from core.widget.picture.picture import Picture


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("About")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.resize(600, 300)

        # left

        self.picture: Picture = Picture(self)
        self.picture.setImage(QImage(":/icon/vort.png"))

        self.main_text_lable: QLabel = QLabel()
        self.main_text_lable.setText(
            textwrap.dedent(
                """
                VORT v1.0.0

                Lightweight text editor written in PySide

                Copyright 2024 FSK
                """
            )
        )
        self.main_text_lable.setWordWrap(True)

        self.parts_label: QLabel = QLabel()
        self.parts_label.setText("This application uses the following parts:")

        self.lucide_lable: QLabel = QLabel()
        self.lucide_lable.setText("Lucide icons")

        self.lucide_button: QPushButton = QPushButton(self)
        self.lucide_button.setText("website")
        self.lucide_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lucide_button.clicked.connect(self.onLucideClicked)

        lucide_label_layout: QHBoxLayout = QHBoxLayout()
        lucide_label_layout.setContentsMargins(0, 0, 0, 0)
        lucide_label_layout.setSpacing(0)
        lucide_label_layout.addWidget(self.lucide_lable)
        lucide_label_layout.addStretch()
        lucide_label_layout.addWidget(self.lucide_button)

        self.lucide_text: QLabel = QLabel()
        self.lucide_text.setText(
            textwrap.dedent(
                """
                Copyright (c) for portions of Lucide are held by Cole Bemis 2013-2022 as part of Feather (MIT). All other copyright (c) for Lucide are held by Lucide Contributors 2022.
                """
            )
        )
        self.lucide_text.setWordWrap(True)
        #self.lucide_text.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        lucide_layout: QVBoxLayout = QVBoxLayout()
        lucide_layout.setContentsMargins(0, 0, 0, 0)
        lucide_layout.setSpacing(0)
        lucide_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        lucide_layout.addLayout(lucide_label_layout)
        lucide_layout.addSpacing(5)
        lucide_layout.addWidget(self.lucide_text)

        parts_layout: QVBoxLayout = QVBoxLayout()
        parts_layout.setContentsMargins(0, 0, 0, 0)
        parts_layout.setSpacing(0)
        parts_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        parts_layout.addWidget(self.parts_label)
        parts_layout.addSpacing(15)
        parts_layout.addLayout(lucide_layout)

        self.parts_widget: QWidget = QWidget()
        self.parts_widget.setLayout(parts_layout)

        self.parts_scroll: QScrollArea = QScrollArea()
        self.parts_scroll.setWidget(self.parts_widget)
        self.parts_scroll.setWidgetResizable(True)
        self.parts_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

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
        right_layout.addWidget(self.main_text_lable)
        right_layout.addWidget(self.parts_label)
        right_layout.addWidget(self.parts_scroll)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.picture, 1)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)

    @Slot()
    def onLucideClicked(self) -> None:
        QDesktopServices.openUrl("https://lucide.dev/")

    @Slot()
    def onGitHubClicked(self) -> None:
        QDesktopServices.openUrl("https://github.com/FSK-idk/vort")
