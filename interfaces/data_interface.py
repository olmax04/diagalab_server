from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Union, Set, List

from selenium.webdriver.remote.webelement import WebElement

from models.result_model import Result


class DataInterface(ABC):

    @abstractmethod
    def get_one_info(self, record: WebElement) -> Result:
        """
        Получение информации одного элемента
        :param record: WebElement
        :return:
        """
    @abstractmethod
    def get_set_info(self) -> Union[Set[Result] or List[Result] or None]:
        """
        Получение информации всех элементов
        :return:
        """