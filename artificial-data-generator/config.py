import os
from math import pi, sin


NAMES_FILE = './generators/data/names.txt'
ORIGINAL_CUSTOMERS = './generators/data/original_data.txt'
ORIGINAL_PRODUCTS = './generators/data/products.txt'
EXPORT_PATH = './generated_data'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEVELOPMENT = os.getenv('DEVELOPMENT', 'false')
DEVELOPMENT = DEVELOPMENT.lower() in ['true', 't', 'y', '1', 'ano', 'tak', 'da', 'naturlich']

NO_SIZE_TO_SIZE_RATIO = 0.3
PRODUCTS_PERCENTAGE_IN_STORE_MIN = 0.3
PRODUCTS_PERCENTAGE_IN_STORE_MAX = 1
NO_PREFERENCES_PROB = 0.8
STORE_OPEN_HOURS = 8

AGE_YOUNG_MID = 35
AGE_MID_OLD = 60

VENDORS = [
    'Bellerose', 'Adidas', 'Polo', 'Hugo Boss', 'Nununu', 'Gap',
    'Puma', 'J.Crew', 'Fred Perry', 'Aeropostale', 'Guess', 'Nike',
    'Gymboree', 'Acrylick', 'Prada', 'Lacoste', 'CLSC', 'Converse',
    'Gucci', 'H & M', 'TinyCottons', 'Calvin Klein', 'Chanel', 'Izod',
    'Diesel', 'Armani', 'ZARA', 'Carhartt', 'Versace', 'Dior', 'Levis'
]

SIZES = ['XS-XXL', 'S-XL', 'S-L', '22-44', '28-38', '32-48', '28-48', 'one-size']

CATEGORIES = {
    'Women': ['Rain jacket', 'Skirt', 'Tank top', 'Wool hat', 'Sweat pants',
            'Dress pants', 'Beach sling', 'Denim cut-offs', 'Short sleeve Henley',
            'Short sleeve polo', 'Overalls', 'V-neck t-shirt', 'Bucket hat',
            'Cotton oxford', 'Romper', 'Skinny jean', 'Suspenders', 'Hawaiian shirt', 'Bathrobe',
            'Sweatshirt', 'Pajama pants', 'Jeans', 'Flannel shirt', 'Onesy', 'Vest top',
            'Cargo short', 'Dress socks', 'T-shirt', 'Dress'
        ],
    'Men': ['Rain jacket', 'Tank top', 'Wool hat', 'Sweat pants',
            'Dress pants', 'Beach sling', 'Denim cut-offs', 'Short sleeve Henley',
            'Short sleeve polo', 'Overalls', 'V-neck t-shirt', 'Bucket hat',
            'Cotton oxford', 'Romper', 'Skinny jean', 'Suspenders', 'Hawaiian shirt', 'Bathrobe',
            'Sweatshirt', 'Pajama pants', 'Jeans', 'Flannel shirt', 'Onesy', 'Vest top',
            'Cargo short', 'Dress socks', 'T-shirt', 'Tuxedo'
        ],
    'Girls': ['Rain jacket', 'Skirt', 'Tank top', 'Wool hat', 'Sweat pants',
            'Dress pants', 'Beach sling', 'Denim cut-offs', 'Short sleeve Henley',
            'Short sleeve polo', 'Overalls', 'V-neck t-shirt', 'Bucket hat',
            'Cotton oxford', 'Romper', 'Skinny jean', 'Suspenders', 'Hawaiian shirt', 'Bathrobe',
            'Sweatshirt', 'Pajama pants', 'Jeans', 'Flannel shirt', 'Onesy', 'Vest top',
            'Cargo short', 'Dress socks', 'T-shirt', 'Dress'
        ],
    'Boys': ['Rain jacket', 'Tank top', 'Wool hat', 'Sweat pants',
            'Dress pants', 'Beach sling', 'Denim cut-offs', 'Short sleeve Henley',
            'Short sleeve polo', 'Overalls', 'V-neck t-shirt', 'Bucket hat',
            'Cotton oxford', 'Romper', 'Skinny jean', 'Suspenders', 'Hawaiian shirt', 'Bathrobe',
            'Sweatshirt', 'Pajama pants', 'Jeans', 'Flannel shirt', 'Onesy', 'Vest top',
            'Cargo short', 'Dress socks', 'T-shirt', 'Tuxedo'
        ],
    'Sport': ['Bathing suit', 'Bike short', 'Sport briefs', 'Sport jacket',
            'Tenis skirt', 'Sport pants', 'Sport shorts', 'Swim trunk',
            'Yoga skort', 'Sport coat', 'Backpack', 'Sport shoes'
        ]
}

from functools import reduce
CATEGORIES_UNIQUE = list(set(reduce(lambda a, b: a + b, [c for k, c in CATEGORIES.items()])))

COLORS = [ # colors from https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F
    'Absolute Zero', 'Acid green', 'Aero', 'Aero blue', 'African violet', 'Air superiority blue', 'Alabaster',
    'Alice blue', 'Alloy orange', 'Almond', 'Amaranth', 'Amaranth (M&P)', 'Amaranth pink', 'Amaranth purple',
    'Amaranth red', 'Amazon', 'Amber', 'Amber (SAE/ECE)', 'Amethyst', 'Android green', 'Antique brass',
    'Antique bronze', 'Antique fuchsia', 'Antique ruby', 'Antique white', 'Ao (English)', 'Apple green',
    'Apricot', 'Aqua', 'Aquamarine', 'Arctic lime', 'Army green', 'Artichoke', 'Arylide yellow', 'Ash gray',
    'Asparagus', 'Atomic tangerine', 'Auburn', 'Aureolin', 'Avocado', 'Azure', 'Azure (X11/web color)',
    'Baby blue', 'Baby blue eyes', 'Baby pink', 'Baby powder', 'Baker-Miller pink', 'Banana Mania', 'Barbie Pink',
    'Barn red', 'Battleship grey', 'Beau blue', 'Beaver', 'Beige', 'B\'dazzled blue', 'Big dip o’ruby', 'Bisque',
    'Bistre', 'Bistre brown', 'Bitter lemon', 'Bitter lime', 'Bittersweet', 'Bittersweet shimmer', 'Black',
    'Black bean', 'Black chocolate', 'Black coffee', 'Black coral', 'Black olive', 'Black Shadows',
    'Blanched almond', 'Blast-off bronze', 'Bleu de France', 'Blizzard blue', 'Blond', 'Blood red', 'Blue',
    'Blue (Crayola)', 'Blue (Munsell)', 'Blue (NCS)', 'Blue (Pantone)', 'Blue (pigment)', 'Blue (RYB)', 'Blue bell',
    'Blue-gray', 'Blue-green', 'Blue-green (color wheel)', 'Blue jeans', 'Blue sapphire', 'Blue-violet',
    'Blue-violet (Crayola)', 'Blue-violet (color wheel)', 'Blue yonder', 'Bluetiful', 'Blush', 'Bole', 'Bone',
    'Bottle green', 'Brandy', 'Brick red', 'Bright green', 'Bright lilac', 'Bright maroon', 'Bright navy blue',
    'Bright yellow (Crayola)', 'Brilliant rose', 'Brink pink', 'British racing green', 'Bronze', 'Brown', 'Brown sugar',
    'Brunswick green', 'Bud green', 'Buff', 'Burgundy', 'Burlywood', 'Burnished brown', 'Burnt orange', 'Burnt sienna',
    'Burnt umber', 'Byzantine', 'Byzantium', 'Cadet', 'Cadet blue', 'Cadet blue (Crayola)', 'Cadet grey',
    'Cadmium green', 'Cadmium orange', 'Cadmium red', 'Cadmium yellow', 'Café au lait', 'Café noir',
    'Cambridge blue', 'Camel', 'Cameo pink', 'Canary', 'Canary yellow', 'Candy apple red', 'Candy pink',
    'Capri', 'Caput mortuum', 'Cardinal', 'Caribbean green', 'Carmine', 'Carmine (M&P)', 'Carnation pink',
    'Carnelian', 'Carolina blue', 'Carrot orange', 'Castleton green', 'Catawba', 'Cedar Chest', 'Celadon',
    'Celadon blue', 'Celadon green', 'Celeste', 'Celtic blue', 'Cerise', 'Cerulean', 'Cerulean blue', 'Cerulean frost',
    'Cerulean (Crayola)', 'CG blue', 'CG red', 'Champagne', 'Champagne pink', 'Charcoal', 'Charleston green',
    'Charm pink', 'Chartreuse (traditional)', 'Chartreuse (web)', 'Cherry blossom pink', 'Chestnut', 'Chili red',
    'China pink', 'China rose', 'Chinese red', 'Chinese violet', 'Chinese yellow', 'Chocolate (traditional)',
    'Chocolate (web)', 'Chocolate Cosmos', 'Chrome yellow', 'Cinereous', 'Cinnabar', 'Cinnamon Satin', 'Citrine',
    'Citron', 'Claret', 'Cobalt blue', 'Cocoa brown', 'Coffee', 'Columbia Blue', 'Congo pink', 'Cool grey', 'Copper',
    'Copper (Crayola)', 'Copper penny', 'Copper red', 'Copper rose', 'Coquelicot', 'Coral', 'Coral pink', 'Cordovan',
    'Corn', 'Cornell red', 'Cornflower blue', 'Cornsilk', 'Cosmic cobalt', 'Cosmic latte', 'Coyote brown', 'Cotton candy',
    'Cream', 'Crimson', 'Crimson (UA)', 'Crystal', 'Cultured', 'Cyan', 'Cyan (process)', 'Cyber grape', 'Cyber yellow',
    'Cyclamen', 'Dark blue-gray', 'Dark brown', 'Dark byzantium', 'Dark cornflower blue', 'Dark cyan', 'Dark electric blue',
    'Dark goldenrod', 'Dark green', 'Dark green (X11)', 'Dark jungle green', 'Dark khaki', 'Dark lava', 
    'Dark magenta', 'Dark moss green', 'Dark olive green', 'Dark orange', 'Dark orchid', 'Dark pastel green', 'Dark purple',
    'Dark red', 'Dark salmon', 'Dark sea green', 'Dark sienna', 'Dark sky blue', 'Dark slate blue', 'Dark slate gray',
    'Dark spring green', 'Dark turquoise', 'Dark violet', 'Dartmouth green', 'Davy\'s grey', 'Deep cerise', 'Deep champagne',
    'Deep chestnut', 'Deep jungle green', 'Deep pink', 'Deep saffron', 'Deep sky blue', 'Deep Space Sparkle', 'Deep taupe',
    'Denim', 'Denim blue', 'Desert', 'Desert sand', 'Dim gray', 'Dodger blue', 'Dogwood rose', 'Drab', 'Duke blue',
    'Dutch white', 'Earth yellow', 'Ebony', 'Ecru', 'Eerie black', 'Eggplant', 'Eggshell', 'Egyptian blue', 'Eigengrau',
    'Electric blue', 'Electric green', 'Electric indigo', 'Electric lime', 'Electric purple', 'Electric violet', 'Emerald',
    'Eminence', 'English green', 'English lavender', 'English red', 'English vermillion', 'English violet', 'Erin',
    'Eton blue', 'Fallow', 'Falu red', 'Fandango', 'Fandango pink', 'Fashion fuchsia', 'Fawn', 'Feldgrau', 'Fern green',
    'Field drab', 'Fiery rose', 'Firebrick', 'Fire engine red', 'Fire opal', 'Flame', 'Flax', 'Flirt', 'Floral white',
    'Fluorescent blue', 'Forest green (Crayola)', 'Forest green (traditional)', 'Forest green (web)', 'French beige',
    'French bistre', 'French blue', 'French fuchsia', 'French lilac', 'French lime', 'French mauve', 'French pink',
    'French raspberry', 'French rose', 'French sky blue', 'French violet', 'Frostbite', 'Fuchsia', 'Fuchsia (Crayola)',
    'Fuchsia purple', 'Fuchsia rose', 'Fulvous', 'Fuzzy Wuzzy']

DEPARTMENTS = [
    {
        'name': 'Men',
        'probability_of_buing': {
            'gender': {'M': 1, 'F': 0.7},
            'age': {
                f"0-{AGE_YOUNG_MID - 1}": 1,
                f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": 0.9,
                f"{AGE_MID_OLD}-200": 0.8
            },
        },
        'department_size': 0.3
    },
    {
        'name': 'Sport',
        'probability_of_buing': {
            'gender': {'M': 1, 'F': 1},
            'age': {
                f"0-{AGE_YOUNG_MID - 1}": 1,
                f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": 0.8,
                f"{AGE_MID_OLD}-200": 0.6
            },
        },
        'department_size': 0.1
    },
    {
        'name': 'Boys',
        'probability_of_buing': {
            'gender': {'M': 0.8, 'F': 1},
            'age': {
                f"0-{AGE_YOUNG_MID - 1}": 0.7,
                f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": 0.6,
                f"{AGE_MID_OLD}-200": 0.2
            },
        },
        'department_size': 0.05
    },
    {
        'name': 'Girls',
        'probability_of_buing': {
            'gender': {'M': 1, 'F': 0.8},
            'age': {
                f"0-{AGE_YOUNG_MID - 1}": 0.4,
                f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": 0.6,
                f"{AGE_MID_OLD}-200": 0.2
            },
        },
        'department_size': 0.05
    },
    {
        'name': 'Women',
        'probability_of_buing': {
            'gender': {'M': 0.6, 'F': 1},
            'age': {
                f"0-{AGE_YOUNG_MID - 1}": 0.1,
                f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}": 1,
                f"{AGE_MID_OLD}-200": 0.9
            },
        },
        'department_size': 0.5
    }
]

assert sum([d['department_size'] for d in DEPARTMENTS]) == 1

COUPON_TYPES = {
    'department': {
        'min_discount_percentage': 5,
        'max_discount_percentage': 70,
        'probability_of_usage': 0.9,
        'gen_coupons': True
    },
    'just_discount': {
        'min_discount_percentage': 5,
        'max_discount_percentage': 30,
        'probability_of_usage': 0.95,
        'gen_coupons': True
    },
    'buy_all': {
        'min_discount_percentage': 5,
        'max_discount_percentage': 70,
        'min_products': 2,
        'max_products': 5,
        'probability_of_usage': 0.5,
        'gen_coupons': True
    },
    'buy_more': {
        'min_discount_percentage': 10,
        'max_discount_percentage': 50,
        'min_products': 2,
        'max_products': 5,
        'probability_of_usage': 0.7,
        'gen_coupons': True
    }
}

COUPONS_PER_DEPARTMENT = 5

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

MALE_COUPON_USAGE_PROBABILITY_WEIGHT = 0.8
FEMALE_COUPON_USAGE_PROBABILITY_WEIGHT = 0.9
