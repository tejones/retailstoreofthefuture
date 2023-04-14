# Prediction Service

REST application which outputs coupon redemption predictions

## Table of contents

* [Development](#development)
  * [Dependencies](#dependencies)
  * [Service configuration](#service-configuration)
  * [Running the service](#running-the-service)
* [Prediction example](#prediction-example)
* [Docker image](#docker-image)

## Development

### Dependencies
Dependencies of the project are contained in requirements.txt file. All the packages are publicly available.

All the packages can be installed with:

```shell
pip install -f requirements.txt
```

For development purposes creating a dedicated virtual environment is helpful (Python 3.8, all the dependencies installed there):

```shell
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

```shell
$ . .environment.variables.sh
$ . .venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload
```

## Prediction example


```shell
curl -s -X 'POST' \
  'http://localhost:8000/score' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer":{
    "customer_id":1,
    "gender":"M",
    "age":79,
    "mean_buy_price":11.62,
    "total_coupons_used":285,
    "mean_discount_received":9.16,
    "unique_products_bought":866,
    "unique_products_bought_with_coupons":232,
    "total_items_bought":1102
  },
  "coupons":[
    {
      "coupon_id":7,
      "coupon_type":"buy_all",
      "department":"Boys",
      "discount":49.0,
      "how_many_products_required":3,
      "product_mean_price":8.79,
      "products_available":3,
      "start_date":"2010-01-01",
      "end_date":"2010-01-09"
    },
    {
      "coupon_id":8,
      "coupon_type":"buy_more",
      "department":"Boys",
      "discount":20.0,
      "how_many_products_required":3,
      "product_mean_price":7.44,
      "products_available":1,
      "start_date":"2010-01-01",
      "end_date":"2010-01-12"
    },
    {
      "coupon_id":9,
      "coupon_type":"just_discount",
      "department":"Boys",
      "discount":23.0,
      "how_many_products_required":1,
      "product_mean_price":6.12,
      "products_available":1,
      "start_date":"2010-01-01",
      "end_date":"2010-01-29"
    }
  ]
}' | jq .
```

Example response:

```json
[
  {
    "coupon_id": "8",
    "customer_id": "1",
    "prediction": 0.6108783426
  },
  {
    "coupon_id": "9",
    "customer_id": "1",
    "prediction": 0.5151725303
  },
  {
    "coupon_id": "7",
    "customer_id": "1",
    "prediction": 0.3721197586
  }
]

```

## Docker image
The docker image for the service is [Dockerfile](Dockerfile).
In order to build the image use:

```shell
docker build -t prediction-service:0.0.1 .
```

> Set image name (`prediction-service`) and tag (`0.0.1`) according to
> your needs.

To run the service as a Docker container run:

```shell
docker run -d -p 8000:80 -e LOG_LEVEL="warning" prediction-service:0.0.1
```
