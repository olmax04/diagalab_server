from abc import abstractmethod, ABC


class PaginationInterface(ABC):
    @abstractmethod
    def next_page(self) -> None:
        """
        Переход на новую страницу
        :return:
        """
