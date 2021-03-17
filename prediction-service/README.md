# Prediction Service

REST application which outputs coupon redemption predictions


## Install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```
uvicorn --host <host, e.g. 0.0.0.0> --port <port, e.g. 8001> app.main:app --reload
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


