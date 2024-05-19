from typing import Union, Set, List

import selenium.common.exceptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from concurrent_work.database.client import client, add_analyze
from interfaces.ad_interface import AdInterface
from interfaces.click_interface import ClickInterface
from interfaces.cookie_interface import CookieInterface
from interfaces.data_interface import DataInterface
from interfaces.pagination_interface import PaginationInterface
from interfaces.point_interface import PointInterface
from interfaces.webdriver_interface import WebdriverInterface
from selenium import webdriver

from models.result_model import Result
from utils.formatting import format_float
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class Diag(WebdriverInterface, CookieInterface, AdInterface,
           ClickInterface, PointInterface, PaginationInterface,
           DataInterface):
    url: str = "https://diag.pl/sklep/badania/wszystkie-kategorie/"

    def __init__(self, city: str, thread_status):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.wait = WebDriverWait(driver=self.driver, timeout=15)
        self.city = city
        self.thread_status = thread_status
        self.set_driver_config()
        self.get_page()

    def get_page(self, url="https://diag.pl/sklep/badania/wszystkie-kategorie/") -> None:
        self.driver.get(url)

    def click_filter(self):
        self.click_button_xpath("//span[text()='Wszystkie badania']")

    def set_driver_config(self) -> None:
        pass

    def cookie(self) -> None:
        self.click_button_xpath("//button[@aria-label=\"accept all and close dialog\"]")

    def select_point(self) -> None:

        self.click_button_xpath("//p[text()='Wybierz swój punkt pobrań']")
        # Выбор города
        self.click_button_id("city")
        cities_element = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//ul[@aria-labelledby=\"city-label\"]")))
        # с9е6
        # city_element = cities_element.find_element(By.XPATH, f".//li[text()=\"{self.city}\"]")
        city_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, f".//li[text()=\"{self.city}\"]")))
        self.click_element(city_element)

        # Выбор отделения
        self.click_button_xpath("//button[text()=\"Wybierz\"]")

    def next_page(self) -> None:
        buttons = self.driver.find_elements(By.CLASS_NAME, "MuiPaginationItem-previousNext")
        if len(buttons) > 1:
            try:
                self.get_page(buttons[-1].find_element(By.XPATH, "..").get_attribute("href"))
            except Exception as e:
                raise AssertionError("End")

    def get_online_price(self, root_element) -> float:
        price_element = root_element.find_element(By.XPATH,
                                                  ".//div[contains(@class, 'MuiTypography-h5') and contains(text(),'PLN')]")
        price_value = price_element.text
        float_value = format_float(price_value)
        return float_value

    def get_offline_price(self, root_element) -> float:
        price_element = root_element.find_element(By.XPATH,
                                                  ".//p[contains(@class, 'MuiTypography-body2') and contains(text(),'PLN')]")
        price_value = price_element.text
        float_value = format_float(price_value)
        return float_value

    def get_innactive_button(self, root_element) -> bool:
        button = root_element.find_element(By.XPATH,
                                           ".//button[contains(@class, 'MuiButton-textPrimary') and contains(text(),'Zmień punkt pobrań')]")
        return button is not None

    def get_one_info(self, record: WebElement) -> List[Result]:
        link_element = record.find_element(By.XPATH, "..")
        root_element = link_element.find_element(By.XPATH, "..")
        result_set: List[Result] = list()
        name, url = (record.find_element(By.CLASS_NAME, "MuiTypography-h5").text,
                     link_element.get_attribute("href"))
        try:
            price_value = self.get_online_price(root_element)
            status = "online"
            result_set.append(Result("Diag", self.city, name, price_value, url, status))
            price_value = self.get_offline_price(root_element)
            status = "offline"
            result_set.append(Result("Diag", self.city, name, price_value, url, status))
        except selenium.common.exceptions.NoSuchElementException as e:
            try:
                if self.get_innactive_button(root_element):
                    price_value: float = 0
                    status: str = "not_available"
                    result_set.append(Result("Diag", self.city, name, price_value, url, status))
            except selenium.common.exceptions.NoSuchElementException:
                price_value = 0
                status = "offline_only"
                result_set.append(Result("Diag", self.city, name, price_value, url, status))

        return result_set

    def get_set_info(self) -> Union[Set[Result] or List[Result] or None]:
        pagination: bool = True
        result: Set[Result] = set()
        while pagination and self.thread_status:
            records = self.wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "MuiCardContent-root")))
            for record in records:
                record_result: Set[Result] = set(self.get_one_info(record))
                for item in record_result:
                    add_analyze(item)
                result.update(result)
            try:
                self.next_page()
            except AssertionError:
                pagination = False
        return result

    def close_ad_dialog(self) -> None:
        pass

    def click_button_id(self, id):
        button = self.wait.until(EC.element_to_be_clickable((By.ID, f"{id}")))
        self.click_element(button)

    def click_button_xpath(self, xpath):
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"{xpath}")))
        self.click_element(button)

    def click_button_class(self, class_name):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, f"{class_name}")))
        self.click_element(button)

    def click_element(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def close(self) -> None:
        self.driver.close()
