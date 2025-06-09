# 🏠 House Price Prediction ML Project

This project is a complete **end-to-end Machine Learning pipeline** for predicting house prices. It incorporates modern tools for development, versioning, deployment, and monitoring.

<!-- Horizontal icons with spacing -->
<p align="left">
  <img src="assets/github-original-wordmark.png" alt="Github" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/githubactions.png" alt="Github Actions" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/jupyter.svg" alt="Jupyter Notebook" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/file-type-dvc.svg" alt="DVC" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/mongodb-original.svg" alt="Mongo DB" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/fastapi.png" alt="FastAPI" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/aws-iam-identity-and-access-management.svg" alt="IAM" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/storage-amazon-s3.svg" alt="S3 Bucket" width="40" height="40"/>
  &nbsp;&nbsp;
  <img src="assets/aws-ec2.svg" alt="EC2" width="40" height="40"/>
</p>

## 🚀 Project Overview

This ML system includes data ingestion, preprocessing, transformation, feature engineering, model training, evaluation, and deployment. It is designed with modularity, automation, and reproducibility in mind — using **Jupyter Notebooks** for experimentation and **FastAPI** for serving predictions. The entire ML lifecycle is tracked using **DVC** and **MLflow**, while **GitHub Actions** and **CI/CD pipelines** ensure automation and production readiness.

## 🔧 Tech Stack & Why We Use It

<p align="left">
  <img src="assets/fastapi.png" alt="FastAPI" width="40" height="40"/> &nbsp;&nbsp;
  <img src="assets/github-original-wordmark.png" alt="GitHub" width="40" height="40"/> &nbsp;&nbsp;
  <img src="assets/githubactions.png" alt="GitHub Actions" width="40" height="40"/>
</p>

1. **Jupyter Notebook** – Interactive development and exploratory data analysis.
2. **GitHub** – Version control for collaboration and reproducibility.
3. **GitHub Actions** – Automates testing, training, and deployment workflows (CI/CD).
4. **CI/CD** – Ensures continuous integration and automated delivery of updated models.
5. **Manual Deployment on EC2** – Custom deployment on cloud instance for full control and scalability.
6. **FastAPI** – Lightweight Python web framework to serve ML model predictions via REST API.
7. **S3 Bucket** – Stores raw and processed datasets and ML models securely and scalably.
8. **MongoDB** – Stores experiment metadata, model configurations, and logs.
9. **IAM (AWS Identity & Access Management)** – Secures and manages access to AWS resources like S3.
10. **DVC (Data Version Control)** – Tracks dataset and model versioning for reproducibility.
11. **MLflow** – Tracks ML experiments, metrics, artifacts, and model registry.

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
├── notebooks/               # EDA and training notebooks
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

> ✨ Designed with MLOps best practices in mind for scalability, automation, and reproducibility.

