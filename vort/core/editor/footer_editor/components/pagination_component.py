from PySide6.QtCore import QObject, Signal


class PaginationComponent(QObject):
    applied: Signal = Signal()
    paginationTurned: Signal = Signal(bool)

    def __init__(self) -> None:
        super().__init__()

        self.__pagination_starting_number: int = 0
        self.__is_pagination_turned: bool = False

    def isPaginationTurned(self) -> bool:
        return self.__is_pagination_turned

    def setPaginationTurned(self, is_turned: bool) -> None:
        if self.__is_pagination_turned != is_turned:
            self.__is_pagination_turned = is_turned
            self.paginationTurned.emit(self.__is_pagination_turned)
            self.applied.emit()

    def paginationStartingNumber(self) -> int:
        return self.__pagination_starting_number

    def setPaginationStartingNumber(self, number: int) -> None:
        if self.__pagination_starting_number != number:
            self.__pagination_starting_number = number
            self.applied.emit()
