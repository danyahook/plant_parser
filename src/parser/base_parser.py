from abc import ABC

from config import Configuration
from utils.selenium_wrapper import ParserSeleniumWrapper


class BaseParser(ABC):
    def __init__(self):
        self.cfg = Configuration
        self.parser = ParserSeleniumWrapper()

    def get_parse_data(self):
        raise NotImplementedError
