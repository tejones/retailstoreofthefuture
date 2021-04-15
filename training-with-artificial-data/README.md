# Data preparation and training - artificial data set


This directory contains jupyter notebooks for preparing data and training a model for the coupon recommendation service.

`01_data_prep.ipynb` - data preparation. This notebook contains data cleaning, feature engineering, as well as merging datasets. It requires the original dataset to be present in a directory - oath to the directory is specified at the top of the script.
`02_training_automl.ipynb` - Training using H2O AutoML.
`03_training.ipynb` - Training model using scikit-learn. Algorithm (GBM) and parameters are selected based on AutoML result. The notebook compares training on unbalanced and balanced dataset.

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
docker run -it -p 0.0.0.0:8002:8000 coupon-rec:0.0.1
```


