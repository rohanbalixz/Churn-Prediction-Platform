# Customer Churn Prediction Platform

A self‑contained, end‑to‑end example showing how to build, train, and deploy a churn prediction model using Delta Lake, PySpark, TensorFlow, XGBoost, and FastAPI. It includes scripts to generate synthetic data, run local ingestion & preprocessing, train an LSTM+XGBoost ensemble, and expose a REST API in Docker.

---

## 🚀 Features

- **Data Ingestion**: Load CSV into Delta Lake (local) via `src/ingest.py`.
- **Preprocessing**: Engineer features, pivot events, and split into train/test with `src/preprocess.py`.
- **Data Generation**: Create 1,000-row synthetic dataset via `src/generate_data.py`.
- **Modeling**: Train an LSTM + XGBoost ensemble and save models in `models/` using `src/train_model.py`.
- **API**: FastAPI service (`src/app.py`) with `/predict` endpoint for inference.
- **Containerization**: Dockerfile + `run_docker.sh` to build and run your API anywhere.
- **Helper Scripts**: `scripts/predict.sh` to test predictions easily.

---

## 📋 Prerequisites

- macOS or Linux with:
  - Python 3.10+ and `venv`
  - Docker
  - Java 11 runtime (for Spark)

---

## 🛠️ Setup & Quickstart

1. **Clone the repo**

   ```bash
   git clone git@github.com:<your-username>/churn-prediction-dev.git
   cd churn-prediction-dev
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python3 -m venv churn-dev
   source churn-dev/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Generate sample data**

   ```bash
   python src/generate_data.py
   ```

4. **Ingest into Delta Lake**

   ```bash
   python src/ingest.py
   ```

5. **Preprocess & split**

   ```bash
   python src/preprocess.py
   ```

6. **Train & save models**

   ```bash
   python src/train_model.py
   ```

7. **Run API locally**

   ```bash
   uvicorn src.app:app --reload --port 8000
   ```

8. **Test endpoint**

   ```bash
   ./scripts/predict.sh
   ```

9. **Dockerize & run**

   ```bash
   ./run_docker.sh
   ```

---

## 📂 Repository Structure

```plaintext
churn-prediction-dev/
├── src/                 # PySpark, model, and API code
│   ├── ingest.py
│   ├── preprocess.py
│   ├── generate_data.py
│   ├── train_model.py
│   └── app.py
├── data/                # sample CSV or generator script
├── models/              # saved LSTM & XGBoost models (gitignored)
├── scripts/             # helper bash scripts
│   ├── predict.sh
├── Dockerfile           # container definition
├── requirements.txt     # Python dependencies
├── run_docker.sh        # helper Docker script
├── predict.sh   # helper API test script
└── run_docker.sh
├── .gitignore
└── README.md
```

---

## 🎓 Next Steps

- Push Docker image to Docker Hub or ECR
- Automate CI/CD (GitHub Actions, GitLab CI)
- Deploy to AWS ECS/Fargate with API Gateway
- Add monitoring & logging (Prometheus, Grafana)
