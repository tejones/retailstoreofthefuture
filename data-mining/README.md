# Data preparation and training

Dataset source: https://www.kaggle.com/bharath901/amexpert-2019.

This directory contains jupyter notebooks for preparing data and training a model for the coupon recommendation service.

`Coupon_recommendations_01_data_prep.ipynb` - data preparation. This notebook contains data cleaning, feature engineering, as well as merging datasets. It also includes remapping product categories from grocery to clothing store. It requires the original dataset to be present in the `original_data` directory
`Coupon_recommendations_02_training.ipynb` - Training using scikit-learn GradientBoostingClassifier.
`Coupon_recommendations_03_get_customers.ipynb` - Retrieving data for demo - selecting customers which can be used to appropriately demonstrate the recommendation service.

In order to run the jupyter notebooks, use (specify `ip` and `port` according to your needs):
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

jupyter notebook --ip 0.0.0.0 --port 8000 --no-browser
```

The notebooks should be run in the order they are numbered.


## Docker images

This repository contains a Dockerfile for building a docker image. To build it, use:

```
docker build -t coupon-rec:0.0.1 .
```

To run it, use:

```
docker run -it -v 00-data:/00-data -p 0.0.0.0:8002:8000 coupon-rec:0.0.1
```


