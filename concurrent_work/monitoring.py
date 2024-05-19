import logging
import threading
import time
from threading import Thread

logger = logging.getLogger("MONITOR")


class Monitoring:

    def __init__(self):
        self.state = threading.Event()
        self.monitor = Thread(target=self.monitor_process, daemon=True)
        self.monitor.start()

    def logger_config(self):
        logging.basicConfig(filename='logs/monitor.log', level=logging.INFO)
        logger.setLevel(level=logging.INFO)

    def monitor_process(self):
        while not self.state.is_set():

            time.sleep(3)

    def stop_monitoring(self):
        self.state.set()

if __name__ == "__main__":
    monitoring = Monitoring()

