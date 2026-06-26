# Medical Telegram Data Warehouse

## Project Overview

This project builds an end-to-end data pipeline for collecting, transforming, and analyzing data from Ethiopian medical-related Telegram channels.

The pipeline consists of:

- **Task 1:** Telegram data extraction and raw data collection
- **Task 2:** Data transformation and warehouse modeling using PostgreSQL and dbt

The final result is an analytics-ready data warehouse that can support reporting, dashboards, and downstream applications.

---

# Project Architecture

```
Telegram Channels
       │
       ▼
Telethon Scraper
       │
       ▼
Raw Data Lake (JSON + Images)
       │
       ▼
PostgreSQL
       │
       ▼
dbt Transformations
       │
       ▼
Star Schema Data Warehouse
       │
       ▼
Analytics / FastAPI / Dashboards
```

---

# Project Structure

```text
medical-telegram-warehouse/
├── api/
├── data/
│   └── raw/
│       ├── images/
│       └── telegram_messages/
├── logs/
├── medical_warehouse/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
├── src/
│   ├── scraper.py
│   ├── telegram_client.py
│   ├── image_downloader.py
│   ├── logger.py
│   ├── utils.py
│   └── config.py
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Technologies

- Python
- Telethon
- PostgreSQL
- dbt
- FastAPI
- Docker
- GitHub Actions

---

# Task 1 – Data Scraping and Collection

## Objective

Extract Telegram messages and images from Ethiopian medical business channels and store them in a raw data lake.

## Features

- Telegram API integration using Telethon
- Scrapes public Telegram channels
- Extracts:
  - Message ID
  - Date
  - Text
  - View count
  - Forward count
  - Media information
- Downloads images
- Stores raw data as JSON
- Logs scraping activity

## Data Sources

- CheMed
- Lobelia Cosmetics
- Tikvah Pharma
- Additional medical channels from TGStat

## Raw Data Structure

```
data/
└── raw/
    ├── telegram_messages/
    │   └── YYYY-MM-DD/
    │       ├── CheMed123.json
    │       ├── lobelia4cosmetics.json
    │       └── tikvahpharma.json
    │
    └── images/
        ├── CheMed123/
        ├── lobelia4cosmetics/
        └── tikvahpharma/
```

## Running the Scraper

Create a `.env` file:

```env
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+2519XXXXXXXX
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python -m src.scraper
```

---

# Task 2 – Data Modeling and Transformation

## Objective

Transform raw Telegram data into an analytics-ready PostgreSQL warehouse using dbt.

The transformation follows the **Medallion Architecture**.

```
Bronze
    │
    ▼
Silver
    │
    ▼
Gold
```

---

## Bronze Layer

Stores raw Telegram data exactly as collected.

Examples:

- Raw messages
- Raw media metadata

---

## Silver Layer

Data cleaning and standardization.

Transformations include:

- Remove duplicates
- Clean message text
- Standardize timestamps
- Normalize channel names
- Handle missing values

---

## Gold Layer

Analytics-ready dimensional models.

Implemented using a **Star Schema**.

### Fact Table

**fact_messages**

Measures include:

- Views
- Forward count
- Media flag

### Dimension Tables

- dim_channels
- dim_dates
- dim_media

---

## dbt Project Structure

```
medical_warehouse/
├── models/
│   ├── staging/
│   └── marts/
├── tests/
├── dbt_project.yml
└── profiles.yml
```

---

## Running dbt

Install dbt dependencies.

Run models:

```bash
dbt run
```

Run tests:

```bash
dbt test
```

Generate documentation:

```bash
dbt docs generate
```

Serve documentation:

```bash
dbt docs serve
```

---

# Logging

Scraping logs are stored in:

```
logs/scraper.log
```

---

# Environment Variables

Create a `.env` file.

```env
API_ID=
API_HASH=
PHONE_NUMBER=

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

---

# Future Work

- Docker deployment
- FastAPI REST API
- Image classification
- Data quality testing
- CI/CD using GitHub Actions

---
