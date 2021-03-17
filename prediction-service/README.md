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
    "customer_id": 4444,
    "age_range": "46-55",
    "marital_status": "Married",
    "family_size": 5,
    "no_of_children": 3,
    "income_bracket": 3,
    "gender": "M",
    "mean_discount_used": -1.83,
    "total_discount_used": -7548.79,
    "total_unique_items_bought": 2040,
    "total_quantity_bought": 4314,
    "mean_quantity_bought": 1.04,
    "mean_selling_price_paid": 61.27,
    "total_coupons_redeemed": 220,
    "total_price_paid": 253295.6
  },
  "coupons": [
    {
      "coupon_id": 1111,
      "item_selling_price": 70.88,
      "coupon_discount": -35.62,
      "item_category": "Men"
    },
    {
      "coupon_id": 2323,
      "item_selling_price": 75.51,
      "coupon_discount": -26.71,
      "item_category": "Sport"
    }
  ]
}'
```

Example response:

```
[
  {
    "coupon_id": 1111,
    "customer_id": 4444,
    "prediction": 1
  },
  {
    "coupon_id": 2323,
    "customer_id": 4444,
    "prediction": 1
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
