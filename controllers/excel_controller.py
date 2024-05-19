from typing import List

import pandas as pd

from models.result_model import Result


def read_cities(filepath) -> List[str]:
    """
    Получение названий городов из файла excel
    :param filepath: str
    :return:
    """
    df = pd.read_excel(filepath)

    # Получаем все значения из столбца 'CityName'
    city_names = df['CityName'].tolist()
    return city_names


def create_result_document(filename, result: List[Result]) -> None:
    """
    Создание результирующего документа
    :return:
    """
    # Создаем DataFrame
    df = pd.DataFrame({
        'ParsingDateTime': [item.timestamp for item in result],
        'Source': [item.source for item in result],
        'URL': [item.url for item in result],
        'ServiceName': [item.name for item in result],
        'City': [item.city for item in result],
        'PriceType': ["Online" if item.status == "online" or item.source == "Alab" else "Offline" for item in result],
        'Price': [item.status if item.price <= 0 else item.price for item in result]
    })

    # Сохраняем DataFrame в файл Excel
    df.to_excel(excel_writer=filename, index=False)


def get_statistic(cities: List[str], result: List[Result]):
    city_dict = {
        city: {"Parced Prices Alab": len([item for item in result if item.city == city and item.source == "Alab"]),
               "Parced Prices Diag": len([item for item in result if item.city == city and item.source == "Diag"]),
               "available_Alab": 0, "available_Diag": 0,
               "unavailable_Alab": 0, "unavailable_Diag": 0,
               "offline_only_Diag": 0} for city in cities}

    # обновляем счетчики в словаре
    for item in result:
        if item.price is not None and item.price > 0:
            city_dict[item.city][f"available_{item.source}"] += 1
        elif item.status == "not_available":
            city_dict[item.city][f"unavailable_{item.source}"] += 1
        if item.status == "offline_only":
            city_dict[item.city][f"offline_only_{item.source}"] += 1

    return city_dict


def create_log_document(filename, cities: List[str], result: List[Result]) -> None:
    """
    Создание документа с логами
    :return:
    """
    city_dict = get_statistic(cities, result)
    # Создаем DataFrame

    df = pd.DataFrame({
        'CityName': city_dict.keys(),
        'Parced Prices Alab': [item['Parced Prices Alab'] for item in city_dict.values()],
        'Parced Prices Diag': [item['Parced Prices Diag'] for item in city_dict.values()],
        'not_available Prices Alab': [item['unavailable_Alab'] for item in city_dict.values()],
        'offline_only Prices Diag': [item['offline_only_Diag'] for item in city_dict.values()],
        'not_available Prices Diag': [item['unavailable_Diag'] for item in city_dict.values()],
    })
    # Сохраняем DataFrame в файл Excel
    df.to_excel(filename, index=False)
