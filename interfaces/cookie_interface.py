from abc import ABC, abstractmethod


class CookieInterface(ABC):

    @abstractmethod
    def cookie(self) -> None:
        """
        Метод прохода диалогового окна cookie файлов
        :return:
        """
