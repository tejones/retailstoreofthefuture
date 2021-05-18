from math import sin
import random
from functools import reduce

from generators.generator import Generator
from config import NO_PREFERENCES_PROB, AGE_PREF_FUNCTIONS, GENDER_PREF_FUNCTIONS, MALE_COUPON_USAGE_PROBABILITY_WEIGHT,\
    FEMALE_COUPON_USAGE_PROBABILITY_WEIGHT, DEPARTMENTS, VENDORS, CATEGORIES, CATEGORIES_UNIQUE
from utils.helpers import define_age_range


class CustomerPreferencesGen(Generator):
    # orders_nr, customers_nr, products_nr, stores_nr
    def __init__(self, customers):
        super().__init__()

        self.customers = customers
        self.number_of_customers = len(customers)

        self.vendors = VENDORS.copy()
        self.categories = CATEGORIES_UNIQUE.copy()

        # random.shuffle(self.departments_shuffled)
        random.shuffle(self.vendors)
        random.shuffle(self.categories)

    def reveal_general_preferences(self, function, shuffled):
        ls = len(shuffled)
        return list(map(lambda e: (e[1], function(1, e[0], ls)), enumerate(shuffled)))

    def __normalize_preferences(self, preferences):
        pref_sum = reduce(lambda x, y: x + y[1], preferences, 0)
        preferences = list(map(lambda x: (x[0], x[1]/pref_sum), preferences))
        preferences.sort(key=lambda x: -x[1])
        return preferences

    def __gen_preferences(self, gender, age_range, shuffled):
        # personal preferences
        personal_pref = [(i, random.randint(60, 100) / 100)\
            if random.random() > NO_PREFERENCES_PROB else (i, 0.8) for i in shuffled]
        # pref = [(i, 1) for i in shuffled] # testing using ones (no personal preferences, just global)

        # gender
        gender_pref = self.reveal_general_preferences(GENDER_PREF_FUNCTIONS[gender], shuffled)
        # age
        age_pref = self.reveal_general_preferences(AGE_PREF_FUNCTIONS[age_range], shuffled)
        
        pref = list(map(lambda a, b, c: (a[0], a[1] * b[1] * c[1]), personal_pref, gender_pref, age_pref))

        return self.__normalize_preferences(pref)

    def __gen_departments_preferences(self, gender, age_range):
        pref = [(d[0] + 1, DEPARTMENTS[d[0]]['probability_of_buing']['gender'][gender] *\
            DEPARTMENTS[d[0]]['probability_of_buing']['age'][age_range]) for d in enumerate(DEPARTMENTS)]

        return self.__normalize_preferences(pref)

    def __coupon_usage_probability(self, gender):
        p = random.random()
        return  (p if p > 0.9 else 0.9) *\
            (MALE_COUPON_USAGE_PROBABILITY_WEIGHT if gender == 'M' else FEMALE_COUPON_USAGE_PROBABILITY_WEIGHT)

    def generate(self):
        self.logger.debug('Generating Customer Preferences')
        preferences = []
        for cindex in range(self.number_of_customers):
            order_prob = random.random()

            gender = self.customers[cindex]['gender']
            age_range = define_age_range(self.customers[cindex]['age'])

            preferences.append({
                'customer_id': cindex + 1,
                'departments': self.__gen_departments_preferences(gender, age_range),
                'vendors': self.__gen_preferences(gender, age_range, self.vendors),
                'categories': self.__gen_preferences(gender, age_range, self.categories),
                'avg_products_per_order': random.randint(2, 10),
                'order_prob_normal': order_prob * random.random(),
                'order_prob_pref': order_prob,
                'day': random.randint(0, 6),
                'coupon_usage_probability': self.__coupon_usage_probability(gender),
            })

        return preferences
