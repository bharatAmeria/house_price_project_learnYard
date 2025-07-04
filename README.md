# 🏠 House Price Prediction ML Project

This project is a complete **end-to-end Machine Learning pipeline** for predicting house prices. It incorporates modern tools for development, versioning, deployment, and monitoring.

## 🚀 Project Overview

This ML system includes data ingestion, preprocessing, transformation, feature engineering, model training, evaluation, and deployment. It is designed with modularity, automation, and reproducibility in mind — using **Flask** for serving predictions. The entire ML lifecycle is tracked using **DVC** and **MLflow**, while **GitHub Actions** and **CI/CD pipelines** ensure automation and production readiness.

## 🔧 Tech Stack & Why We Use It

<!-- Horizontal icons with spacing -->
<p align="left">
  <img src="assets/github-original-wordmark.png" alt="Github" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/githubactions.png" alt="Github Actions" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/file-type-dvc.svg" alt="DVC" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/fastapi.png" alt="FastAPI" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/aws-iam-identity-and-access-management.svg" alt="IAM" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/storage-amazon-s3.svg" alt="S3 Bucket" width="40" height="40"/>
  &nbsp;&nbsp;
</p>

1. **GitHub** – Version control for collaboration and reproducibility.
2. **GitHub Actions** – Automates testing, training, and deployment workflows (CI/CD).
3. **CI/CD** – Ensures continuous integration and automated delivery of updated models.
4. **Manual Deployment on EC2** – Custom deployment on cloud instance for full control and scalability.
5. **Flask** – Lightweight Python web framework to serve ML model predictions via REST API.
6. **S3 Bucket** – Stores raw and processed datasets and ML models securely and scalably.
7. **MongoDB** – Stores experiment metadata, model configurations, and logs.
8. **IAM (AWS Identity & Access Management)** – Secures and manages access to AWS resources like S3.
9. **DVC (Data Version Control)** – Tracks dataset and model versioning for reproducibility.
10. **MLflow** – Tracks ML experiments, metrics, artifacts, and model registry.

## 🛠️ Pipeline Components

- **Data Ingestion** → from S3 or local source.
- **Data Preprocessing & Transformation** → handled in Jupyter & scripted pipelines.
- **Model Training** → trained and tracked using MLflow.
- **Model Evaluation** → using MAE, RMSE, and R² metrics.
- **Model Serving** → deployed using FastAPI.
- **CI/CD** → automated using GitHub Actions.
- **Deployment** → on AWS EC2 with secure S3 integration.

## 📁 Project Structure

```
.
├── data/                    # Raw and processed data
├── src/                     # Source code: ingestion, training, utils
├── models/                  # Saved models
├── .dvc/                    # DVC pipelines and tracking
├── .github/workflows/       # GitHub Actions CI/CD pipelines
├── main.py                  # FastAPI inference app
├── requirements.txt         # Python dependencies
└── README.md
```

## 📦 Future Improvements

- Docker containerization and EKS deployment
- Full ML monitoring with Prometheus & Grafana
- Real-time prediction and feedback loop

---

## 🧑‍💻 Step-by-Step Setup & Development Flow

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/house-price-ml.git
cd house-price-ml
```

### 2️⃣ Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file with your secrets for S3, MongoDB, etc.

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
MONGO_URI=your_mongodb_uri
```

### 4️⃣ Data Versioning with DVC

```bash
dvc pull  # Pulls data from remote (S3)
```

To add or update data:

```bash
dvc add data/raw_data.csv
dvc push
```

### 5️⃣ Run Jupyter Notebooks

For EDA, preprocessing, feature engineering:

```bash
jupyter notebook
```

### 6️⃣ Train the Model & Track with MLflow

```bash
python src/train.py
# MLflow UI (optional)
mlflow ui
```

### 7️⃣ Model Serving with FastAPI

```bash
uvicorn main:app --reload
```

### 8️⃣ Set Up GitHub Actions CI/CD

Push to GitHub to trigger `.github/workflows/train-deploy.yml`

---

# 🚀 GCP Flask App Deployment to GKE using Docker, Helm, and GitHub Actions

This document outlines the full deployment lifecycle for a Flask app to **Google Kubernetes Engine (GKE)** using Docker, Helm charts, and GitHub Actions. It also includes billing cleanup instructions to avoid future charges.

## ⚙️ Step 1: Build Docker Image and Push to GCR

1. Authenticate with Google:
   ```bash
   gcloud auth login
   gcloud config set project <your-project-id>
   ```

2. Build and push Docker image:
   ```bash
   docker build -t gcr.io/<your-project-id>/flask-app:v1 .
   docker push gcr.io/<your-project-id>/flask-app:v1
   ```

---

## ☸️ Step 2: Create and Connect to GKE Cluster

```bash
gcloud container clusters create flask-cluster --num-nodes=2 --zone=us-central1-c
gcloud container clusters get-credentials flask-cluster --zone=us-central1-c
```

---

## 🔧 Step 3: Configure Helm Chart

Edit `helm/flask-chart/values.yaml`:

```yaml
image:
  repository: gcr.io/<your-project-id>/flask-app
  tag: v1
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 5000

serviceAccount:
  create: false
  name: ""

autoscaling:
  enabled: false

ingress:
  enabled: false
```

---

## 🚀 Step 4: Deploy App Using Helm

```bash
helm install flask-release ./helm/flask-chart
```

To update after changes:
```bash
helm upgrade flask-release ./helm/flask-chart
```

---

## 🌐 Step 5: Access the App

Get the external IP:

```bash
kubectl get svc
```

Visit in browser:
```
http://<EXTERNAL-IP>
```

---

## 🛡️ Step 6: Set Up GitHub Actions (CI/CD)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GKE

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Auth GCP
        uses: google-github-actions/setup-gcloud@v2
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          export_default_credentials: true

      - name: Build & Push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/flask-app:v1 .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/flask-app:v1

      - name: Deploy with Helm
        run: |
          gcloud container clusters get-credentials flask-cluster --zone=us-central1-c
          helm upgrade --install flask-release ./helm/flask-chart             --set image.repository=gcr.io/${{ secrets.GCP_PROJECT_ID }}/flask-app             --set image.tag=v1
```

> 🔐 Add GitHub secrets:
- `GCP_PROJECT_ID`
- `GCP_SA_KEY` (Base64 encoded service account JSON)

---

## 💸 Step 7: Clean Up to Avoid Billing

You are billed for:
- GKE clusters
- Load balancers
- Static IPs
- Persistent disks
- Container images

### Delete Cluster
```bash
gcloud container clusters delete flask-cluster --zone=us-central1-c
```

### Delete Images
```bash
gcloud container images delete gcr.io/<your-project-id>/flask-app:v1
```

### Optional: Shut Down Entire Project
```bash
gcloud projects delete <your-project-id>
```

Or from Console:  
https://console.cloud.google.com/cloud-resource-manager

---

## 🧼 If You See: `403 - Billing Required`
To delete the cluster or project:
- Re-enable billing temporarily at  
  https://console.cloud.google.com/billing/enable
- Then delete the resources
- Disable billing again or shut down the project

---

## 🏁 Done!

You've deployed a Flask app to GKE, automated it with CI/CD, and learned how to clean up to avoid charges. ✅