from dagster import (AssetSelection, Definitions, ScheduleDefinition,
                     define_asset_job, load_assets_from_modules)

from . import assets

all_assets = load_assets_from_modules([assets])

# Addition: define a job that will materialize the assets
eigen_job = define_asset_job("eigen_job", selection=AssetSelection.all())

eigen_schedule = ScheduleDefinition(
    job=eigen_job,
    cron_schedule="0 * * * *",  # every hour
)

defs = Definitions(
    assets=all_assets,
    # jobs=[eigen_job],  # Addition: add the job to Definitions object (see below)
    schedules=[eigen_schedule],
)
