from parser import PtPlantsParser

from models import create_tables
from utils.helpers import parse_jsons_to_db_plants


def main():
    create_tables()
    parse_jsons_to_db_plants()

    pt_parser = PtPlantsParser()
    pt_parser.get_parse_data()


if __name__ == '__main__':
    main()
