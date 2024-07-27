from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
    QCheckBox,
)
from PySide6.QtGui import QImage, QGuiApplication, QPixmap

from core.widget.basic_widget import DoubleSpinBox

from core.widget.picture.picture import Picture


class EditImageDialogContext:
    def __init__(self) -> None:
        self.image: QImage = QImage()


class EditImageDialog(QDialog):
    def __init__(self, context: EditImageDialogContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.context: EditImageDialogContext = context

        self.setWindowTitle("Edit image")
        self.setMinimumWidth(400)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()
        px_to_cm: float = 2.54 / dpi

        # left

        self.picture: Picture = Picture(self)
        self.picture.setImage(context.image)

        # ratio = width / height
        self.default_image: QImage = context.image
        self.current_image: QImage = context.image
        self.ratio: float = 0.0
        self.updateRatio()

        # right

        self.filepath_line_edit_label: QLabel = QLabel(self)
        self.filepath_line_edit_label.setText("Filepath")

        self.filepath_line_edit: QLineEdit = QLineEdit(self)
        self.filepath_line_edit.setPlaceholderText("Filepath")
        self.filepath_line_edit.setEnabled(False)

        self.filepath_button: QPushButton = QPushButton(self)
        self.filepath_button.setIcon(QPixmap(":/icon/paperclip.svg"))
        self.filepath_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.filepath_button.clicked.connect(self.onFilepathClicked)

        self.filepath_clear_button: QPushButton = QPushButton(self)
        self.filepath_clear_button.setIcon(QPixmap(":/icon/eraser.svg"))
        self.filepath_clear_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.filepath_clear_button.clicked.connect(self.onFilepathClearClicked)

        filepath_line_edit_layout: QHBoxLayout = QHBoxLayout()
        filepath_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        filepath_line_edit_layout.setSpacing(2)
        filepath_line_edit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        filepath_line_edit_layout.addWidget(self.filepath_line_edit_label)
        filepath_line_edit_layout.addWidget(self.filepath_line_edit)
        filepath_line_edit_layout.addWidget(self.filepath_button)
        filepath_line_edit_layout.addWidget(self.filepath_clear_button)

        # size

        self.ratio_check_box: QCheckBox = QCheckBox(self)
        self.ratio_check_box.setText("Keep aspect ratio")
        self.ratio_check_box.checkStateChanged.connect(self.onRatioCheckBoxChanged)

        self.size_title_lable: QLabel = QLabel(self)
        self.size_title_lable.setText("Size")

        self.width_spin_box_label: QLabel = QLabel(self)
        self.width_spin_box_label.setText("Width")

        self.width_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.width_spin_box.setMinimum(0.0)
        self.width_spin_box.setSingleStep(0.25)
        self.width_spin_box.setDecimals(2)
        self.width_spin_box.setSuffix(" cm")
        self.width_spin_box.setValue(self.context.image.width() * px_to_cm)
        self.width_spin_box.valueChanged.connect(self.onWidthChanged)

        self.width_spin_box_error: QLabel = QLabel(self)
        self.width_spin_box_error.setText("Invalid input")
        self.width_spin_box_error.setFixedHeight(10)
        font = self.width_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.width_spin_box_error.setFont(font)
        self.width_spin_box_error.hide()

        width_spin_box_layout: QHBoxLayout = QHBoxLayout()
        width_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        width_spin_box_layout.setSpacing(10)
        width_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        width_spin_box_layout.addWidget(self.width_spin_box_label)
        width_spin_box_layout.addWidget(self.width_spin_box)

        self.height_spin_box_label: QLabel = QLabel(self)
        self.height_spin_box_label.setText("Height")

        self.height_spin_box: DoubleSpinBox = DoubleSpinBox(self)
        self.height_spin_box.setMinimum(0.0)
        self.height_spin_box.setSingleStep(0.25)
        self.height_spin_box.setDecimals(2)
        self.height_spin_box.setSuffix(" cm")
        self.height_spin_box.setValue(self.context.image.height() * px_to_cm)
        self.height_spin_box.valueChanged.connect(self.onHeightChanged)

        self.height_spin_box_error: QLabel = QLabel(self)
        self.height_spin_box_error.setText("Invalid input")
        self.height_spin_box_error.setFixedHeight(10)
        font = self.height_spin_box_error.font()
        font.setItalic(True)
        font.setPixelSize(10)
        self.height_spin_box_error.setFont(font)
        self.height_spin_box_error.hide()

        height_spin_box_layout = QHBoxLayout()
        height_spin_box_layout.setContentsMargins(0, 0, 0, 0)
        height_spin_box_layout.setSpacing(10)
        height_spin_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        height_spin_box_layout.addWidget(self.height_spin_box_label)
        height_spin_box_layout.addWidget(self.height_spin_box)

        size_layout = QVBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(0)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        size_layout.addWidget(self.size_title_lable)
        size_layout.addSpacing(15)
        size_layout.addWidget(self.ratio_check_box)
        size_layout.addSpacing(5)
        size_layout.addLayout(width_spin_box_layout)
        size_layout.addWidget(self.width_spin_box_error)
        size_layout.addSpacing(5)
        size_layout.addLayout(height_spin_box_layout)
        size_layout.addWidget(self.height_spin_box_error)
        size_layout.addSpacing(5)

        # button

        self.save_button = QPushButton(self)
        self.save_button.setText("Save")
        self.save_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_button.clicked.connect(self.onSaveClicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_button.clicked.connect(self.onCancelClicked)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.addLayout(filepath_line_edit_layout)
        right_layout.addSpacing(5)
        right_layout.addLayout(size_layout)
        right_layout.addStretch()
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.picture, 1)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)

    @Slot()
    def onFilepathClicked(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Image files (*.png *jpg)")
        if filepath != "":
            self.filepath_line_edit.setText(filepath)
            self.current_image = QImage(filepath)
            self.context.image = self.current_image
            self.picture.setImage(self.context.image)

            dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()
            px_to_cm: float = 2.54 / dpi

            self.updateRatio()
            self.width_spin_box.setValue(self.current_image.width() * px_to_cm)
            self.height_spin_box.setValue(self.current_image.height() * px_to_cm)

    @Slot()
    def onFilepathClearClicked(self) -> None:
        self.filepath_line_edit.setText("")
        self.current_image = self.default_image
        self.context.image = self.default_image
        self.picture.setImage(self.default_image)

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()
        px_to_cm: float = 2.54 / dpi

        self.updateRatio()
        self.width_spin_box.setValue(self.default_image.width() * px_to_cm)
        self.height_spin_box.setValue(self.default_image.height() * px_to_cm)

    def onRatioCheckBoxChanged(self, value: int) -> None:
        if value:
            self.onWidthChanged(0)

    @Slot(float)
    def onWidthChanged(self, value: float) -> None:
        if self.ratio_check_box.isChecked():
            self.height_spin_box.setValue(self.width_spin_box.value() / self.ratio)

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()
        cm_to_px: float = dpi / 2.54

        if (
            int(self.width_spin_box.value() * cm_to_px) != 0
            and int(self.height_spin_box.value() * cm_to_px) != 0
            and not self.current_image.isNull()
        ):
            self.context.image = self.current_image.scaled(
                int(self.width_spin_box.value() * cm_to_px), int(self.height_spin_box.value() * cm_to_px)
            )
            self.picture.setImage(self.context.image)
        else:
            self.context.image = QImage(0, 0, QImage.Format.Format_ARGB32)
            self.picture.setImage(self.context.image)

    @Slot(float)
    def onHeightChanged(self, value: float) -> None:
        if self.ratio_check_box.isChecked():
            self.width_spin_box.setValue(self.height_spin_box.value() * self.ratio)

        dpi: float = QGuiApplication.screens()[0].logicalDotsPerInch()
        cm_to_px: float = dpi / 2.54

        if (
            int(self.width_spin_box.value() * cm_to_px) != 0
            and int(self.height_spin_box.value() * cm_to_px) != 0
            and not self.current_image.isNull()
        ):
            self.context.image = self.current_image.scaled(
                int(self.width_spin_box.value() * cm_to_px), int(self.height_spin_box.value() * cm_to_px)
            )
            self.picture.setImage(self.context.image)
        else:
            self.context.image = QImage(0, 0, QImage.Format.Format_ARGB32)
            self.picture.setImage(self.context.image)

    @Slot()
    def onSaveClicked(self) -> None:
        is_valid = True

        is_valid = is_valid and self.width_spin_box.hasAcceptableInput()
        self.width_spin_box_error.setHidden(self.width_spin_box.hasAcceptableInput())

        is_valid = is_valid and self.height_spin_box.hasAcceptableInput()
        self.height_spin_box_error.setHidden(self.height_spin_box.hasAcceptableInput())

        if is_valid:
            self.accept()

    @Slot()
    def onCancelClicked(self) -> None:
        self.reject()

    def updateRatio(self) -> None:
        self.ratio = (
            (self.current_image.width() / self.current_image.height())
            if (self.current_image.height() != 0)
            else float("inf")
        )
