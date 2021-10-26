# Kafka Guide

## Installation

If can follow [this](https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes) tutorial. But different versions can behave differently. Moreover if you deploy kafka following above tutorial, you have to change some codes here. So, alternatively you deploy kafka from a `yaml` file. Still make sure you have helm installed. Once done, copy this in your terminal

### STEP:1

```bash
$ helm template kafka bitnami/kafka \
     --set volumePermissions.enabled=true \
     --set zookeeper.volumePermissions.enabled=true \
     --set zookeeperConnectionTimeoutMs=10000 \
     > kafka.yaml
```

### STEP:2

It will create a `kafka.yaml` in for current directory. Now deploy this with `kubectl apply -f kafka.yaml`. Now you can check `kubectl get pod` and wait for sometime untill both `kafka` and `zookeeper` are in `running` state. It should look something like this:  

```bash
NAME                     READY   STATUS    RESTARTS AGE 
kafka-0                  1/1     Running   0        3m41s
kafka-zookeeper-0        1/1     Running   0        3m41s
```

It may take 10-20 mins to be in `running` state, in that time pods may be in `ImagePullBackOff` or `PodInitializing` state several times, so be alert. You may also want keep kubeclt to wait for sometime untill both are running using

```bash
$ kubectl wait pod --timeout 300s --for=condition=Ready \
       -l app.kubernetes.io/name=kafka
```

### STEP:3

Now create a topic with this

```bash
$ kubectl exec -it kafka-0 -- kafka-topics.sh \
       --create --bootstrap-server kafka-headless:9092 \
       --replication-factor 1 --partitions 1 \ 
       --topic mytopic
```

See if that outputs something like this (**Don't copy**)

```bash
 Defaulted container "kafka" out of: kafka, volume-permissions (init)
 Created topic mytopic.
```

### STEP:4

Check the `kubectl get svc` output looks something like this

```bash
  NAME                          TYPE      CLUSTER-IP      EXTERNAL-IP      PORT(S)                     AGE
  kafka-zookeeper-headless    ClusterIP     None            <none>      2181/TCP,2888/TCP,3888/TCP     125m
  kafka-zookeeper             ClusterIP   10.43.79.54       <none>      2181/TCP,2888/TCP,3888/TCP     125m
  kafka-headless              ClusterIP     None            <none>        9092/TCP,9093/TCP            125m
  kafka                       ClusterIP   10.43.208.124     <none>        9092/TCP                     125m
```

If everything works, you are good to go.

## Issues

If you have faced any deployment issue(in step:1), you can try this to increase timeout

```bash
$ helm template kafka bitnami/kafka \
     --set volumePermissions.enabled=true \
     --set zookeeper.volumePermissions.enabled=true \
    --set zookeeperConnectionTimeoutMs=10000 \
    --set readinessProbe.periodSeconds=20 \
    --set readinessProbe.timeoutSeconds=10 \
    > kafka.yaml
```

Now redeploy using

```bash
$ kubectl delete -f kafka.yaml
$ kubectl apply -f kafka.yaml
```

If you have issues while creating topic(in step:3), you can try `--bootstrap-server` instead of the deprecated `--zookeeper`

```bash
$ kubectl exec -it kafka-0 -- \
    kafka-topics.sh --create \
    --bootstrap-server kafka-headless:9092 \
    --replication-factor 1 --partitions 1 \
    --topic mytopic
```

If this step fails, **in separate terminals** start the consumer and producer, blocking the terminals

```bash
kubectl exec -it kafka-0 -- kafka-console-consumer.sh \
        --bootstrap-server kafka-headless:9092 \
        --topic mytopic
# output:
# Defaulted container "kafka" out of: kafka, volume-permissions (init)
```

and

```bash
kubectl exec -it kafka-0 -- kafka-console-producer.sh \
       --broker-list kafka-headless:9092 \
       --topic mytopic
# output:
# Defaulted container "kafka" out of: kafka, volume-permissions (init)
# >message 1
# >message 2
```

The `message 1` and `message 2` should appear in the consumer output. Exit producer with `ctrl+d`, and consumer with `ctrl+c`.
