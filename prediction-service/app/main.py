from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

# from .encoder import DataEncoder
# from .model import PredictionInput, PredictionOutput
# from .scorer import Scorer, get_scorer
from app.encoder import DataEncoder
from app.model import PredictionInput, PredictionOutput
from app.scorer import Scorer, get_scorer

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


@app.get('/healthcheck')
async def healthcheck() -> Optional[str]:
    return PlainTextResponse('OK')
