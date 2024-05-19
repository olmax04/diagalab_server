from controllers.timestamp_controller import create_timestamp


class Result:
    """
    Класс Result представляет результат поиска.

    Атрибуты:
    source (str): Источник данных.
    city (str): Город, в котором был найден результат.
    name (str): Название результата.
    price (str): Цена результата. Может быть None, если цена не указана.
    url (str): URL-адрес результата.
    status (str): Статус записи.
    timestamp (str): Временная метка создания результата.
    """

    def __init__(self, source, city, name, price, url, status="not_available"):
        """
        Инициализирует объект класса Result.

        Параметры:
        source (str): Источник данных.
        city (str): Город, в котором был найден результат.
        name (str): Название результата.
        price (str): Цена результата. Может быть None, если цена не указана.
        url (str): URL-адрес результата.
        status (str): Статус записи.
        """
        self.source = source
        self.city = city
        self.name = name
        self.price: float = price
        self.url = url
        self.status = status
        self.set_timestamp()

    def __str__(self):
        """
        Возвращает строковое представление объекта класса Result.

        Возвращает:
        str: Строковое представление объекта класса Result.
        """
        return (f"[Source: {self.source}, City: {self.city}, Name: {self.name}, Price: {self.price}, Url: {self.url}, "
                f"Timestamp: {self.timestamp}, Status: {self.status}]")

    def set_timestamp(self):
        """
        Устанавливает временную метку для объекта класса Result.
        """
        self.timestamp = create_timestamp()
