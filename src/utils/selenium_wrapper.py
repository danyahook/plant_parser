import typing as t

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class ParserSeleniumWrapper(object):

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--start-maximized')

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

    def get_url(self, url: str) -> None:
        return self.driver.get(url)

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_elements(self, value: str, find_type: By = By.XPATH) -> list[WebElement]:
        return self.driver.find_elements(by=find_type, value=value)

    def get_element(self, value: str, find_type: By = By.XPATH, element_index=0, default=None) -> t.Optional[WebElement]:
        try:
            element = self.driver.find_elements(by=find_type, value=value)[element_index]
        except IndexError:
            return default
        return element

    @staticmethod
    def get_attr(element: WebElement, attr: t.Literal['text', 'href', 'innerHTML']):
        return element.text if attr == 'text' else element.get_attribute(attr)

    def get_element_attr(
            self,
            value: str,
            attr: t.Literal['text', 'href', 'innerHTML'],
            find_type: By = By.XPATH,
            element_index: int = 0,
            find_in: t.Optional[WebElement] = None,
            default: t.Any = None
    ) -> str:
        driver = find_in or self.driver

        try:
            element = driver.find_elements(by=find_type, value=value)[element_index]
        except IndexError:
            return default

        return self.get_attr(element, attr)

    def get_elements_attr(
            self,
            value: str,
            attr: t.Literal['text', 'href', 'innerHTML'],
            find_type: By = By.XPATH,
            find_in: t.Optional[WebElement] = None
    ) -> list[str]:
        driver = find_in or self.driver

        return [self.get_attr(element, attr) for element in driver.find_elements(by=find_type, value=value)]
