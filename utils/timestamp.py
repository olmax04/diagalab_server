from datetime import datetime


def create_timestamp() -> str:
    """
    Получение текущего timestamp
    :return: timestamp(str)
    """
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp
