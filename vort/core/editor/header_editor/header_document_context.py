from PySide6.QtGui import QTextDocument, QTextCursor

from core.editor.header_editor.header_document_layout import HeaderDocumentLayout
from core.editor.header_editor.components.formatting_component import FormattingComponent
from core.editor.header_editor.components.page_component import PageComponent
from core.editor.header_editor.components.pagination_component import PaginationComponent
from core.editor.header_editor.components.text_component import TextComponent


class HeaderDocumentContext:
    def __init__(
        self,
        document: QTextDocument,
        layout: HeaderDocumentLayout,
        cursor: QTextCursor,
    ) -> None:
        self.document: QTextDocument = document
        self.layout: HeaderDocumentLayout = layout
        self.cursor: QTextCursor = cursor

        self.formatting_component: FormattingComponent = FormattingComponent(self.cursor)
        self.page_component: PageComponent = PageComponent(self.cursor)
        self.pagination_component: PaginationComponent = PaginationComponent()
        self.text_component: TextComponent = TextComponent()
