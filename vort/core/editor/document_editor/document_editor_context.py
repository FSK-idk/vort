from core.editor.page_layout.page_layout import PageLayout
from core.editor.text_editor.text_editor import TextEditor
from core.editor.header_editor.header_editor import HeaderEditor
from core.editor.footer_editor.footer_editor import FooterEditor
from core.editor.document_editor.document_canvas import DocumentCanvas


class DocumentEditorContext:
    def __init__(
        self,
        page_layout: PageLayout,
        text_editor: TextEditor,
        header_editor: HeaderEditor,
        footer_editor: FooterEditor,
        canvas: DocumentCanvas,
    ) -> None:
        self.page_layout: PageLayout = page_layout
        self.text_editor: TextEditor = text_editor
        self.header_editor: HeaderEditor = header_editor
        self.footer_editor: FooterEditor = footer_editor
        self.canvas: DocumentCanvas = canvas
