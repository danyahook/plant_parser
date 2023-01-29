from parser import RhsPrePlantsParser

from models import PlantNames, create_tables
from utils.helpers import parse_jsons_to_db_plants


def main():
    create_tables()
    parse_jsons_to_db_plants()

    rhs_parser = RhsPrePlantsParser()
    rhs_parser.get_parse_data()


if __name__ == '__main__':
    main()
