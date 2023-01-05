class Configuration:
    RHS_SEARCH_URL = 'https://www.rhs.org.uk/search?query={}'
    RHS_HOUSEPLANT_URL = 'https://www.rhs.org.uk/plants/search-results?form-mode=true&plantTypes={plant_type}&pageSize=50&startFrom={start_from}'

    COLORS_ROWS = ('stem', 'flower', 'foliage', 'fruit')
    COLORS_SEASONS = ('spring', 'summer', 'autumn', 'winter')

    PLANT_CARD = '/html/body/div/div/app-root/app-plant-search-result-page/app-plant-listing/div/div/div/div[2]/app-plant-search-list/ul/li/app-plants-search-list-item/div/a'

    PLANT_TAGS = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[1]/div/div[2]/div/span'
    PLANT_NAME = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[2]/div/div[1]/div[1]/div/h1/span'
    PLANT_NAMES = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div'

    PLANT_SIZE = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]'
    SEARCH_FIRST_PLANT_XPATH = '/html/body/form/div[3]/div[4]/div[4]/div[1]/div[1]/section/div/div/div[3]/div/div[1]/div/div[1]/div/div/a'

    SOIL_TYPE_XPATH = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div/div[2]'
    SOIL_PARAMS_KEY = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[2]/div[2]/div[2]/div/div'

    SUN_POSITION_XPATH = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[4]/div[2]/ul/li/div/div[2]'
    ASPECT_POSITION_XPATH = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[4]/div[2]/p/span'
    ASPECT_PARAMS_KEY = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[4]/div[2]/div/div/div'

    BOTAN_XPATH = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[2]/div/div/div[1]/div/div/div/div[2]/div/dl/span'

    HOW_TO_GROW_KEY = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[3]/div/div/div/div[1]/div/span'
    COLOUR_SCENT = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[2]/table/tr[2]/td/'

    PLANT_COMMON_INFO = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[2]/div/div[1]/div[1]/div/p'
    PLANT_COMMON_NAME = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[2]/div/div[1]/div[1]/div/p[1]'
    PLANT_SUMMARY = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[2]/div/div[1]/div[1]/div/p[2]'
    PLANT_SIZE_ELEMENTS = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[1]/div[2]/div'
    PLANT_SUB_SIZE = './/div/div/div/div[2]'

    FRAGRANCE_XPATH = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[1]/div[1]/div[2]/div'
    COLOR_TYPES_TABLE = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[2]/table/tr[1]/td[position() > 1]'
    COLOR_TABLE = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[2]/table/tr[{}]/td/span/span[2]'
    COLOR_COLUMNS_TABLE = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[2]/table/tr/th'

    QWE_COLOR = '/html/body/div/div/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div/div[3]/div/div[3]/div[2]/table/tr[{seasons}]/td[{c_type}]/span/span[2]'