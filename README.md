# retailstoreofthefuture

## Solution diagram and components description

![Solution basic diagram](documentation/images/basic_diagram.png)

### Prediction service

Prediction service handles the model.

It provides a REST API that can be called to retrieve predictions for coupons.

Check [Prediction service README](prediction-service/README.md) for details.

### Recommendation service

Recommendation service handles Kafka requests.

When the entry event occurs it calls (TODO) the central resource for client data. The component stores the data in a cache - database (TODO).

When the focus event occurs the component gets client and coupon data from the cache (TODO) and calls prediction service.
The result of the prediction is pushed to Kafka.

Check [Recommendation service README](recommendation-service/README.md) for details.
Kafka topics description and schema can also be found there.
