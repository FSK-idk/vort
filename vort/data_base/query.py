style_attributes: list[str] = [
    "TextStyle.name",
    "TextStyle.is_font_changed",
    "TextStyle.font_family",
    "TextStyle.font_size",
    "TextStyle.background_color_red",
    "TextStyle.background_color_green",
    "TextStyle.background_color_blue",
    "TextStyle.background_color_alpha",
    "TextStyle.foreground_color_red",
    "TextStyle.foreground_color_green",
    "TextStyle.foreground_color_blue",
    "TextStyle.foreground_color_alpha",
    "TextStyle.is_bold",
    "TextStyle.is_italic",
    "TextStyle.is_underlined",
    "TextStyle.is_paragraph_changed",
    "TextStyle.alignment",
    "TextStyle.first_line_indent",
    "TextStyle.indent",
    "TextStyle.line_spacing",
    "TextStyle.top_margin",
    "TextStyle.bottom_margin",
    "TextStyle.left_margin",
    "TextStyle.right_margin",
]


class Query:
    @staticmethod
    def createTextStyleTable() -> str:
        return """
            CREATE TABLE IF NOT EXISTS TextStyle (
                name                    text        CHECK(name != '') UNIQUE, 
                is_font_changed         integer,
                font_family             text,
                font_size               integer,
                background_color_red    integer,
                background_color_green  integer,
                background_color_blue   integer,
                background_color_alpha  integer,
                foreground_color_red    integer,
                foreground_color_green  integer,
                foreground_color_blue   integer,
                foreground_color_alpha  integer,
                is_bold                 integer,
                is_italic               integer,
                is_underlined           integer,
                is_paragraph_changed    integer,
                alignment               str,
                first_line_indent       real,
                indent                  integer,
                line_spacing            real,
                top_margin              real,
                bottom_margin           real,
                left_margin             real,
                right_margin            real
            )
        """

    @staticmethod
    def insertTextStyle() -> str:
        return """
            INSERT OR IGNORE INTO TextStyle (
                name, 
                is_font_changed,
                font_family,
                font_size,
                background_color_red,
                background_color_green,
                background_color_blue,
                background_color_alpha,
                foreground_color_red,
                foreground_color_green,
                foreground_color_blue,
                foreground_color_alpha,
                is_bold,
                is_italic,
                is_underlined,
                is_paragraph_changed,
                alignment,
                first_line_indent,
                indent,
                line_spacing,
                top_margin,
                bottom_margin,
                left_margin,
                right_margin
            )
            VALUES (
                :name, 
                :is_font_changed,
                :font_family,
                :font_size,
                :background_color_red,
                :background_color_green,
                :background_color_blue,
                :background_color_alpha,
                :foreground_color_red,
                :foreground_color_green,
                :foreground_color_blue,
                :foreground_color_alpha,
                :is_bold,
                :is_italic,
                :is_underlined,
                :is_paragraph_changed,
                :alignment,
                :first_line_indent,
                :indent,
                :line_spacing,
                :top_margin,
                :bottom_margin,
                :left_margin,
                :right_margin
            )
        """

    @staticmethod
    def updateTextStyle() -> str:
        return """
            UPDATE TextStyle
            SET name = :name, 
                is_font_changed = :is_font_changed,
                font_family = :font_family,
                font_size = :font_size,
                background_color_red = :background_color_red,
                background_color_green = :background_color_green,
                background_color_blue = :background_color_blue,
                background_color_alpha = :background_color_alpha,
                foreground_color_red = :foreground_color_red,
                foreground_color_green = :foreground_color_green,
                foreground_color_blue = :foreground_color_blue,
                foreground_color_alpha = :foreground_color_alpha,
                is_bold = :is_bold,
                is_italic = :is_italic,
                is_underlined = :is_underlined,
                is_paragraph_changed = :is_paragraph_changed,
                alignment = :alignment,
                first_line_indent = :first_line_indent,
                indent = :indent,
                line_spacing = :line_spacing,
                top_margin = :top_margin,
                bottom_margin = :bottom_margin,
                left_margin = :left_margin,
                right_margin = :right_margin
            WHERE name = :old_name
        """

    @staticmethod
    def selectTextStyleData() -> str:
        return f"""
            SELECT {', '.join(style_attributes)}
            FROM TextStyle
            WHERE TextStyle.name = :name
            AND :name != ""
            LIMIT 1
        """

    @staticmethod
    def selectTextStyleTable(ascending: bool = True) -> str:
        return f"""
            SELECT TextStyle.name
            FROM TextStyle
            WHERE (:name == '' OR TextStyle.name LIKE :name || '%')
            ORDER BY TextStyle.name {"ASC" if ascending else "DESC"}
        """

    @staticmethod
    def deleteTextStyle() -> str:
        return """
            DELETE
            FROM TextStyle
            WHERE TextStyle.name = :name
        """
