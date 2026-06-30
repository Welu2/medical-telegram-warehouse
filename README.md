````markdown
# 📦 Medical Telegram Data Warehouse

An end-to-end data engineering pipeline that extracts medical product data from Ethiopian Telegram channels, transforms it using **dbt**, enriches image data with **YOLOv8** object detection, orchestrates workflows using **Dagster**, stores results in **PostgreSQL**, and exposes analytics through a **FastAPI** REST API.

---

## 🚀 Project Overview

This project builds a modern ELT data platform for analyzing Ethiopian medical Telegram channels, including:

- CheMed
- Lobelia Cosmetics
- Tikvah Pharma
- Other public medical-related Telegram channels

The pipeline supports the complete data lifecycle, from raw data ingestion to analytical API endpoints.

---

## 🏗️ Project Architecture

```text
Telegram Channels
        │
        ▼
Dagster Orchestration (Task 5)
        │
        ▼
Telethon Scraper
        │
        ▼
Raw Data (JSON + Images)
        │
        ▼
PostgreSQL
        │
        ▼
dbt Transformations
        │
        ▼
Star Schema Warehouse
        │
        ▼
YOLOv8 Image Enrichment
        │
        ▼
FastAPI Analytics API
```

---

## ⚙️ Technology Stack

- Python
- PostgreSQL
- Telethon
- dbt
- Dagster
- FastAPI
- SQLAlchemy
- Ultralytics YOLOv8
- OpenCV
- Docker

---

## 📁 Project Structure

```text
medical-telegram-warehouse/
│
├── api/
├── data/
├── logs/
├── medical_warehouse/
├── src/
├── scripts/
├── pipeline.py              # Dagster orchestration (Task 5)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` File

```env
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+251XXXXXXXXX

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=medical_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

---

# 🧩 Task 1 – Telegram Data Extraction

## Objective

Collect medical product data from Ethiopian Telegram channels.

### Run the Scraper

```bash
python -m src.scraper
```

---

# 🏢 Task 2 – Data Warehouse with dbt

### Run dbt

```bash
cd medical_warehouse

dbt run
dbt test
```

---

# 🖼️ Task 3 – YOLOv8 Image Enrichment

```bash
python src/yolo_detect.py
```

---

# 🌐 Task 4 – FastAPI Analytical API

```bash
uvicorn api.main:app --reload --port 8001
```

---

# ⚙️ Task 5 – Pipeline Orchestration (Dagster)

## Objective

Automate the entire data pipeline using **Dagster** to provide:

- Reproducibility
- Observability
- Scheduling
- Failure handling

### Pipeline Workflow

```text
scrape_telegram_data
        │
        ▼
load_raw_to_postgres
        │
        ▼
run_dbt_transformations
        │
        ▼
run_yolo_enrichment
```

---

## ⚙️ Dagster Features

- Modular ops-based pipeline
- Dependency management between pipeline stages
- Built-in logging for each operation
- Failure sensors for monitoring
- Cron-based scheduling support
- UI-based execution tracking

---

## 🚀 Running the Dagster Pipeline

### Start the Dagster UI

```bash
dagster dev -f pipeline.py
```

### Open the UI

```
http://localhost:3000
```

### Execute the Pipeline

1. Select **medical_pipeline**
2. Click **Launch Run**
3. Monitor execution logs in the Dagster UI

---

## 📊 Dagster Benefits

| Feature | Benefit |
|---------|----------|
| Orchestration | Automates the complete data pipeline |
| Observability | Real-time execution logs |
| Scheduling | Supports automated daily execution |
| Failure Handling | Sensor-based monitoring and alerts |
| Modularity | Easier maintenance and scalability |

---

## 🖼️ Pipeline Evidence

The project includes a successful Dagster execution demonstrating that all pipeline stages completed successfully:

- ✅ Telegram Scraper
- ✅ PostgreSQL Loader
- ✅ dbt Transformations
- ✅ YOLOv8 Image Enrichment

---

## 📊 Business Value

This data platform enables:

- Medical product trend analysis
- Telegram channel performance comparison
- Image-based product classification
- Market intelligence for the Ethiopian healthcare sector

---

## 🚀 Future Improvements

- CI/CD using GitHub Actions
- Fully Dockerized deployment
- Production orchestration with Apache Airflow
- Real-time data ingestion using Apache Kafka
- Advanced NLP for medical entity extraction

---
````
