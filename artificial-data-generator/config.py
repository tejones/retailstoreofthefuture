from math import pi, sin


NAMES_FILE = './generators/data/names.txt'
ORIGINAL_CUSTOMERS = './generators/data/original_data.txt'
ORIGINAL_PRODUCTS = './generators/data/products.txt'
EXPORT_PATH = './generated_data'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

NO_SIZE_TO_SIZE_RATIO = 0.3
MSRP_DIFF_RATIO = 0.5
PRODUCTS_PERCENTAGE_IN_STORE_MIN = 0.3
PRODUCTS_PERCENTAGE_IN_STORE_MAX = 1
NO_PREFERENCES_PROB = 0.7
STORE_HOURS_OPEN = 8

AGE_YOUNG_MID = 35
AGE_MID_OLD = 60

def young_pref_function(x, i, elements):
    e3 = elements / 3
    if i < e3:
        return x * (3 * sin(i * pi / e3) + 1)
    return x

def mid_pref_function(x, i, elements):
    e3 = elements / 3
    if i > e3 and i < 2 * e3:
        return x * (3 * sin((i + e3) * pi / e3) + 1)
    return x

def old_pref_function(x, i, elements):
    e3 = elements / 3
    if i > 2 * e3:
        return x * (3 * sin((i + (2 * e3)) * pi / e3) + 1)
    return x

def women_pref_function(x, i, elements):
    return x * (3 * (i / elements) + 1)

def men_pref_function(x, i, elements):
    return x * (-3 * (i / elements) + 4)

AGE_PREF_FUNCTIONS = {
    f"0-{AGE_YOUNG_MID - 1}": young_pref_function,
    f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": mid_pref_function,
    f"{AGE_MID_OLD}-200": old_pref_function
}

GENDER_PREF_FUNCTIONS = {
    'F': women_pref_function,
    'M': men_pref_function
}
