from math import sin
import random
from functools import reduce

from generators.generator import Generator
from config import NO_PREFERENCES_PROB, AGE_PREF_FUNCTIONS, GENDER_PREF_FUNCTIONS
from utils.helpers import define_age_range


class CustomerPreferencesGen(Generator):
    # orders_nr, customers_nr, products_nr, stores_nr
    def __init__(self, customers, number_of_departments, number_of_vendors, number_of_categories):
        super().__init__()

        self.customers = customers
        self.number_of_customers = len(customers)
        # self.number_of_departments = number_of_departments
        # self.number_of_vendors = number_of_vendors
        # self.number_of_categories = number_of_categories

        self.departments_shuffled = list(range(1, number_of_departments + 1))
        self.vendors_shuffled = list(range(1, number_of_vendors + 1))
        self.categories_shuffled = list(range(1, number_of_categories + 1))

        random.shuffle(self.departments_shuffled)
        random.shuffle(self.vendors_shuffled)
        random.shuffle(self.categories_shuffled)

    def reveal_general_preferences(self, function, shuffled):
        ls = len(shuffled)
        return list(map(lambda e: (e[1], function(1, e[0], ls)), enumerate(shuffled)))

    def __gen_preferences(self, cid, shuffled):
        slen = len(shuffled)
        cindex = cid - 1

        pref = [(i, random.random()) if random.random() > NO_PREFERENCES_PROB else (i, 0.3) for i in shuffled]
        # pref = [(i, 1) for i in shuffled] # testing using ones (no personal preferences, just global)

        # gender
        gender_pref = self.reveal_general_preferences(GENDER_PREF_FUNCTIONS[self.customers[cindex]['gender']], shuffled)
        # age
        age_pref = self.reveal_general_preferences(AGE_PREF_FUNCTIONS[define_age_range(self.customers[cindex]['age'])], shuffled)
        
        pref = list(map(lambda a, b, c: (a[0], a[1] * b[1] * c[1]), pref, gender_pref, age_pref))

        pref_sum = reduce(lambda x, y: x + y[1], pref, 0)
        pref = list(map(lambda x: (x[0], x[1]/pref_sum), pref))
        pref.sort(key=lambda x: -x[1])
        return pref

    def generate(self):
        self.logger.debug('Generating Customer Preferences')
        preferences = []
        for cid in range(1, self.number_of_customers + 1):
            prob = random.random()
            preferences.append({
                'customerId': cid,
                'departments': self.__gen_preferences(cid, self.departments_shuffled),
                'vendors': self.__gen_preferences(cid, self.vendors_shuffled),
                'categories': self.__gen_preferences(cid, self.categories_shuffled),
                'avgProductsPerOrder': random.randint(5, 20),
                'orderProbNormal': prob * random.random(),
                'orderProbPref': prob,
                'day': random.randint(0, 6)
            })

        return preferences
