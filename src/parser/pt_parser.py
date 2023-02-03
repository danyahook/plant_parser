import json
import logging
from os.path import join

from selenium.webdriver.common.by import By

from utils.helpers import get_pt_plant_url

from .base_parser import BaseParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pt_parser.log"),
        logging.StreamHandler(),
    ],
)


class PtPlantsParser(BaseParser):
    def __init__(self):
        super().__init__()

    def get_head_items(self) -> dict:
        cfg = self.cfg
        head_item_data = {}

        for head_item in self.parser.get_elements(cfg.HEAD_ITEMS_CLASS_NAME, By.CLASS_NAME):
            if head_key := self.parser.get_element_attr(
                value=cfg.HEAD_ITEMS_CLASS_NAME_TEXT,
                find_type=By.CLASS_NAME,
                attr='text',
                find_in=head_item,
            ):
                head_key = head_key.lower().replace(' ', '_')
                head_value = self.parser.get_element_attr(
                    value=cfg.HEAD_ITEMS_CLASS_NAME_TITLE,
                    find_type=By.CLASS_NAME,
                    attr='text',
                    find_in=head_item,
                )
                if ', ' in head_value:
                    head_value = head_value.split(', ')
                head_item_data[head_key] = head_value
        return head_item_data

    def get_care_items(self) -> dict:
        cfg = self.cfg
        care_item_data = {}

        for care_item in self.parser.get_elements(cfg.CARE_ITEMS_CLASS_NAME, By.CLASS_NAME):
            if care_key := self.parser.get_element_attr(
                value=cfg.CARE_ITEMS_CLASS_NAME_TITLE,
                find_type=By.CLASS_NAME,
                attr='text',
                find_in=care_item,
            ):
                care_key = care_key.lower().replace(' ', '_')
                care_value = self.parser.get_element_attr(
                    value=cfg.CARE_ITEMS_CLASS_NAME_TEXT,
                    find_type=By.CLASS_NAME,
                    attr='text',
                    find_in=care_item,
                )
                if ', ' in care_value:
                    care_value = care_value.split(', ')
                care_item_data[care_key] = care_value
        return care_item_data

    def get_scientific_classification(self) -> dict:
        cfg = self.cfg
        class_data = {}

        for class_item in self.parser.get_elements(cfg.CLASS_ITEMS, By.CLASS_NAME):
            if class_key := self.parser.get_element_attr(
                value='.//div',
                attr='text',
                find_in=class_item,
            ):
                class_key = class_key.lower().replace(' ', '_')
                class_value = self.parser.get_element_attr(
                    value='.//a',
                    attr='text',
                    find_in=class_item,
                )
                if class_key == 'order':
                    class_value = [
                        class_value_item.capitalize()
                        for class_value_item in class_value.replace(', ', '@').replace(' and ', '@').split('@')
                    ]
                class_data[class_key] = class_value
        return class_data

    def get_toxic_data(self) -> list:
        cfg = self.cfg
        return list(map(lambda s: s.strip(), self.parser.get_elements_attr(cfg.TOXIC_ITEM, 'innerHTML', By.CLASS_NAME)))

    def get_common_pests_and_diseases(self):
        cfg = self.cfg
        return list(set(filter(None, self.parser.get_elements_attr(cfg.DISEASES_ITEM, 'text', By.CLASS_NAME))))

    def get_parse_data(self):
        for plant_data in get_pt_plant_url():
            self.parser.get_url(plant_data.pt_link)
            logging.info(f'<{plant_data.latin_name}> - processing ({plant_data.filename})')

            pt_data = plant_data.dict()

            items_data = self.get_head_items()
            items_data.update(self.get_care_items())

            pt_data['items_data'] = items_data
            pt_data['class_data'] = self.get_scientific_classification()
            pt_data['toxic_data'] = self.get_toxic_data()
            pt_data['diseases_data'] = self.get_common_pests_and_diseases()

            with open(join(self.cfg.PARSE_DATA_DIR_PATH, plant_data.filename), 'r', encoding='UTF-8') as file:
                file_data = json.load(file)

            file_data['pt_data'] = pt_data

            with open(join(self.cfg.PARSE_DATA_DIR_PATH, plant_data.filename), 'w', encoding='UTF-8') as file:
                json.dump(file_data, file, indent=4, ensure_ascii=False)
        logging.info('====== PARSE COMPETED ======')
