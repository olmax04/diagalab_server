from abc import ABC, abstractmethod


class AdInterface(ABC):

    @abstractmethod
    def close_ad_dialog(self) -> None:
        """
        Метод закрытия рекламного диалогового окна
        :return:
        """
