style_attributes: list[str] = [
    "Style.name",
    "Style.is_font_changed",
    "Style.font_family",
    "Style.font_size",
    "Style.background_color_red",
    "Style.background_color_green",
    "Style.background_color_blue",
    "Style.background_color_alpha",
    "Style.foreground_color_red",
    "Style.foreground_color_green",
    "Style.foreground_color_blue",
    "Style.foreground_color_alpha",
    "Style.is_bold",
    "Style.is_italic",
    "Style.is_underlined",
    "Style.is_paragraph_changed",
    "Style.alignment",
    "Style.is_first_line",
    "Style.first_line_indent",
    "Style.indent",
    "Style.line_spacing",
    "Style.top_margin",
    "Style.bottom_margin",
    "Style.left_margin",
    "Style.right_margin",
]


class Query:
    @staticmethod
    def createStyleTable() -> str:
        return """
            CREATE TABLE IF NOT EXISTS Style (
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
                is_first_line           integer,
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
    def insertStyle() -> str:
        return """
            INSERT OR IGNORE INTO Style (
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
                is_first_line,
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
                :is_first_line,
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
    def updateStyle() -> str:
        return """
            UPDATE Style
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
                is_first_line = :is_first_line,
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
    def selectStyleData() -> str:
        return f"""
            SELECT {', '.join(style_attributes)}
            FROM Style
            WHERE Style.name = :name
            LIMIT 1
        """

    @staticmethod
    def selectStyleTable(ascending: bool = True) -> str:
        return f"""
            SELECT Style.name
            FROM Style
            WHERE (:name == '' OR Style.name LIKE :name || '%')
            ORDER BY Style.name {"ASC" if ascending else "DESC"}
        """

    @staticmethod
    def deleteStyle() -> str:
        return """
            DELETE
            FROM Style
            WHERE Style.name = :name
        """
