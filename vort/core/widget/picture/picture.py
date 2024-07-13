from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QResizeEvent, QImage, QPixmap


class Picture(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__fullness: float = 0.8
        self.__image: QImage = QImage()
        self.__image.fill("blue")
        self.__image_ratio: float = 0.0
        self.updateRatio()

        self.__picture: QLabel = QLabel(self)
        self.__picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.updateSize()

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.__picture)

        self.setLayout(main_layout)

    def fullness(self) -> float:
        return self.__fullness

    def setFullness(self, fullness: int) -> None:
        self.__fullness = fullness

    def image(self) -> QImage:
        return self.__image

    def setImage(self, image: QImage) -> None:
        self.__image = image
        self.updateRatio()
        self.updateSize()

    def clearImage(self) -> None:
        self.__image = QImage(0, 0, QImage.Format.Format_ARGB32)
        self.__image.fill("blue")
        self.updateRatio()
        self.updateSize()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.updateSize()

    def updateSize(self) -> None:
        size_x: float = int(self.width() * self.__fullness)
        size_y: float = int(self.height() * self.__fullness)
        screen_ratio: float = (size_x / size_y) if (size_y != 0) else float("inf")
        if self.__image_ratio >= screen_ratio:
            size_y = int(size_x / self.__image_ratio) if (self.__image_ratio != 0) else int("inf")
        elif self.__image_ratio < screen_ratio:
            size_x = int(size_y * self.__image_ratio)

        if size_x != 0 and size_y != 0:
            self.__picture.setPixmap(QPixmap(self.__image.scaled(size_x, size_y)))
        else:
            self.__picture.clear()

    def updateRatio(self) -> None:
        self.__image_ratio = (
            (self.__image.width() / self.__image.height()) if (self.__image.height() != 0) else float("inf")
        )
