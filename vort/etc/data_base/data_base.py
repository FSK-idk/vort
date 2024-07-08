import os

from PySide6.QtCore import Signal, QObject
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord

from etc.data_base.query import Query
from etc.style_data import StyleData


class DataBase(QObject):
    updatedStyleTable: Signal = Signal()

    def init(self) -> None:
        if not os.path.isdir("./vort/data/"):
            os.mkdir("./vort/data/")

        self.data_base: QSqlDatabase = QSqlDatabase("QSQLITE")
        self.data_base.setDatabaseName("./vort/data/library.sqlite")
        self.data_base.open()

        QSqlQuery(Query.createStyleTable(), self.data_base).exec()

    def insertStyle(self, style_data: StyleData) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.insertStyle())
        query.bindValue(":name", style_data.name)
        query.bindValue(":is_font_changed", style_data.is_font_changed)
        query.bindValue(":font_family", style_data.font_family)
        query.bindValue(":font_size", style_data.font_size)
        query.bindValue(":background_color_red", style_data.background_color.red())
        query.bindValue(":background_color_green", style_data.background_color.green())
        query.bindValue(":background_color_blue", style_data.background_color.blue())
        query.bindValue(":background_color_alpha", style_data.background_color.alpha())
        query.bindValue(":foreground_color_red", style_data.foreground_color.red())
        query.bindValue(":foreground_color_green", style_data.foreground_color.green())
        query.bindValue(":foreground_color_blue", style_data.foreground_color.blue())
        query.bindValue(":foreground_color_alpha", style_data.foreground_color.alpha())
        query.bindValue(":is_bold", style_data.is_bold)
        query.bindValue(":is_italic", style_data.is_italic)
        query.bindValue(":is_underlined", style_data.is_underlined)
        query.bindValue(":is_paragraph_changed", style_data.is_paragraph_changed)
        query.bindValue(
            ":alignment", style_data.ALIGNMENT_NAMES[style_data.ALIGNMENT_FLAGS.index(style_data.alignment)]
        )
        query.bindValue(":first_line_indent", style_data.first_line_indent)
        query.bindValue(":indent", style_data.indent)
        query.bindValue(":line_spacing", style_data.line_spacing)
        query.bindValue(":top_margin", style_data.top_margin)
        query.bindValue(":bottom_margin", style_data.bottom_margin)
        query.bindValue(":left_margin", style_data.left_margin)
        query.bindValue(":right_margin", style_data.right_margin)
        query.exec()

        self.updatedStyleTable.emit()

    def updateStyle(self, old_name: str, style_data: StyleData) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.updateStyle())
        query.bindValue(":name", style_data.name)
        query.bindValue(":is_font_changed", style_data.is_font_changed)
        query.bindValue(":font_family", style_data.font_family)
        query.bindValue(":font_size", style_data.font_size)
        query.bindValue(":background_color_red", style_data.background_color.red())
        query.bindValue(":background_color_green", style_data.background_color.green())
        query.bindValue(":background_color_blue", style_data.background_color.blue())
        query.bindValue(":background_color_alpha", style_data.background_color.alpha())
        query.bindValue(":foreground_color_red", style_data.foreground_color.red())
        query.bindValue(":foreground_color_green", style_data.foreground_color.green())
        query.bindValue(":foreground_color_blue", style_data.foreground_color.blue())
        query.bindValue(":foreground_color_alpha", style_data.foreground_color.alpha())
        query.bindValue(":is_bold", style_data.is_bold)
        query.bindValue(":is_italic", style_data.is_italic)
        query.bindValue(":is_underlined", style_data.is_underlined)
        query.bindValue(":is_paragraph_changed", style_data.is_paragraph_changed)
        query.bindValue(
            ":alignment", style_data.ALIGNMENT_NAMES[style_data.ALIGNMENT_FLAGS.index(style_data.alignment)]
        )
        query.bindValue(":first_line_indent", style_data.first_line_indent)
        query.bindValue(":indent", style_data.indent)
        query.bindValue(":line_spacing", style_data.line_spacing)
        query.bindValue(":top_margin", style_data.top_margin)
        query.bindValue(":bottom_margin", style_data.bottom_margin)
        query.bindValue(":left_margin", style_data.left_margin)
        query.bindValue(":right_margin", style_data.right_margin)
        query.bindValue(":old_name", old_name)
        query.exec()

        self.updatedStyleTable.emit()

    def selectStyleData(self, name: str) -> StyleData:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.selectStyleData())
        query.bindValue(":name", name)
        query.exec()

        style_data: StyleData = StyleData()
        rec: QSqlRecord = query.record()

        if query.next():
            row = [query.value(index) for index in range(rec.count())]
            style_data.setData(row)

        return style_data

    def deleteStyle(self, name: int) -> None:
        query: QSqlQuery = QSqlQuery(self.data_base)
        query.prepare(Query.deleteStyle())
        query.bindValue(":name", name)
        query.exec()

        self.updatedStyleTable.emit()


data_base: DataBase = DataBase()
