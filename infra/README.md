### Building images on Openshift Container Platform

If you require a private repository access you must create a secret containing Github Deploy Key
```
oc create secret generic retail-git-ssh-key --from-file=ssh-privatekey=<path_to_private_key> --type=kubernetes.io/ssh-auth
```
Create BuildConfigs and ImageTags: 
```
oc apply -f ocp-buildconfigs.yaml
```
Verify build configs have been created:
```
oc get buildconfigs
```
```
NAME                           TYPE     FROM             LATEST
prediction-service-build       Docker   Git@develop-pl   0
recommendation-service-build   Docker   Git@develop-pl   0
```
Verify ImageTags have been created in your project:
```bash
oc get is
```
```
NAME                     IMAGE REPOSITORY                                                                                TAGS     UPDATED
prediction-service       default-route-openshift-image-registry.apps.red.ocp.public/retail/prediction-service          
recommendation-service   default-route-openshift-image-registry.apps.red.ocp.public/retail/recommendation-service      
```
Manually trigger the images builds:
```bash
oc start-build customer-simulation-service
oc start-build prediction-service
oc start-build recommendation-service
oc start-build visualization-service
```
Wait for the builds to complete:
```bash
oc get builds --watch
```
```
NAME                             TYPE     FROM             STATUS    STARTED               DURATION
prediction-service-build-1       Docker   Git@develop-pl   Running   5 seconds ago   
prediction-service-build-1       Docker   Git@72d19cf      Running   12 seconds ago   
recommendation-service-build-1   Docker   Git@develop-pl   Running   6 seconds ago    
recommendation-service-build-1   Docker   Git@72d19cf      Running   15 seconds ago   
recommendation-service-build-1   Docker   Git@72d19cf      Running   About a minute ago   
recommendation-service-build-1   Docker   Git@72d19cf      Running   About a minute ago   
recommendation-service-build-1   Docker   Git@72d19cf      Complete   About a minute ago   1m21s
prediction-service-build-1       Docker   Git@72d19cf      Running    About a minute ago   
prediction-service-build-1       Docker   Git@72d19cf      Running    About a minute ago   
prediction-service-build-1       Docker   Git@72d19cf      Complete   About a minute ago   1m45s
```

See if the ImageTags have been updated:
```bash
oc get is
```
```
NAME                     IMAGE REPOSITORY                                                                           TAGS     UPDATED
prediction-service       default-route-openshift-image-registry.apps.red.ocp.public/retail/prediction-service       latest   1 minutes ago
recommendation-service   default-route-openshift-image-registry.apps.red.ocp.public/retail/recommendation-service   latest   1 minutes ago
```

### Deploy the solution using Helm Charts
Edit the `values.yaml` file and configure your workload parameters:
```bash
vim retail-helm-chart/values.yaml
```
Install the Chart with Helm: 
```bash
helm install retail retail-helm-chart/
```
```
NAME: retail
LAST DEPLOYED: 2021-04-07 14:52:49.839391 +0000 UTC m=+0.078141486
NAMESPACE: retail
STATUS: deployed
```

Verify all pods are Running and in a Ready:
```bash
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
