from abc import abstractmethod, ABC

from selenium.webdriver.remote.webelement import WebElement


class SelectOptionInterface(ABC):
    @abstractmethod
    def select_option_index(self, element: WebElement, index: int) -> None:
        """
        Выбор элемента из dropdown по средству индекса
        :param element: WebElement
        :param index: int
        :return:
        """

    @abstractmethod
    def select_option_value(self, element: WebElement, value: str) -> None:
        """
        Выбор элемента из dropdown по средству знвчения
        :param element: WebElement
        :param value: str
        :return:
        """
