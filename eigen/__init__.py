from dagster import (
    AssetSelection,
    DefaultScheduleStatus,
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

from . import assets

all_assets = load_assets_from_modules([assets])

# Addition: define a job that will materialize the assets
eigen_job = define_asset_job("eigen_job", selection=AssetSelection.all())

eigen_schedule = ScheduleDefinition(
    job=eigen_job,
    cron_schedule="* * * * *",  # every minute
    default_status=DefaultScheduleStatus.RUNNING,
)

io_manager = FilesystemIOManager(
    base_dir="dagster_output",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    # jobs=[eigen_job],  # Addition: add the job to Definitions object (see below)
    schedules=[eigen_schedule],
    resources={
        "io_manager": io_manager,
    },
)
