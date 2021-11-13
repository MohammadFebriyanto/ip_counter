# Print IP and Hit Counter Application

## Description
In this application we can count how much spesific IP address hit an service.

## Structure
- app.py is the code of the app that written in python
- Dockerfile is the file of docker to containeraize this application 

## How to run
To run this application, you can follow the steps below:

1. Please make sure you have installed docker-compose. If not please go to https://docs.docker.com/compose/install/ to install docker-compose.
2. You can just running this application using this command:
   ``` docker-compose up -d ```

## How to make this service scalable
To make this service scalable you can deploy this container into a kubernetes cluster.
Then you can make HPA based on CPU metrics (for example) to make the pod of this service scalable.

for example you can make a deployment.yaml like this:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: application
spec:
  selector:
    matchLabels:
      run: application
  replicas: 1
  template:
    metadata:
      labels:
        run: application
    spec:
      containers:
      - name: application
        image: <image-of-this-service>
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 500m
          requests:
            cpu: 200m
---
apiVersion: v1
kind: Service
metadata:
  name: application
  labels:
    run: application
spec:
  ports:
  - port: 80
  selector:
    run: application
```

and then write the HPA (hpa.yaml) to make your service auto scale (for example based on CPU metrics):
```
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: application
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: application
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

On this HPA you can see that if the CPU use more than 50% the replicas will be created, the maximal pod of this deployment will be 10 pod.