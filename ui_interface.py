import tkinter as tk
from tkinter import filedialog

from models.result_model import Result
from services.alab_service import Alab
from services.diag_service import Diag
from controllers.excel_controller import *


class UIInterface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.filename = None
        self.update_value = None
        self.master = master
        self.cities: List[str] or None = list()
        self.result: List[Result] or None = list()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self)
        self.load_button["text"] = "Загрузить файл"
        self.load_button["command"] = self.load_file
        self.load_button.pack(side="top")

        self.start_button = tk.Button(self)
        self.start_button["text"] = "Запуск"
        self.start_button["command"] = self.start_loading
        self.start_button['state'] = "disabled"
        self.start_button.pack(side="top")

        self.export_result_button = tk.Button(self)
        self.export_result_button["text"] = "Экспорт результатов"
        self.export_result_button["command"] = self.export_result
        self.export_result_button["state"] = "disabled"
        self.export_result_button.pack(side="top")

        self.export_logs_button = tk.Button(self)
        self.export_logs_button["text"] = "Экспорт логов"
        self.export_logs_button["command"] = self.export_logs
        self.export_logs_button["state"] = "disabled"
        self.export_logs_button.pack(side="top")

    def load_file(self):
        self.filename = filedialog.askopenfilename()
        self.cities = read_cities(self.filename)
        self.update_value = len(self.cities) / 2 / 10
        self.start_button['state'] = "normal"

    def alab_process(self, city: str) -> None:
        alab = Alab(city)
        alab.cookie()
        alab.select_point()
        alab.get_page()
        self.result += alab.get_set_info()
        alab.close()

    def diag_process(self, city: str) -> None:
        diag = Diag(city)
        diag.cookie()
        diag.click_filter()
        diag.select_point()
        self.result += diag.get_set_info()
        diag.close()

    def start_loading(self):
        for city in self.cities:
            self.alab_process(city)
        for city in self.cities:
            self.diag_process(city)
        self.start_button["state"] = "disabled"
        self.export_result_button["state"] = "normal"
        self.export_logs_button["state"] = "normal"

    def export_result(self):
        export_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                       filetypes=(("Excel", "*.xlsx"), ("All Files", "*.*"),))
        assert export_filename, "Filename not provided"
        create_result_document(result=self.result, filename=export_filename)

    def export_logs(self):
        export_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                       filetypes=(("Excel", "*.xlsx"), ("All Files", "*.*"),))
        assert export_filename, "Filename not provided"
        create_log_document(result=self.result, cities=self.cities,
                            filename=export_filename)
