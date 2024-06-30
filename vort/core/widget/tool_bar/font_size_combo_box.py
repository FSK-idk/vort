from PySide6.QtCore import QRegularExpression, QRegularExpressionMatch, Signal, Slot
from PySide6.QtWidgets import QComboBox, QWidget, QCompleter
from PySide6.QtGui import QRegularExpressionValidator


class FontSizeComboBox(QComboBox):
    fontSizeChanged = Signal(int)
    closed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        default_sizes = [6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 36, 42, 48]
        self.regex_without_pt: QRegularExpression = QRegularExpression("[1-9][0-9]?$")

        self.setEditable(True)
        self.setCompleter(QCompleter())  # remove auto complete
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.lineEdit().setValidator(QRegularExpressionValidator("[1-9][0-9]?( pt)?$"))
        self.addItems([str(size) + " pt" for size in default_sizes])

        self.activated.connect(self.onActivated)
        self.lineEdit().returnPressed.connect(self.onLineEditReturnPressed)

    def setFontSize(self, font_size: int) -> None:
        self.setEditText(str(font_size) + " pt")

    @Slot(int)
    def onActivated(self, index: int) -> None:
        text = self.currentText()
        self.fontSizeChanged.emit(int(text[:-3]))
        self.closed.emit()

    @Slot()
    def onLineEditReturnPressed(self) -> None:
        self.addPointSuffix()
        text = self.currentText()
        self.fontSizeChanged.emit(int(text[:-3]))
        self.closed.emit()

    @Slot()
    def addPointSuffix(self) -> None:
        rem: QRegularExpressionMatch = self.regex_without_pt.match(self.currentText())
        if rem.hasMatch():
            self.setEditText(self.currentText() + " pt")
