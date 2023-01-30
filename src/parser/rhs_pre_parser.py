import json
import logging
import os

from config import Configuration
from .base_parser import BaseParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("rts_pre_parser.log"),
        logging.StreamHandler(),
    ],
)


class RhsPrePlantsParser(BaseParser):
    def __init__(self):
        super().__init__()

        self.plant_name = None

    def get_how_to_grow_info(self):
        cfg = self.cfg
        how_to_grow_info = {}

        for how_to_element in self.parser.get_elements(cfg.HOW_TO_GROW_KEY):
            how_to_key = self.parser.get_element_attr(value='.//h5', attr='text', find_in=how_to_element)

            if not how_to_key:
                logging.warning(f'<{self.plant_name}> not found HOW_TO_GROW_KEY ({cfg.HOW_TO_GROW_KEY})')
                continue

            how_to_key = how_to_key.lower().replace(' ', '_')
            text_value = self.parser.get_element_attr(value='.//p', attr='text', find_in=how_to_element)

            if not text_value:
                text_value = self.parser.get_elements_attr(value='.//li', attr='text', find_in=how_to_element)

            links = self.parser.get_elements_attr(value='.//p/a', attr='text', find_in=how_to_element)
            href = self.parser.get_elements_attr(value='.//p/a', attr='href', find_in=how_to_element)
            related_links = dict(zip(map(lambda s: s.lower().replace(' ', '_'), links), href))

            links = list(map(lambda s: s.capitalize(), links))
            how_to_grow_info[how_to_key] = {'text': text_value, 'link_names': links, 'related_links': related_links}
        return how_to_grow_info

    def get_parse_data(self):
        cfg = self.cfg
        file_path = Configuration.PARSE_DATA_DIR_PATH

        for number, file_name in enumerate(os.listdir(file_path)):
            if os.path.isfile(os.path.join(file_path, file_name)):
                with open(file_path + file_name, 'r', encoding='UTF-8') as file_data:
                    plant_data = json.load(file_data)

                if plant_data.get('display_name'):
                    continue

                self.plant_name = plant_data["main_name"]

                logging.info(f'<{plant_data["main_name"]}> - processing ({file_name})')
                self.parser.get_url(plant_data['link'])

                plant_data['main_name_original'] = self.parser.get_element_attr(cfg.PLANT_NAME, 'text')
                plant_data['display_name'] = self.parser.get_element_attr(cfg.PLANT_DISPLAY_NAME, 'text').capitalize()

                if plant_data.get('how_to_grow'):
                    plant_data['how_to_grow'] = self.get_how_to_grow_info()

                with open(os.path.join(self.cfg.PARSE_DATA_DIR_PATH, file_name), 'w', encoding='UTF-8') as file:
                    json.dump(plant_data, file, indent=4, ensure_ascii=False)
