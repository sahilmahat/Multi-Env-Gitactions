# Multi-Environment GitOps CI/CD Pipeline

Docker · GitHub Actions · Kubernetes · ArgoCD

---

# Overview

This project demonstrates a **modern DevOps CI/CD pipeline using GitOps principles**.

The system automatically:

1. Builds a Docker image
2. Pushes the image to DockerHub
3. Deploys the application to Kubernetes
4. Synchronizes cluster state using ArgoCD

The deployment supports **multiple environments**:

```
DEV
STAGING
PRODUCTION
```

Each environment runs independently with different replica configurations.

---

# Architecture

```
Developer
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions (CI)
   │
   ├── Build Docker Image
   ├── Tag Image
   └── Push Image → DockerHub
   │
   ▼
Git Repository (K8s Manifests)
   │
   ▼
ArgoCD (GitOps Controller)
   │
   ▼
Kubernetes Cluster
   │
   ▼
Pods Running Application
```

---

# Project Structure

```
mscicd
│
├── app.py
├── Dockerfile
├── requirements.txt
│
├── k8s
│   ├── dev
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   │
│   ├── staging
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   │
│   └── prod
│       ├── deployment.yaml
│       └── service.yaml
│
└── .github/workflows
    └── pipeline.yaml
```

---

# Application

Simple Flask application used for deployment testing.

## app.py

```python
from flask import Flask
import os

app = Flask(__name__)

ENV = os.getenv("ENVIRONMENT","dev")

@app.route("/")
def home():
    return f"Running in {ENV} environment"

app.run(host="0.0.0.0",port=5000)
```

---

# Dockerfile

```
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","app.py"]
```

---

# requirements.txt

```
flask
```

---

# Kubernetes Deployments

Each environment has its own deployment.

## DEV

```
replicas: 1
environment: dev
```

## STAGING

```
replicas: 2
environment: staging
```

## PRODUCTION

```
replicas: 3
environment: production
```

---

# Example Deployment Manifest

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cicd-app-dev

spec:
  replicas: 1

  selector:
    matchLabels:
      app: cicd-app-dev

  template:
    metadata:
      labels:
        app: cicd-app-dev

    spec:
      containers:
      - name: cicd-app
        image: sahilmahat/cicd:latest

        ports:
        - containerPort: 5000

        env:
        - name: ENVIRONMENT
          value: dev
```

---

# Kubernetes Service

Example service exposing the application.

```
apiVersion: v1
kind: Service
metadata:
  name: cicd-service-dev

spec:
  type: NodePort

  selector:
    app: cicd-app-dev

  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30001
```

---

# GitHub Actions CI Pipeline

Location:

```
.github/workflows/pipeline.yaml
```

Pipeline performs:

```
1. Checkout code
2. Login to DockerHub
3. Build Docker image
4. Push image to DockerHub
```

Example pipeline:

```
name: Multi Environment CI/CD

on:
  push:
    branches: [ main ]

jobs:

  build:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Docker Login
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker Image
        run: |
          docker build -t sahilmahat/cicd:${{ github.sha }} .

      - name: Push Docker Image
        run: |
          docker push sahilmahat/cicd:${{ github.sha }}
```

---

# Install ArgoCD

Create namespace:

```
kubectl create namespace argocd
```

Install ArgoCD:

```
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Verify installation:

```
kubectl get pods -n argocd
```

---

# Access ArgoCD UI

Run:

```
kubectl port-forward svc/argocd-server -n argocd 9090:443 --address 0.0.0.0
```

Open browser:

```
http://<EC2_PUBLIC_IP>:9090
```

---

# Get Admin Password

```
kubectl get secret argocd-initial-admin-secret \
-n argocd \
-o jsonpath="{.data.password}" | base64 -d
```

Login credentials:

```
username: admin
password: <output>
```

---

# Create ArgoCD Application

Repository:

```
https://github.com/sahilmahat/Multi-Env-Gitactions.git
```

Path:

```
k8s
```

Cluster:

```
https://kubernetes.default.svc
```

Enable:

```
Auto Sync
Self Heal
Prune
```

---

# GitOps Deployment Flow

```
Developer Push
        │
        ▼
GitHub Actions
        │
        ▼
DockerHub Image
        │
        ▼
Git Manifests Updated
        │
        ▼
ArgoCD Detects Change
        │
        ▼
Kubernetes Deployment Updated
```

---

# Access Applications

DEV

```
http://EC2_PUBLIC_IP:8081
```

STAGING

```
http://EC2_PUBLIC_IP:8082
```

PRODUCTION

```
http://EC2_PUBLIC_IP:8083
```

(using port-forward in this setup)

---

# Debugging Commands

Check pods:

```
kubectl get pods
```

Check services:

```
kubectl get svc
```

View logs:

```
kubectl logs <pod>
```

Describe deployment:

```
kubectl describe deployment <deployment-name>
```

---

# Key DevOps Concepts Demonstrated

```
Docker Containerization
CI Automation using GitHub Actions
Kubernetes Orchestration
Multi-Environment Deployments
GitOps Continuous Delivery
Self-Healing Infrastructure
Declarative Infrastructure
```

---

# Future Improvements

Possible production improvements:

```
Helm charts
Ingress controller
Argo Rollouts (canary deployment)
Prometheus monitoring
Grafana dashboards
Centralized logging
```

---

# Author

```
Sahil Mahat
DevOps / Cloud / Kubernetes Projects
```

