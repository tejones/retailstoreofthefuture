# Prediction Service

REST application which outputs coupon redemption predictions



## Development

### Dependencies
Dependencies of the project are contained in requirements.txt file. All the packages are publicly available.

All the packages can be installed with: 
```
pip install -f requirements.txt
```

For development purposes creating a dedicated virtual environment is helpful (Python 3.8, all the dependencies installed there):
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Service configuration
**TBD**

### Running the service
The code reads configuration information (tokens, secrets) from environment variables. They need to be set accordingly in
advance.
`.environment.variables.sh` can be used for that purpose. Then, in order to run the service the following commands can be
used:

```
$ . .environment.variables.sh
$ . .venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload
```

## Prediction example

```
curl -X 'POST' \
  'http://10.91.117.45:8002/score' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer": {
    "customer_id": 54,
    "age": "old",
    "credit": 1,
    "gender": "F",
    "mean_product_price": 13.63,
    "unique_coupons_used": 369,
    "mean_discount_used": 11.93,
    "unique_items_bought": 1934,
    "total_items_bought": 42265
  },
  "coupons": [
    {
      "coupon_id": 1,
      "mean_item_selling_price": 7.06,
      "coupon_discount": 50,
      "category": "",
      "how_many_products": 2,
      "coupon_type": "buy_more",
      "days_valid": 24
    },
    {
      "coupon_id": 2,
      "mean_item_selling_price": 7.06,
      "coupon_discount": 3.78,
      "category": "",
      "how_many_products": 2,
      "coupon_type": "buy_all",
      "days_valid": 20
    }
  ]
}'
```

Example response:

```
[
  {
    "coupon_id": 2,
    "customer_id": 54,
    "prediction": 0.0409353164
  },
  {
    "coupon_id": 1,
    "customer_id": 54,
    "prediction": 0.0311633506
  }
]
```

## Docker image
The docker image for the service is [Dockerfile](Dockerfile).
It is based on FastAPI "official" image. 
See https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker 
for detail on configuring the container (http port, log level, etc.)

In order to build the image use:
```
docker build -t prediction-service:0.0.1 .
```

> Set image name (`prediction-service`) and tag (`0.0.1`) according to
> your needs.

To run the service as a Docker container run:
```
docker run -d -p 8000:80 -e LOG_LEVEL="warning" prediction-service:0.0.1

```
