from abc import ABC, abstractmethod


class WebdriverInterface(ABC):

    @abstractmethod
    def get_page(self, url) -> None:
        """
        Переход по ссылке
        :return:
        """

    @abstractmethod
    def set_driver_config(self) -> None:
        """
        Настройка веб-драйвера
        :return:
        """

    @abstractmethod
    def close(self) -> None:
        """
        Закрытие окна
        :return:
        """
