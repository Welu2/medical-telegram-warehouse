from dagster import op
import subprocess


@op
def scrape_telegram_data(context):
    context.log.info("Starting Telegram scraping...")

    subprocess.run(
        ["python", "src/scraper.py"],
        check=True
    )

    context.log.info("Scraping completed.")


@op
def load_raw_to_postgres(context):
    context.log.info("Loading raw data into PostgreSQL...")

    subprocess.run(
        ["python", "src/load_to_postgres.py"],
        check=True
    )

    context.log.info("Loading completed.")


@op
def run_dbt_transformations(context):
    context.log.info("Running dbt models...")

    subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        check=True
    )

    context.log.info("dbt finished.")


@op
def run_yolo_enrichment(context):
    context.log.info("Running YOLO detection...")

    subprocess.run(
        ["python", "src/yolo_detector.py"],
        check=True
    )

    context.log.info("YOLO completed.")