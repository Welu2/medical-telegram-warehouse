FROM python:3.12-slim

WORKDIR /app

# system deps (important for dbt, postgres, opencv, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# default command (Dagster UI)
CMD ["dagster", "dev", "-f", "pipeline.py", "-h", "0.0.0.0", "-p", "3000"]