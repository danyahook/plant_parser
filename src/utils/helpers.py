import typing as t
import json
import logging
import re
from os import listdir
from os.path import isfile, join

import pydantic
import requests

from config import Configuration
from models import PlantNames

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class PtRuResponse(pydantic.BaseModel):
    common_names: list = pydantic.Field([], alias='commonNames')
    synonyms: list = pydantic.Field([])


class PtResponse(pydantic.BaseModel):
    pt_link: str
    filename: str
    latin_name: str = pydantic.Field(..., alias='latinName')
    common_names: t.Optional[list] = pydantic.Field([], alias='commonNames')
    synonyms: t.Optional[list] = pydantic.Field([])
    ru_data: t.Optional[PtRuResponse] = pydantic.Field({})
    rank: t.Optional[int] = pydantic.Field(default=999999)


def clear_text(text: str) -> str:
    clean_pattern = re.compile('<.*?>')
    cleaned_text = re.sub(clean_pattern, '', text)
    return ' '.join(cleaned_text.split())


def get_russian_names(plant_name: str) -> dict:
    ru_response = requests.get(Configuration.PICTURE_THIS_AI_URL.format(search_text=plant_name, language_code='5'))
    if ru_response.status_code != 200:
        return {}

    return {plant_data['latinName']: plant_data for plant_data in ru_response.json()['response']['indexModels']}


def get_pt_plant_url():
    file_path = Configuration.PARSE_DATA_DIR_PATH

    for file_name in listdir(file_path):
        if isfile(join(file_path, file_name)):
            with open(join(file_path, file_name), 'r') as file_data:
                fcc_data = json.load(file_data)
                if plant_name := fcc_data.get('main_name'):
                    response = requests.get(
                        Configuration.PICTURE_THIS_AI_URL.format(search_text=plant_name, language_code='0')
                    )

                    if response.status_code == 200 and (index_models := response.json()['response']['indexModels']):
                        ru_names = get_russian_names(plant_name)

                        for plant_data in index_models:
                            latin_name = plant_data['latinName']
                            pt_link = None

                            if plant_name == latin_name:
                                pt_link = f'https://www.picturethisai.com/wiki/{plant_name.replace(" ", "_")}.html'
                            elif plant_db := PlantNames.get_or_none(plant_name=latin_name):
                                file_name = plant_db.file_name
                                pt_link = f"""https://www.picturethisai.com/wiki/{latin_name.replace(" ", "_").replace("'", "_")}.html"""

                            if pt_link:
                                yield PtResponse(pt_link=pt_link, filename=file_name, ru_data=ru_names.get(latin_name), **plant_data)


def parse_jsons_to_db_plants():
    plants_count = PlantNames.select().count()

    if not plants_count:
        logging.info('====== PARSE JSON TO DB START ======')
        file_path = Configuration.PARSE_DATA_DIR_PATH

        db_data = []
        for number, file_name in enumerate(listdir(file_path)):
            if isfile(join(file_path, file_name)):
                with open(file_path + file_name, 'r') as file_data:
                    plant_data = json.load(file_data)
                    db_data.append({'plant_name': plant_data['main_name'], 'file_name': file_name})
                    file_data.close()
            if number % 10000 == 0:
                PlantNames.insert_many(db_data).execute()
                db_data.clear()
        else:
            PlantNames.insert_many(db_data).execute()
        logging.info('====== PARSE JSON TO DB END ======')
