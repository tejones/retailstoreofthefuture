# Build and deployment

## Table of contents
* [Prerequisites](#prerequisites)
* [Building images on Openshift Container Platform](#building-images-on-openshift-container-platform)
* [Deploy the solution using Helm Charts](#deploy-the-solution-using-helm-charts)

## Prerequisites
This instruction assumes that you have access to an Openshift Container Platform, 
and that you have the `oc` command line tool installed and configured to connect to your cluster.

In addition, you need to have the following components installed in your cluster:
* Kafka Broker
* MQTT Broker

Please, take a look at [KAFKA_MQTT.md](KAFKA_MQTT.md) for instructions on how to install them
if operators for AMQ Streams and AMQ Broker (Red Hat Integration) are installed.

Kafka and MQTT brokers addressees are configured in [values.yaml](../helm/retail-infra/values.yaml) file, 
so remember to update them.

## Building images on Openshift Container Platform
Build configs and image streams definitions are stored in [ocp-buildconfigs.yaml](ocp-buildconfigs.yaml).

Create BuildConfigs and ImageTags: 

```shell
oc apply -f ocp-buildconfigs.yaml
```

Verify build configs have been created:

```shell
oc get buildconfigs
```

```shell
NAME                            TYPE     FROM                LATEST
cachedb-loader                  Docker   Git@init-cache-db   0
customer-simulation-service     Docker   Git@develop-pl      0
prediction-service              Docker   Git@develop-pl      0
recommendation-service          Docker   Git@develop-pl      0
visualization-service           Docker   Git@develop-pl      0
```

Verify ImageTags have been created in your project:

```shell
oc get imagestreams
```

```shell
NAME                            IMAGE REPOSITORY                                                                                           TAGS     UPDATED
cachedb-loader                  default-route-openshift-image-registry.apps.rojo.igk.internal/retail-infra/cachedb-loader
customer-simulation-service     default-route-openshift-image-registry.apps.rojo.igk.internal/retail-infra/customer-simulation-service
prediction-service              default-route-openshift-image-registry.apps.rojo.igk.internal/retail-infra/prediction-service
recommendation-service          default-route-openshift-image-registry.apps.rojo.igk.internal/retail-infra/recommendation-service
visualization                   default-route-openshift-image-registry.apps.rojo.igk.internal/retail-infra/visualization
```

Manually trigger the images builds:

```shell
oc start-build customer-simulation-service
oc start-build prediction-service
oc start-build recommendation-service
oc start-build visualization-service
oc start-build cachedb-loader
```

Wait for the builds to complete:

```shell
oc get builds --watch
```

```shell
NAME                             TYPE     FROM             STATUS    STARTED               DURATION
prediction-service-build-1       Docker   Git@develop-pl   Running   5 seconds ago
prediction-service-build-1       Docker   Git@72d19cf      Running   12 seconds ago
recommendation-service-build-1   Docker   Git@develop-pl   Running   6 seconds ago   
recommendation-service-build-1   Docker   Git@72d19cf      Running   15 seconds ago
recommendation-service-build-1   Docker   Git@72d19cf      Running   About a minute ago   
recommendation-service-build-1   Docker   Git@72d19cf      Running   About a minute ago   
recommendation-service-build-1   Docker   Git@72d19cf      Complete   About a minute ago
prediction-service-build-1       Docker   Git@72d19cf      Running    About a minute ago
prediction-service-build-1       Docker   Git@72d19cf      Running    About a minute ago
prediction-service-build-1       Docker   Git@72d19cf      Complete   About a minute ago
```

See if the ImageTags have been updated:

```shell
oc get imagestreams
```

```shell
NAME                          IMAGE REPOSITORY                                                                                  TAGS     UPDATED
cachedb-loader                default-route-openshift-image-registry.apps.rojo.igk.internal/rsotf/cachedb-loader                latest   16 minutes ago
customer-simulation-service   default-route-openshift-image-registry.apps.rojo.igk.internal/rsotf/customer-simulation-service   latest   16 minutes ago
prediction-service            default-route-openshift-image-registry.apps.rojo.igk.internal/rsotf/prediction-service            latest   16 minutes ago
recommendation-service        default-route-openshift-image-registry.apps.rojo.igk.internal/rsotf/recommendation-service        latest   16 minutes ago
visualization-service         default-route-openshift-image-registry.apps.rojo.igk.internal/rsotf/visualization-service         latest   16 minutes ago
```

## Deploy the solution using Helm Charts

Edit the `values.yaml` file and configure your workload parameters:

```shell
vim retail-helm-chart/values.yaml
```

Install the Chart with Helm:

```shell
helm install retail retail-helm-chart/
```

```
NAME: retail
LAST DEPLOYED: 2021-04-07 14:52:49.839391 +0000 UTC m=+0.078141486
NAMESPACE: retail
STATUS: deployed
```

Verify all pods are Running:

```shell
oc get all
```

```
NAME                                       READY   STATUS      RESTARTS   AGE
pod/postgres-5f549f5798-9qz72              1/1     Running     0          68s
pod/prediction-6d8d96776c-fpcjn            1/1     Running     0          67s
pod/prediction-service-build-1-build       0/1     Completed   0          10m
pod/recommendation-7c954f47fb-8qjzm        1/1     Running     0          67s
pod/recommendation-service-build-1-build   0/1     Completed   0          10m

NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/postgres-svc         ClusterIP   172.31.128.7     <none>        5432/TCP   68s
service/prediction-svc       ClusterIP   172.31.109.189   <none>        80/TCP     68s
service/recommendation-svc   ClusterIP   172.31.185.22    <none>        80/TCP     68s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/postgres         1/1     1            1           68s
deployment.apps/prediction       1/1     1            1           68s
deployment.apps/recommendation   1/1     1            1           68s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/postgres-5f549f5798         1         1         1       68s
replicaset.apps/prediction-6d8d96776c       1         1         1       68s
replicaset.apps/recommendation-7c954f47fb   1         1         1       67s

NAME                                                          TYPE     FROM             LATEST
buildconfig.build.openshift.io/prediction-service-build       Docker   Git@develop-pl   1
buildconfig.build.openshift.io/recommendation-service-build   Docker   Git@develop-pl   1

NAME                                                      TYPE     FROM          STATUS     STARTED          DURATION
build.build.openshift.io/prediction-service-build-1       Docker   Git@72d19cf   Complete   10 minutes ago   1m45s
build.build.openshift.io/recommendation-service-build-1   Docker   Git@72d19cf   Complete   10 minutes ago   1m21s

NAME                                                    IMAGE REPOSITORY                                                                                TAGS     UPDATED                                                                                                                                                     
imagestream.image.openshift.io/prediction-service       default-route-openshift-image-registry.apps.red.ocp.public/retail/prediction-service       latest   8 minutes ago                                                                                                                                               
imagestream.image.openshift.io/recommendation-service   default-route-openshift-image-registry.apps.red.ocp.public/retail/recommendation-service   latest   8 minutes ago                                                                                                                                               

NAME                                               HOST/PORT                                                 PATH   SERVICES             PORT                  TERMINATION   WILDCARD                                                                                                                                        
route.route.openshift.io/prediction-external       prediction-external-retail.apps.red.ocp.public              prediction-svc       prediction-port                     None                                                                                                                                            
route.route.openshift.io/recommendation-external   recommendation-external-retail.apps.red.ocp.public          recommendation-svc   recommendation-port                 None      
```

## Notes

### Using private GitHub repository

Please, note, that if you require private repository access, you must create a secret containing GitHub deploy key
(see https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys for details 
on managing deploy keys).

The key could be stored as a secret:

```shell
oc create secret generic retail-git-ssh-key --from-file=ssh-privatekey=<path_to_private_key> --type=kubernetes.io/ssh-auth
```

And used in build config definition:
```yaml
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: prediction-service
spec:
  source:
    type: Git
    sourceSecret:                                       # use the secret
      name: retail-git-ssh-key
    git:
      uri: 'https://github.com/karol-brejna-i/retailstoreofthefuture.git'
      ref: develop
    contextDir: prediction-service/
  strategy:
    type: Docker
  output:
    to:
      kind: ImageStreamTag
      name: 'prediction-service:latest'
```
