from abc import abstractmethod, ABC


class PointInterface(ABC):

    @abstractmethod
    def select_point(self) -> None:
        """
        Выбор пункта
        :return:
        """
