from typing import List

from fastapi import Depends, FastAPI

from .encoder import DataEncoder
from .model import PredictionInput, PredictionOutput
from .scorer import Scorer, get_scorer


app = FastAPI(
    title='Prediction Service'
)


@app.post('/score', response_model=List[PredictionOutput])
def score_coupon(
    input_data: PredictionInput,
    scorer: Scorer = Depends(get_scorer)
):
    input_df = DataEncoder.encode(input_data)
    output_df = scorer.score(input_df)

    return [PredictionOutput(**row) for row in output_df.to_dict(orient='index').values()]

