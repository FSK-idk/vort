import os

from PySide6.QtCore import Signal, QObject
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord

from data_base.query import Query
from core.widget.text_style.text_style import TextStyle

from core.util import resource_path


class DataBase(QObject):
    updatedStyleTable: Signal = Signal()

    def init(self) -> None:
        if not os.path.isdir(resource_path("./vort/data/")):
            os.mkdir(resource_path("./vort/data/"))

        self.data_base: QSqlDatabase = QSqlDatabase("QSQLITE")
        self.data_base.setDatabaseName(resource_path("./vort/data/library.sqlite"))
        self.data_base.open()

        QSqlQuery(Query.createTextStyleTable(), self.data_base).exec()

    def insertTextStyle(self, style: TextStyle) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.insertTextStyle())
        query.bindValue(":name", style.name)
        query.bindValue(":is_font_changed", 1 if style.is_font_changed else 0)
        query.bindValue(":font_family", style.font_family)
        query.bindValue(":font_size", style.font_size)
        query.bindValue(":background_color_red", style.background_color.red())
        query.bindValue(":background_color_green", style.background_color.green())
        query.bindValue(":background_color_blue", style.background_color.blue())
        query.bindValue(":background_color_alpha", style.background_color.alpha())
        query.bindValue(":foreground_color_red", style.foreground_color.red())
        query.bindValue(":foreground_color_green", style.foreground_color.green())
        query.bindValue(":foreground_color_blue", style.foreground_color.blue())
        query.bindValue(":foreground_color_alpha", style.foreground_color.alpha())
        query.bindValue(":is_bold", 1 if style.is_bold else 0)
        query.bindValue(":is_italic", 1 if style.is_italic else 0)
        query.bindValue(":is_underlined", 1 if style.is_underlined else 0)
        query.bindValue(":is_paragraph_changed", 1 if style.is_paragraph_changed else 0)
        query.bindValue(":alignment", style.ALIGNMENT_NAMES[style.ALIGNMENT_FLAGS.index(style.alignment)])
        query.bindValue(":first_line_indent", style.first_line_indent)
        query.bindValue(":indent", style.indent)
        query.bindValue(":line_spacing", style.line_spacing)
        query.bindValue(":top_margin", style.top_margin)
        query.bindValue(":bottom_margin", style.bottom_margin)
        query.bindValue(":left_margin", style.left_margin)
        query.bindValue(":right_margin", style.right_margin)
        query.exec()

        self.updatedStyleTable.emit()

    def updateTextStyle(self, old_name: str, style: TextStyle) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.updateTextStyle())
        query.bindValue(":name", style.name)
        query.bindValue(":is_font_changed", 1 if style.is_font_changed else 0)
        query.bindValue(":font_family", style.font_family)
        query.bindValue(":font_size", style.font_size)
        query.bindValue(":background_color_red", style.background_color.red())
        query.bindValue(":background_color_green", style.background_color.green())
        query.bindValue(":background_color_blue", style.background_color.blue())
        query.bindValue(":background_color_alpha", style.background_color.alpha())
        query.bindValue(":foreground_color_red", style.foreground_color.red())
        query.bindValue(":foreground_color_green", style.foreground_color.green())
        query.bindValue(":foreground_color_blue", style.foreground_color.blue())
        query.bindValue(":foreground_color_alpha", style.foreground_color.alpha())
        query.bindValue(":is_bold", 1 if style.is_bold else 0)
        query.bindValue(":is_italic", 1 if style.is_italic else 0)
        query.bindValue(":is_underlined", 1 if style.is_underlined else 0)
        query.bindValue(":is_paragraph_changed", 1 if style.is_paragraph_changed else 0)
        query.bindValue(":alignment", style.ALIGNMENT_NAMES[style.ALIGNMENT_FLAGS.index(style.alignment)])
        query.bindValue(":first_line_indent", style.first_line_indent)
        query.bindValue(":indent", style.indent)
        query.bindValue(":line_spacing", style.line_spacing)
        query.bindValue(":top_margin", style.top_margin)
        query.bindValue(":bottom_margin", style.bottom_margin)
        query.bindValue(":left_margin", style.left_margin)
        query.bindValue(":right_margin", style.right_margin)
        query.bindValue(":old_name", old_name)
        query.exec()

        self.updatedStyleTable.emit()

    def selectTextStyleData(self, name: str) -> TextStyle:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.selectTextStyleData())
        query.bindValue(":name", name)
        query.exec()

        style: TextStyle = TextStyle()
        rec: QSqlRecord = query.record()

        if query.next():
            row = [query.value(index) for index in range(rec.count())]
            style.setData(row)

        return style

    def deleteTextStyle(self, name: int) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.deleteTextStyle())
        query.bindValue(":name", name)
        query.exec()

        self.updatedStyleTable.emit()


data_base: DataBase = DataBase()
