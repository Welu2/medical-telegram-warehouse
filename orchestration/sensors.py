from dagster import (
    run_failure_sensor,
    RunFailureSensorContext,
)


@run_failure_sensor
def failure_alert(context: RunFailureSensorContext):

    context.log.error(
        f"Pipeline failed: {context.dagster_run.run_id}"
    )