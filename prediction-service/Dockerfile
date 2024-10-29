FROM bitnami/python:3.9

EXPOSE 80

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# the model is supposed to reside in model_path = 'app/model_store/scikit_classifier'
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
