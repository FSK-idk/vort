from PySide6.QtGui import QTextDocument, QTextCursor

from core.editor.text_editor.text_document_layout import TextDocumentLayout
from core.editor.text_editor.component.history_component import HistoryComponent
from core.editor.text_editor.component.clipboard_component import ClipboardComponent
from core.editor.text_editor.component.selection_component import SelectionComponent
from core.editor.text_editor.component.input_component import InputComponent
from core.editor.text_editor.component.movement_component import MovementComponent
from core.editor.text_editor.component.paragraph_component import ParagraphComponent
from core.editor.text_editor.component.char_component import CharComponent
from core.editor.text_editor.component.text_style_component import TextStyleComponent
from core.editor.text_editor.component.search_component import SearchComponent


class TextDocumentContext:
    def __init__(
        self,
        document: QTextDocument,
        layout: TextDocumentLayout,
        cursor: QTextCursor,
    ) -> None:
        self.document: QTextDocument = document
        self.layout: TextDocumentLayout = layout
        self.cursor: QTextCursor = cursor

        self.history_component: HistoryComponent = HistoryComponent(self.cursor)
        self.clipboard_component: ClipboardComponent = ClipboardComponent(self.cursor)
        self.selection_component: SelectionComponent = SelectionComponent(self.cursor)
        self.input_component: InputComponent = InputComponent(self.cursor)
        self.movement_component: MovementComponent = MovementComponent(self.cursor, self.layout)
        self.paragraph_component: ParagraphComponent = ParagraphComponent(self.cursor)
        self.char_component: CharComponent = CharComponent(self.cursor)
        self.text_style_component: TextStyleComponent = TextStyleComponent(self.cursor)
        self.search_component: SearchComponent = SearchComponent(self.cursor)
