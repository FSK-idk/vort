from PySide6.QtWidgets import (
    QMenuBar,
    QMenu,
    QToolBar,
    QComboBox,
    QMainWindow,
    QWidget,
    QStatusBar,
    QLabel,
    QFontComboBox,
    QLineEdit,
    QCompleter,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QApplication,
    QListWidget,
    QMainWindow,
    QTableWidget,
)
from PySide6.QtGui import (
    QAction,
    QPixmap,
    QIntValidator,
    QRegularExpressionValidator,
    QMoveEvent,
    QColor,
    QResizeEvent,
    QPainter,
    QBrush,
    QPaintEvent,
    QPalette,
)
from PySide6.QtCore import (
    QEvent,
    QObject,
    Qt,
    QRegularExpression,
    QRegularExpressionMatch,
    QRect,
    QPoint,
    QTimer,
    QSize,
    QPropertyAnimation,
    Property,
    Signal,
)


from view.widget.color_palette import ColorPalette


class ColorPicker(QWidget):
    colorSelected = Signal(QColor)

    def __init__(self, text: str | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        icon: QPixmap = QPixmap(16, 16)
        icon.fill(Qt.GlobalColor.black)

        self.button: QPushButton = QPushButton(text)
        self.button.setCheckable(True)
        self.button.setIcon(icon)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.color_table: ColorPalette = ColorPalette(self)
        self.color_table.setWindowFlags(Qt.WindowType.Popup)

        self.button.clicked.connect(self.showPopup)
        self.color_table.hidden.connect(self.button.animateClick)
        self.color_table.colorSelected.connect(self.onColorSelected)

    def setColor(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.button.setIcon(icon)

    def showPopup(self, checked):
        if checked:
            self.color_table.setVisible(checked)
            if not self.color_table.isVisible():
                return
            rect: QRect = self.button.geometry()
            bottomLeft: QPoint = self.mapToGlobal(rect.bottomLeft())
            self.color_table.move(bottomLeft)
        else:
            self.color_table.blockSignals(True)
            self.color_table.hide()
            self.color_table.blockSignals(False)

    def onColorSelected(self, color: QColor) -> None:
        icon: QPixmap = QPixmap(16, 16)
        icon.fill(color)
        self.button.setIcon(icon)
        self.colorSelected.emit(color)
