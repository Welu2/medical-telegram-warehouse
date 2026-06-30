from dagster import job

from .ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment,
)


@job
def medical_pipeline():

    scrape = scrape_telegram_data()

    load = load_raw_to_postgres()

    dbt = run_dbt_transformations()

    yolo = run_yolo_enrichment()

    scrape >> load >> dbt >> yolo