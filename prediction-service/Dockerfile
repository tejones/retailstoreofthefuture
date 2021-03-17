FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app/app
# the model is supposed to reside in model_path = 'app/model_store/scikit_classifier'