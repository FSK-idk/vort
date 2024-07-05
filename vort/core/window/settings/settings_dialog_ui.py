from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
)

from core.window.settings.page_settings_ui import PageSettingsUI, PageSettingsContext
from core.window.settings.paragraph_settings_ui import ParagraphSettingsUI, ParagraphSettingsContext
from core.window.settings.header_settings_ui import HeaderSettingsUI, HeaderSettingsContext
from core.window.settings.footer_settings_ui import FooterSettingsUI, FooterSettingsContext


class SettingsContext:
    def __init__(self) -> None:
        self.page_context: PageSettingsContext = PageSettingsContext()
        self.paragraph_context: ParagraphSettingsContext = ParagraphSettingsContext()
        self.header_context: HeaderSettingsContext = HeaderSettingsContext()
        self.footer_context: FooterSettingsContext = FooterSettingsContext()


class SettingsDialogUI(QDialog):
    applied = Signal(SettingsContext)

    def __init__(self, context: SettingsContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: SettingsContext = context

        self.setWindowTitle("Settings")
        self.resize(600, 400)

        self.page_settings: PageSettingsUI = PageSettingsUI(self.context.page_context)
        self.paragraph_settings: ParagraphSettingsUI = ParagraphSettingsUI(self.context.paragraph_context)
        self.header_settings: HeaderSettingsUI = HeaderSettingsUI(self.context.header_context)
        self.footer_settings: FooterSettingsUI = FooterSettingsUI(self.context.footer_context)

        self.tab_index = {"page": 0, "paragraph": 1, "header": 2, "footer": 3}

        self.tab_widget: QTabWidget = QTabWidget()
        self.tab_widget.setContentsMargins(50, 50, 50, 50)
        self.tab_widget.addTab(self.page_settings, "Page")
        self.tab_widget.addTab(self.paragraph_settings, "Paragraph")
        self.tab_widget.addTab(self.header_settings, "Header")
        self.tab_widget.addTab(self.footer_settings, "Footer")

        # buttons

        self.apply_button = QPushButton(self)
        self.apply_button.setText("Apply")
        self.apply_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.apply_button.clicked.connect(self.onApplyClicked)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ok_button.clicked.connect(self.onOkClicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_button.clicked.connect(self.onCancelClicked)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def openTab(self, name: str) -> None:
        self.tab_widget.setCurrentIndex(self.tab_index[name])

    def onApplyClicked(self) -> bool:
        # validate

        # set context

        self.applied.emit(self.context)
        return True

    def onOkClicked(self) -> None:
        if self.onApplyClicked():
            self.accept()

    def onCancelClicked(self) -> None:
        self.reject()
