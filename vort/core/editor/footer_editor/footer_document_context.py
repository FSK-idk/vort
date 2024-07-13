from PySide6.QtGui import QTextDocument, QTextCursor

from core.editor.footer_editor.footer_document_layout import FooterDocumentLayout
from core.editor.footer_editor.components.formatting_component import FormattingComponent
from core.editor.footer_editor.components.page_component import PageComponent
from core.editor.footer_editor.components.pagination_component import PaginationComponent
from core.editor.footer_editor.components.text_component import TextComponent


class FooterDocumentContext:
    def __init__(
        self,
        document: QTextDocument,
        layout: FooterDocumentLayout,
        cursor: QTextCursor,
    ) -> None:
        self.document: QTextDocument = document
        self.layout: FooterDocumentLayout = layout
        self.cursor: QTextCursor = cursor

        self.formatting_component: FormattingComponent = FormattingComponent(self.cursor)
        self.page_component: PageComponent = PageComponent(self.cursor)
        self.pagination_component: PaginationComponent = PaginationComponent()
        self.text_component: TextComponent = TextComponent()
