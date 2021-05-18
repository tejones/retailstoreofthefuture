from config import AGE_YOUNG_MID, AGE_MID_OLD


def define_age_range(age):
    if age < AGE_YOUNG_MID:
        return f'0-{AGE_YOUNG_MID - 1}'
    if age < AGE_MID_OLD:
        return f'{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}'
    return f'{AGE_MID_OLD}-200'


def define_age_range_as_nr(age):
    if age < AGE_YOUNG_MID:
        return 1
    if age < AGE_MID_OLD:
        return 2
    return 3
