from dagster import Definitions

from .jobs import medical_pipeline
from .schedules import daily_schedule
from .sensors import failure_alert

defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_schedule],
    sensors=[failure_alert],
)