# Kubernetes EKS Platform

Production-grade Kubernetes platform deploying a Python Flask application 
on AWS EKS using Helm charts, with Horizontal Pod Autoscaling, 
health monitoring, and CI/CD via GitHub Actions.

## Architecture

Developer pushes code to GitHub

↓

GitHub Actions builds Docker image → pushes to Amazon ECR

↓

Helm deploys to Kubernetes (Minikube locally / EKS on AWS)

↓

Horizontal Pod Autoscaler scales pods 2→5 based on CPU load

↓

Liveness + Readiness probes monitor pod health automatically

↓

Flask app live at /  /health  /info endpoints

## Tech Stack

- **Orchestration:** Kubernetes (Minikube locally / AWS EKS in production)
- **Package Manager:** Helm v4
- **App:** Python Flask + Gunicorn
- **Containerization:** Docker
- **Autoscaling:** Horizontal Pod Autoscaler (HPA)
- **Cloud:** AWS EKS (eu-north-1)
- **CLI Tools:** kubectl · eksctl · helm

## Project Structure

kubernetes-eks-platform/

├── app/

│   ├── main.py              # Flask app with /, /health, /info endpoints

│   └── requirements.txt     # Python dependencies

├── Dockerfile               # Multi-stage container build

├── helm/

│   └── flask-app/

│       ├── Chart.yaml       # Helm chart metadata

│       ├── values.yaml      # Configurable values

│       └── templates/

│           ├── deployment.yaml   # Kubernetes Deployment

│           ├── service.yaml      # NodePort Service

│           └── hpa.yaml          # Horizontal Pod Autoscaler

├── k8s/

│   └── namespace.yaml       # flask-app namespace

└── screenshots/             # Architecture proof screenshots

## Key Features

- **Helm-managed deployment** — entire app deployed and upgraded with one command
- **Horizontal Pod Autoscaling** — scales from 2 to 5 pods when CPU > 70%
- **Health probes** — Kubernetes automatically restarts unhealthy pods
- **Namespace isolation** — app runs in dedicated `flask-app` namespace
- **Resource limits** — CPU and memory limits defined per pod
- **3 API endpoints** — `/` home, `/health` status, `/info` pod metadata

## Quick Start (Local — Minikube)

### Prerequisites
- Docker Desktop running
- Minikube installed
- Helm installed
- kubectl installed

### Deploy locally

```bash
# Start Minikube
minikube start --driver=docker --cpus=2 --memory=3500

# Point Docker to Minikube
eval $(minikube docker-env)

# Build Docker image
docker build -t flask-k8s-app:latest .

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy with Helm
helm install flask-app helm/flask-app --namespace flask-app

# Watch pods start
kubectl get pods -n flask-app --watch

# Access the app
minikube service flask-app-service -n flask-app
```

### Useful commands

```bash
# Check all resources
kubectl get all -n flask-app

# Check autoscaler
kubectl get hpa -n flask-app

# Check Helm releases
helm list -n flask-app

# Upgrade deployment
helm upgrade flask-app helm/flask-app --namespace flask-app

# View pod logs
kubectl logs -l app=flask-app -n flask-app

# Delete everything
helm uninstall flask-app -n flask-app
```

## API Endpoints

| Endpoint | Method | Response |
|---|---|---|
| `/` | GET | HTML homepage |
| `/health` | GET | JSON health status + pod name |
| `/info` | GET | JSON pod metadata + version |

## Kubernetes Resources

| Resource | Details |
|---|---|
| Deployment | 2 replicas, rolling update strategy |
| Service | NodePort on port 5000 |
| HPA | Min 2 / Max 5 pods, CPU threshold 70% |
| Namespace | flask-app (isolated environment) |
| Probes | Liveness + Readiness on /health |

## Screenshots

### Pods Running
![Pods](screenshots/pods-running.png)

### All Kubernetes Resources
![All Resources](screenshots/all-resources.png)

### Horizontal Pod Autoscaler
![HPA](screenshots/hpa.png)

### Helm Deployment
![Helm](screenshots/helm-list.png)

### Live Application
![App](screenshots/app-browser.png)

### Health Endpoint
![Health](screenshots/health-endpoint.png)

### Info Endpoint
![Info](screenshots/info-endpoint.png)

## Key Concepts Demonstrated

- Kubernetes Deployments, Services, and Namespaces
- Helm chart creation and deployment management
- Horizontal Pod Autoscaling based on CPU metrics
- Liveness and Readiness health probes
- Container resource requests and limits
- kubectl CLI proficiency
- Local Kubernetes development with Minikube
- Production-ready application packaging