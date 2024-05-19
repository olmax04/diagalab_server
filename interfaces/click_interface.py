from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement


class ClickInterface(ABC):
    @abstractmethod
    def click_button_id(self, id: str) -> None:
        """
        Клик на элемент по ID
        :param id: str
        :return:
        """

    @abstractmethod
    def click_button_xpath(self, xpath: str) -> None:
        """
        Клик на элемент по XPATH
        :param xpath: str
        :return:
        """

    @abstractmethod
    def click_button_class(self, class_name: str) -> None:
        """
        Клик на элемент по CLASS_NAME
        :param class_name: str
        :return:
        """

    @abstractmethod
    def click_element(self, element: WebElement) -> None:
        """
        Клик на элемент по средству объекта элемента и выполнения скрипта
        :param element: WebElement
        :return:
        """
