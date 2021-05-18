# Retail Store of the Future

Disclaimer! This solution was created for demo purposes only. It contains simplifications and must not be used for production purposes!

## Solution diagram and components description

![Solution basic diagram](documentation/images/basic_diagram.png)

### Training

The training part is made in the jupyter notebooks using Intel DAAL libraries.

### Prediction service

Prediction service handles the model.

It provides a REST API that can be called to retrieve predictions for coupons.

Check [Prediction service README](prediction-service/README.md) for details.

### Recommendation service

Recommendation service listens for MQTT requests.

When the entry event occurs it calls (TODO) the central resource for client data. The component stores the data in a cache - database (TODO).

When the focus event occurs the component gets client and coupon data from the cache (TODO) and calls prediction service.
The result of the prediction is pushed to MQTT.

Check [Recommendation service README](recommendation-service/README.md) for details.
MQTT topics description and schema can also be found there.

### Visualization app

The application was made for demo purposes. [More details int app's README](visualization-app/README.md).

### Customers simulator

This simulator was made for demo purposes. See more details in the [README file](scenario-player/README.md)
