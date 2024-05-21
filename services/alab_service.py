from typing import Union, Set, List
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from database.client import add_analyze
from exceptions.CityException import CityException
from interfaces.click_interface import ClickInterface
from interfaces.scroll_into_Interface import ScrollIntoInterface
from interfaces.ad_interface import AdInterface
from interfaces.cookie_interface import CookieInterface
from interfaces.data_interface import DataInterface
from interfaces.point_interface import PointInterface
from interfaces.select_option_interface import SelectOptionInterface
from interfaces.webdriver_interface import WebdriverInterface
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from models.result_model import Result
from utils.formatting import format_float
from selenium.webdriver import FirefoxOptions

class Alab(CookieInterface, DataInterface, PointInterface,
           AdInterface, WebdriverInterface, ScrollIntoInterface,
           SelectOptionInterface, ClickInterface):
    url: str = "https://sklep.alablaboratoria.pl/?category=Wszystkie+badania#configurator"

    def __init__(self, city: str, thread_status):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts, service=FirefoxService(GeckoDriverManager().install()))
        self.wait = WebDriverWait(driver=self.driver, timeout=15)
        self.city = city
        self.thread_status = thread_status
        self.set_driver_config()
        self.get_page()

    def get_page(self, url="https://sklep.alablaboratoria.pl/?category=Wszystkie+badania#configurator") -> None:
        self.driver.get(url)

    def close_ad_dialog(self) -> None:
        self.click_button_xpath("//span[contains(@class, \"cursor-pointer\")]")

    def set_driver_config(self) -> None:
        pass

    def cookie(self) -> None:
        self.click_button_id("onetrust-accept-btn-handler")

    def get_one_info(self, record: WebElement) -> Result:
        link_item = record.find_element(By.CLASS_NAME, "ns-list-link")
        formatted_price = format_float(record.get_attribute("data-price"))
        status = "not_available"
        if formatted_price is not None and formatted_price > 0:
            status = "online"
        name, price, url = (
            record.get_attribute("data-name"), formatted_price, link_item.get_attribute("href"))
        return Result("Alab", self.city, name, price, url, status)

    def get_set_info(self) -> Union[Set[Result] or List[Result] or None]:
        records = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "examinations-catalog-examination")))
        result: Set[Result] = set()
        for record in records:
            if not self.thread_status:
                break
            result_item: Result = self.get_one_info(record)
            result.add(result_item)
            add_analyze(result_item)
        return result

    def click_button_id(self, id):
        button = self.wait.until(EC.element_to_be_clickable((By.ID, f"{id}")))
        button.click()

    def click_button_xpath(self, xpath):
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"{xpath}")))
        button.click()

    def click_button_class(self, class_name):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, f"{class_name}")))
        button.click()

    def click_element(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def select_option_index(self, element, index) -> None:
        select = Select(element)
        options = select.options
        select.select_by_index(index)

    def select_option_value(self, element: WebElement, value: str) -> None:
        select = Select(element)
        options = select.options
        selected_city = None
        for i, option in enumerate(options):
            if option.text == value:
                selected_city = value
                select.select_by_index(i)
                break
        if selected_city is None:
            raise CityException("CityException")

    def select_point(self) -> None:
        button = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "catalog-select-point-button")))
        self.scroll_into_element(button)
        self.click_element(button)
        # Выбор города
        try:
            city_select_item = self.wait.until(EC.visibility_of_element_located((By.ID, 'shop-location-city')))
            self.select_option_value(city_select_item, self.city)
        except CityException as e:
            raise e

        # Выбор отделения
        shop_select_item = self.wait.until(EC.visibility_of_element_located((By.ID, 'shop-location-punkt')))
        self.select_option_index(shop_select_item, 1)

        self.click_button_id("wybierz-punkt")

    def scroll_into_element(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def close(self) -> None:
        self.driver.close()
