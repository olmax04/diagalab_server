import threading
import time
from threading import Thread

from database.client import get_cities_alab, get_cities_diag, log_message, create_source_log, update_source_log
from services.alab_service import Alab
from services.diag_service import Diag


class Server:

    def __init__(self):
        self.alab_thread: Thread = None
        self.diag_thread: Thread = None
        self.alab_object: Alab = None
        self.diag_object: Diag = None
        self.diag_status: bool = False
        self.alab_status: bool = False

    def alab_work(self):
        cities = get_cities_alab()
        for city in cities:
            if self.alab_status:
                self.alab_object = Alab(city.city, self.alab_status)
                create_source_log(city=city.city, source="Alab")
                try:
                    self.alab_object.cookie()
                    self.alab_object.select_point()
                    self.alab_object.get_page()
                    self.alab_object.get_set_info()
                except Exception as e:
                    print(e)
                    log_message(f"Alab error: {e}")
                finally:
                    update_source_log(city=city.city, source="Alab")
                    self.alab_object.close()
        log_message(f"Alab parsing completed")
        self.alab_object = None
        self.alab_thread = None

    def diag_work(self):
        cities = get_cities_diag()
        for city in cities:
            if self.diag_status:
                self.diag_object = Diag(city.city, self.diag_status)
                create_source_log(city=city.city, source="Diag")
                try:
                    self.diag_object.cookie()
                    self.diag_object.click_filter()
                    self.diag_object.select_point()
                    self.diag_object.get_set_info()
                except Exception as e:
                    print(e)
                    log_message(f"Diag error: {e}")
                finally:
                    update_source_log(city=city.city, source="Diag")
                    self.diag_object.close()
        log_message(f"Diag parsing completed")
        self.diag_object = None
        self.diag_thread = None


    def start_alab(self):
        if self.alab_thread is None:
            self.alab_status = True
            self.alab_thread = Thread(target=self.alab_work)
            self.alab_thread.start()
            log_message("Alab Process started")
            return 200
        return 409

    def start_diag(self):
        if self.diag_thread is None:
            self.diag_status = True
            self.diag_thread = Thread(target=self.diag_work)
            self.diag_thread.start()
            log_message("Diag Process Started")
            return 200
        return 409

    def stop_diag(self):
        if self.diag_thread is not None:
            self.diag_status = False
            self.diag_object.thread_status = False
            log_message("Diag Process stopping")
            self.diag_thread.join()
            self.diag_thread = None
            log_message("Diag Process stopped")
            return 200
        else:
            self.diag_thread = None
            self.diag_object = None
            log_message("Diag Process stopped")
            return 200

    def stop_alab(self):
        if self.alab_thread is not None:
            self.alab_status = False
            self.alab_object.thread_status = False
            log_message("Alab Process stopping")
            self.alab_thread.join()
            self.alab_thread = None
            log_message("Alab Process stopped")
            return 200
        else:
            self.alab_thread = None
            self.alab_object = None
            log_message("Alab Process stopped")
            return 200

