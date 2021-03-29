import os
import pickle

import pandas


class Scorer:

    def __init__(self, model):
        self._model = model

    def score(self, input_df: pandas.DataFrame) -> pandas.DataFrame:
        output_df = pandas.DataFrame(input_df[['customer_id', 'coupon_id']])
        input_df.drop(['customer_id', 'coupon_id'], axis=1, inplace=True)
        probs = self._model.predict_proba(input_df)[:, 1]
        output_df['prediction'] = probs.round(decimals=10)
        output_df.sort_values(by='prediction', ascending=False)
        return output_df


def get_scorer():
    model_path = 'app/model_store/scikit_classifier'
    with open(model_path, 'rb') as f:
        return Scorer(pickle.load(f))
