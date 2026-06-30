from pathlib import Path
import subprocess
from dagster import (
    op,
    job,
    In,
    Nothing,
    Definitions,
    ScheduleDefinition,
    run_failure_sensor,
    RunFailureSensorContext,
)

ROOT = Path(__file__).parent.resolve()


def run_command(context, command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
    )

    context.log.info(result.stdout)

    if result.stderr:
        context.log.error(result.stderr)

    result.check_returncode()


@op
def scrape_telegram_data(context):
    context.log.info("Starting Telegram scraper...")

    run_command(
        context,
        ["python", "-m", "src.scraper"],
        cwd=ROOT,
    )


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres(context):
    context.log.info("Loading raw data...")

    run_command(
        context,
        ["python", "scripts/load_raw_data.py"],
        cwd=ROOT,
    )


@op(ins={"start": In(Nothing)})
def run_dbt_transformations(context):
    context.log.info("Running dbt...")

    run_command(
        context,
        ["dbt", "run"],
        cwd=ROOT / "medical_warehouse",
    )


@op(ins={"start": In(Nothing)})
def run_yolo_enrichment(context):
    context.log.info("Running YOLO...")

    run_command(
        context,
        ["python", "-m", "src.yolo_detect"],
        cwd=ROOT,
    )


@job
def medical_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)


daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *",
)


@run_failure_sensor
def failure_alert(context: RunFailureSensorContext):
    context.log.error(f"Pipeline failed: {context.dagster_run.run_id}")


defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_schedule],
    sensors=[failure_alert],
)