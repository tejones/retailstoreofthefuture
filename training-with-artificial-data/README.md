# Data preparation and training - artificial data set


This directory contains jupyter notebooks for preparing data and training a model for the coupon recommendation service.

In order to run the Jupyter notebooks, original dataset needs to be present. Path to the directory needs to be specified at the top of each script.

* `01_data_prep.ipynb` - data preparation. This notebook contains data cleaning, merging, feature engineering and encoding. It results in an input dataset for training.

* `02_training_automl.ipynb` - Training using H2O AutoML.

* `03_training.ipynb` - Training model using scikit-learn. Algorithm (GBM) and parameters are selected based on AutoML result. The notebook compares training on unbalanced and balanced dataset.

* `04_demo_data_selection.ipynb` - Using model trained in the previous notebook, select 'good' customer-coupon pairs, i.e. customers for whom there are many 'hit' coupons predicted, along with the 'hit' coupons. Data are saved in a `demo_data` directory. Details can be found in the notebook.

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
docker build -t coupon-rec:0.0.1 . --build-arg DATA_DIR=<path to data dir>
```

To run it, use:

```
docker run -it -p 0.0.0.0:8002:8000 coupon-rec:0.0.1
```


