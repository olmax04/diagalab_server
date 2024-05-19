# import tkinter as tk
# from tkinter import filedialog
# import pandas as pd
# import time
#
#
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.load_button = tk.Button(self)
#         self.load_button["text"] = "Загрузить файл"
#         self.load_button["command"] = self.load_file
#         self.load_button.pack(side="top")
#
#         self.start_button = tk.Button(self)
#         self.start_button["text"] = "Запуск"
#         self.start_button["command"] = self.start_loading
#         self.start_button.pack(side="top")
#
#         self.export_button = tk.Button(self)
#         self.export_button["text"] = "Экспорт"
#         self.export_button["command"] = self.export_file
#         self.export_button["state"] = "disabled"
#         self.export_button.pack(side="top")
#
#     def load_file(self):
#         self.filename = filedialog.askopenfilename()
#
#     def start_loading(self):
#         # Здесь должен быть ваш код для загрузки данных
#         time.sleep(5)  # Имитация процесса загрузки
#         self.export_button["state"] = "normal"
#
#     def export_file(self):
#         export_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
#                                                        filetypes=(("Excel", "*.xlsx"), ("All Files", "*.*"),))
#         df = pd.DataFrame()  # Здесь должны быть ваши данные
#         df.to_excel(export_filename)
#
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()

"""
TEST ALAB
"""
from services.alab_service import Alab

# alab = Alab("Warszawa")
# alab.cookie()
# alab.select_point()
# alab.get_page()
# results = alab.get_set_info()
# for result in results:
#     print(result)
# alab.close()

# """
# TEST DIAG
# """
# from services.diag_service import Diag
#
# diag = Diag("Warszawa")
# diag.cookie()
# diag.click_filter()
# diag.select_point()
# results = diag.get_set_info()
# for result in results:
#     print(result)
# diag.close()
from datetime import datetime

# Get the current timestamp
from datetime import datetime

# Get the current timestamp
current_timestamp = datetime.timestamp(datetime.now())

# Convert the timestamp to a datetime object
current_datetime = datetime.fromtimestamp(current_timestamp)

# Format the datetime object
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

print("Formatted datetime:", formatted_datetime)

# предположим, что у вас есть следующие списки
# cities = ["City1", "City2", "City3"]
# results = [
#     {"source": "Alab", "city": "City1", "name": "Name1", "price": 10, "url": "url1", "timestamp": "time1"},
#     {"source": "Diag", "city": "City1", "name": "Name2", "price": 20, "url": "url2", "timestamp": "time2"},
#     {"source": "Alab", "city": "City2", "name": "Name3", "price": None, "url": "url3", "timestamp": "time3"},
#     {"source": "Diag", "city": "City3", "name": "Name4", "price": 30, "url": "url4", "timestamp": "time4"},
#     {"source": "Alab", "city": "City3", "name": "Name5", "price": 40, "url": "url5", "timestamp": "time5"},
# ]
#
# # создаем словарь
# city_dict = {city: {"Alab": 0, "Diag": 0} for city in cities}
#
# # обновляем счетчики в словаре
# for result in results:
#     if result["price"] is not None and result["price"] > 0:
#         city_dict[result["city"]][result["source"]] += 1
#
# print(city_dict)
