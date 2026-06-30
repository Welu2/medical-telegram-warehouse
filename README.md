# 📦 Medical Telegram Data Warehouse

An end-to-end data engineering pipeline that extracts medical product data from Ethiopian Telegram channels, transforms it using dbt, enriches image data with YOLOv8 object detection, stores the results in PostgreSQL, and exposes analytics through a FastAPI REST API.

---

# 🚀 Project Overview

This project builds a modern ELT data platform for analyzing Ethiopian medical Telegram channels such as:

* CheMed
* Lobelia Cosmetics
* Tikvah Pharma
* Other public medical-related Telegram channels

The pipeline consists of four major tasks:

* **Task 1:** Telegram data extraction and raw data collection
* **Task 2:** Data transformation and warehouse modeling with PostgreSQL and dbt
* **Task 3:** Image enrichment using YOLOv8 object detection
* **Task 4:** FastAPI analytical API

The platform provides insights into:

* Top mentioned medical products
* Product availability trends
* Image versus text content
* Channel activity
* Image object detection results

---

# 🏗️ Project Architecture

```text
Telegram Channels
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

# 📁 Project Structure

```text
medical-telegram-warehouse/
│
├── api/
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── __pycache__/
│
├── data/
│   ├── raw/
│   └── yolo_results.csv
│
├── logs/
│
├── medical_warehouse/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── seeds/
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── src/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# ⚙️ Technology Stack

* Python
* PostgreSQL
* Telethon
* dbt
* FastAPI
* SQLAlchemy
* Ultralytics YOLOv8
* OpenCV
* Docker

---

# Task 1 – Telegram Data Extraction

## Objective

Collect messages and images from Ethiopian medical Telegram channels.

## Features

* Scrapes public Telegram channels
* Downloads images
* Stores raw messages as JSON
* Preserves message metadata
* Logging support

## Extracted Data

* Message ID
* Date
* Channel
* Message text
* Views
* Forward count
* Media information

## Run the Scraper

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+251XXXXXXXXX
```

Run:

```bash
python src/scraper.py
```

---

# Task 2 – Data Warehouse with dbt

## Objective

Transform raw Telegram data into an analytics-ready PostgreSQL warehouse.

## Warehouse Layers

### Bronze

Stores raw Telegram data.

### Silver

Performs:

* Duplicate removal
* Text cleaning
* Timestamp normalization
* Missing value handling

### Gold

Analytics-ready Star Schema.

## Core Models

### Staging

* stg_telegram_messages
* stg_yolo_detections

### Dimensions

* dim_channels
* dim_dates

### Facts

* fct_messages
* fct_product_mentions
* fct_image_detections

## Run dbt

```bash
cd medical_warehouse

dbt run
```

Run tests:

```bash
dbt test
```

Generate documentation:

```bash
dbt docs generate
dbt docs serve
```

---

# Task 3 – Data Enrichment with YOLO Object Detection

## Objective

Enrich Telegram images using the Ultralytics YOLOv8 Nano object detection model.

## Features

* Detects objects in Telegram images
* Records confidence scores
* Categorizes images into:

  * Promotional
  * Product Display
  * Lifestyle
  * Other
* Loads detection results into PostgreSQL
* Integrates image analytics with Telegram messages

## Installation

```bash
pip install ultralytics
pip install opencv-python
```

## Run Detection

```bash
python src/yolo_detect.py
```

## Load Detection Results

```sql
CREATE TABLE analytics.raw_yolo_detections (
    message_id BIGINT,
    objects TEXT,
    confidence_score FLOAT,
    image_category TEXT
);
```

```sql
\copy analytics.raw_yolo_detections
FROM 'data/yolo_results.csv'
DELIMITER ','
CSV HEADER;
```

Rebuild the warehouse:

```bash
dbt run
dbt test
```

## Example Analytics

Average engagement by image category:

```sql
SELECT
    image_category,
    AVG(view_count) AS avg_views
FROM analytics.fct_image_detections
GROUP BY image_category
ORDER BY avg_views DESC;
```

Channel image usage:

```sql
SELECT
    channel_key,
    COUNT(*) AS image_posts
FROM analytics.fct_image_detections
GROUP BY channel_key
ORDER BY image_posts DESC;
```

---

# Task 4 – Analytical API

## Objective

Provide REST endpoints for querying warehouse analytics.

## Run FastAPI

```bash
uvicorn api.main:app --reload --port 8001
```

Swagger documentation:

```
http://localhost:8001/docs
```

## Available Endpoints

### Top Products

```
GET /api/reports/top-products?limit=10
```

Returns the most frequently mentioned products.

### Channel Activity

```
GET /api/channels/{channel_name}/activity
```

Returns posting activity and engagement statistics.

### Search Messages

```
GET /api/search/messages?query=paracetamol
```

Searches Telegram messages for a keyword.

### Visual Content Analysis

```
GET /api/reports/visual-content
```

Returns statistics generated from YOLO image detection.

---

# 🧪 Environment Variables

Create a `.env` file.

```env
API_ID=
API_HASH=
PHONE_NUMBER=

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=medical_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

---

# 📊 Key Features

* End-to-end ELT pipeline
* Telegram data collection
* PostgreSQL data warehouse
* dbt transformations
* Star schema design
* YOLOv8 image enrichment
* Product mention analytics
* FastAPI REST API
* SQL analytics

---

# 📈 Results

* Telegram data successfully collected from medical channels
* Analytics-ready PostgreSQL warehouse built using dbt
* YOLOv8 object detection integrated with message data
* Image categories generated for downstream analysis
* FastAPI endpoints expose warehouse analytics
* Modular architecture supporting future expansion

---

# 🚀 Future Improvements

* Dagster orchestration
* CI/CD with GitHub Actions
* Docker deployment
* Streamlit or Power BI dashboards
* NLP-based medical entity extraction
* Automated data quality monitoring
