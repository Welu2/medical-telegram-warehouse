from dagster import ScheduleDefinition

from .jobs import medical_pipeline


daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *",
)