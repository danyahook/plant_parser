from parser.rhs_parser import rhs_parser

PARSERS = [
    rhs_parser,
]


def main():
    for obj in PARSERS:
        obj.grab_data()


if __name__ == '__main__':
    main()
