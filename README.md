 # 🏠 House Price Prediction with DVC, Flask, Docker & Helm on GCP (GKE)

This project demonstrates an end-to-end MLOps workflow for a **regression model** predicting house prices. The primary focus is on **MLOps tooling**: version control, model packaging, containerization, and Kubernetes deployment using Helm on **Google Cloud Platform**.

---

## 🚀 Project Overview

**Use Case:** House price prediction based on features like area, number of bedrooms, location, etc.

- 📥 **Input:** JSON with house features  
- 📤 **Output:** Predicted price  
- 🔍 **Model:** Linear Regression / LightGBM  
- 📊 **Dataset:** Banglore Housing data  

---

## 🔧 Tools & Why They're Used

| Tool | Purpose | Description |
|------|---------|-------------|
| **DVC** | Data & model versioning | Tracks dataset and model files. Enables reproducible pipelines. Stores large files remotely (e.g., Google Drive or GCS). |
| **scikit-learn** | Model training | Lightweight ML library to build the regression model. |
| **Flask** | Model serving | Minimal web server to expose a `/predict` API endpoint. |
| **Gunicorn** | Production WSGI server | Serves Flask app in production (multi-threaded). |
| **Docker** | Containerization | Packages Flask app, model, and dependencies into a portable image. |
| **Helm** | Kubernetes deployment | Helm charts manage GKE deployment, service, and configuration. |
| **GKE (GCP)** | Deployment platform | Host our Docker container using Google Kubernetes Engine. |

---

## 📁 Project Structure

```bash
house-price-prediction/
│
├── data/                     # Raw and processed data
├── models/                   # Trained models
├── src/                      # Source code
│   ├── train.py              # Model training script
│   └── app.py                # Flask API
├── dvc.yaml                  # DVC pipeline definition
├── Dockerfile                # Dockerfile to build the app
├── helm/                     # Helm chart folder
│   ├── templates/
│   └── values.yaml
├── requirements.txt          # Python dependencies
└── README.md                 # You are here
```

---

## 🧪 Step-by-Step Workflow

### 1. ⚙️ Set up DVC for Data Versioning

Initialize DVC & add dataset:
```bash
dvc init
dvc add data/train.csv
```

### 2. 🤖 Train the Model

```bash
python src/train.py
```

This will train and save the model to \`models/model.joblib\`.

---

### 3. 🌐 Serve Model via Flask

```bash
python src/app.py
```

API Endpoint:
```bash
POST /predict
{
  "features": [value1, value2, ...]
}
```

---

### 4. 🐳 Dockerize the Flask App

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
```

Build and tag the image:
```bash
docker build -t house-price-api .
```

Push to Google Container Registry (GCR):
```bash
docker tag house-price-api gcr.io/<project-id>/house-price-api
docker push gcr.io/<project-id>/house-price-api
```

---

### 5. ⛵ Deploy with Helm on GKE

**Install Helm & configure:**

```bash
gcloud container clusters create ml-cluster --num-nodes=2
gcloud container clusters get-credentials ml-cluster
```

Update \`values.yaml\`:
```yaml
image:
  repository: gcr.io/<project-id>/house-price-api
  tag: latest
service:
  type: LoadBalancer
```

Install Helm chart:
```bash
helm install house-price helm/
```

Check status:
```bash
kubectl get svc
```

Use the external IP to access the \`/predict\` API.

---

## ✅ Example Prediction

```bash
curl -X POST http://<external-ip>:5050/predict     -H "Content-Type: application/json"     -d '{"features": [0.00632, 18.0, 2.31, 0, 0.538, 6.575, 65.2, 4.09, 1, 296.0, 15.3, 396.9, 4.98]}'
```

---

## 📦 Reproducible Pipelines with DVC

To run the entire ML pipeline:
```bash
dvc repro
```

If you change any stage (e.g., data, parameters), DVC will re-run only the affected parts.

---

## 📚 Requirements

```txt
scikit-learn
Flask
gunicorn
joblib
dvc[gdrive]
```

---

## 🧹 Cleanup

```bash
helm uninstall house-price
gcloud container clusters delete ml-cluster
```

---

## 📌 Summary

✅ **End-to-end MLOps project**  
✅ **Version-controlled ML pipelines**  
✅ **Scalable deployment via GKE + Helm**  
✅ **Production-ready Flask API in Docker**

---

### For detailed step by step working setup of the project. Navigate to the file {project_flow.txt}.

## 📎 Related Links

- [DVC Docs](https://dvc.org/doc)
- [Helm Docs](https://helm.sh/docs/)
- [Flask Docs](https://flask.palletsprojects.com/)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- [Google Container Registry](https://cloud.google.com/container-registry)

## 📬 Contact

For queries, feedback, or contributions:

👤 [Bharat Aameriya](https://www.linkedin.com/in/bharat-aameriya-24579a261/)  
📂 Feel free to open an issue or submit a pull request on this repository.

---