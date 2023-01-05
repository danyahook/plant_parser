import os
import json
import logging
from parser.rhs_parser.config import Configuration
from parser.rhs_parser.helpers import clear_text
from parser.selenium_wrapper import ParserSeleniumWrapper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(),
    ],
)


class RhsPlantsParser:
    def __init__(self):
        self.cfg = Configuration()
        self.parser = ParserSeleniumWrapper()

        self.plant_name = None

    def get_other_names_info(self):
        cfg = self.cfg
        names_info = {}

        for names_element in self.parser.get_elements(cfg.PLANT_NAMES):
            name_key = self.parser.get_element_attr(value='.//h6', attr='text', find_in=names_element)

            if not name_key:
                logging.warning(f'<{self.plant_name}> not found PLANT_NAMES (.//h6)')
                continue

            names = self.parser.get_elements_attr(
                value='.//span[@class="ng-star-inserted"]',
                attr='innerHTML',
                find_in=names_element,
            )
            names_info[name_key.lower().replace(' ', '_')] = list(map(clear_text, names))

        return names_info

    def get_plant_size_info(self):
        cfg = self.cfg
        size_info = {}

        for size_element in self.parser.get_elements(cfg.PLANT_SIZE):
            try:
                size_key, size_data = self.parser.get_attr(size_element, 'text').split('\n')
            except ValueError:
                logging.warning(f'<{self.plant_name}> not found PLANT_SIZE ({cfg.PLANT_SIZE})')
                continue

            size_info[size_key.lower().replace(' ', '_')] = size_data

        return size_info

    def get_growing_conditions_info(self):
        cfg = self.cfg
        growing_conditions_info = {'soil': self.parser.get_elements_attr(cfg.SOIL_TYPE_XPATH, attr='text')}

        for soil_element in self.parser.get_elements(cfg.SOIL_PARAMS_KEY):
            soil_key = self.parser.get_element_attr(value='.//h6', attr='text', find_in=soil_element)
            
            if not soil_key:
                logging.warning(f'<{self.plant_name}> not found SOIL_PARAMS_KEY (.//h6)')
                continue

            names = self.parser.get_elements_attr(
                value='.//span[@class="ng-star-inserted"]',
                attr='innerHTML',
                find_in=soil_element,
            )
            growing_conditions_info[soil_key.lower().replace(' ', '_')] = list(
                map(lambda s: s.removesuffix(', '), names)
            )

        return growing_conditions_info

    def get_position_info(self):
        cfg = self.cfg
        position_info = {
            'sun_position': self.parser.get_elements_attr(cfg.SUN_POSITION_XPATH, attr='text'),
            'aspect_position': list(map(
                lambda s: s.removesuffix(' or'), self.parser.get_elements_attr(cfg.ASPECT_POSITION_XPATH, 'text')
            )),
        }

        for position_element in self.parser.get_elements(cfg.ASPECT_PARAMS_KEY):
            try:
                position_key, position_data = self.parser.get_attr(position_element, 'text').split('\n')
            except ValueError:
                logging.warning(f'<{self.plant_name}> not found ASPECT_PARAMS_KEY ({cfg.ASPECT_PARAMS_KEY})')
                continue

            position_info[position_key.lower()] = position_data

        return position_info

    def get_botanical_details_info(self):
        cfg = self.cfg
        botanical_details_info = {}

        for botan_element in self.parser.get_elements(cfg.BOTAN_XPATH):
            try:
                botan_key, botan_data = self.parser.get_attr(botan_element, 'text').split('\n')
            except ValueError:
                logging.warning(f'<{self.plant_name}> not found BOTAN_XPATH ({cfg.BOTAN_XPATH})')
                continue

            botanical_details_info[botan_key.lower().replace(' ', '_')] = botan_data

        return botanical_details_info

    def get_how_to_grow_info(self):
        cfg = self.cfg
        how_to_grow_info = {}

        for how_to_element in self.parser.get_elements(cfg.HOW_TO_GROW_KEY):
            how_to_key = self.parser.get_element_attr(value='.//h5', attr='text', find_in=how_to_element)

            if not how_to_key:
                logging.warning(f'<{self.plant_name}> not found HOW_TO_GROW_KEY ({cfg.HOW_TO_GROW_KEY})')
                continue

            how_to_key = how_to_key.lower().replace(' ', '_')
            if value := self.parser.get_element_attr(
                    value='.//p',
                    attr='text',
                    find_in=how_to_element
            ):
                how_to_grow_info[how_to_key] = value
            elif value := self.parser.get_elements_attr(value='.//li', attr='text', find_in=how_to_element):
                how_to_grow_info[how_to_key] = value

        return how_to_grow_info

    def get_colour_and_scent_info(self):
        cfg = self.cfg
        colour_and_scent_info = {}

        if fragrance_value := self.parser.get_element_attr(value=cfg.FRAGRANCE_XPATH, attr='text'):
            colour_and_scent_info['fragrance'] = fragrance_value.split(': ')[-1]

        for s_number, seasons in enumerate(cfg.COLORS_SEASONS):
            color_types = {}
            for ct_number, color_type in enumerate(cfg.COLORS_ROWS):
                colors = list(map(
                    clear_text,
                    self.parser.get_elements_attr(
                        cfg.QWE_COLOR.format(seasons=s_number + 2, c_type=ct_number + 1), attr='innerHTML'
                    )
                ))
                color_types[color_type] = colors
            colour_and_scent_info[seasons] = color_types

        return colour_and_scent_info

    def grab_data(self):
        cfg = self.cfg

        chunk_size = 0
        processed_chunks = 0

        while True:
            self.parser.get_url(self.cfg.RHS_HOUSEPLANT_URL.format(chunk_size))

            for plant_link in self.parser.get_elements_attr(cfg.PLANT_CARD, 'href'):
                plant_info = {}
                processed_chunks += 1

                self.parser.get_url(plant_link)
                self.plant_name = self.parser.get_element_attr(cfg.PLANT_NAME, 'text')

                file_path = 'parsed_data/' + self.plant_name.replace('/', '_') + '.json'
                if os.path.exists(file_path):
                    logging.info(f'<{self.plant_name}> - already parsed (startFrom={chunk_size})')
                    continue

                if not self.plant_name:
                    logging.warning(f'!!! {plant_link} - NOT FOUND !!!')
                    continue

                logging.info(f'<{self.plant_name}> - processing (startFrom={chunk_size})')

                plant_info['link'] = plant_link
                plant_info['main_name'] = self.plant_name
                plant_info['tags'] = self.parser.get_elements_attr(cfg.PLANT_TAGS, 'text')
                plant_info['names'] = self.get_other_names_info()
                plant_info['size'] = self.get_plant_size_info()
                plant_info['growing_conditions'] = self.get_growing_conditions_info()
                plant_info['colour_and_scent'] = self.get_colour_and_scent_info()
                plant_info['position'] = self.get_position_info()
                plant_info['botanical_details'] = self.get_botanical_details_info()
                plant_info['how_to_grow'] = self.get_how_to_grow_info()

                with open(file_path, 'w', encoding='UTF-8') as fp:
                    json.dump(plant_info, fp, indent=4)

            if chunk_size > processed_chunks:
                break

            chunk_size += 50
