from abc import ABC, abstractmethod


class ScrollIntoInterface(ABC):
    @abstractmethod
    def scroll_into_element(self, element)-> None:
        """
        Скролл к элементу
        :param element:
        :return:
        """