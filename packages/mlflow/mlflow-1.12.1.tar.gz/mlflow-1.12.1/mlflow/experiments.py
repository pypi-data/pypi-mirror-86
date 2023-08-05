import os

import click
from tabulate import tabulate

from mlflow.data import is_uri
from mlflow.entities import ViewType
from mlflow.tracking import _get_store, fluent

EXPERIMENT_ID = click.option("--experiment-id", "-x", type=click.STRING, required=True)


@click.group("experiments")
def commands():
    """
    Manage experiments. To manage experiments associated with a tracking server, set the
    MLFLOW_TRACKING_URI environment variable to the URL of the desired server.
    """
    pass


@commands.command()
@click.option("--experiment-name", "-n", type=click.STRING, required=True)
@click.option(
    "--artifact-location",
    "-l",
    help="Base location for runs to store artifact results. Artifacts will be stored "
    "at $artifact_location/$run_id/artifacts. See "
    "https://mlflow.org/docs/latest/tracking.html#where-runs-are-recorded for "
    "more info on the properties of artifact location. "
    "If no location is provided, the tracking server will pick a default.",
)
def create(experiment_name, artifact_location):
    """
    Create an experiment.

    All artifacts generated by runs related to this experiment will be stored under artifact
    location, organized under specific run_id sub-directories.

    Implementation of experiment and metadata store is dependent on backend storage. ``FileStore``
    creates a folder for each experiment ID and stores metadata in ``meta.yaml``. Runs are stored
    as subfolders.
    """
    store = _get_store()
    exp_id = store.create_experiment(experiment_name, artifact_location)
    print("Created experiment '%s' with id %s" % (experiment_name, exp_id))


@commands.command("list")
@click.option(
    "--view",
    "-v",
    default="active_only",
    help="Select view type for list experiments. Valid view types are "
    "'active_only' (default), 'deleted_only', and 'all'.",
)
def list_experiments(view):
    """
    List all experiments in the configured tracking server.
    """
    store = _get_store()
    view_type = ViewType.from_string(view) if view else ViewType.ACTIVE_ONLY
    experiments = store.list_experiments(view_type)
    table = [
        [
            exp.experiment_id,
            exp.name,
            exp.artifact_location
            if is_uri(exp.artifact_location)
            else os.path.abspath(exp.artifact_location),
        ]
        for exp in experiments
    ]
    print(tabulate(sorted(table), headers=["Experiment Id", "Name", "Artifact Location"]))


@commands.command("delete")
@EXPERIMENT_ID
def delete_experiment(experiment_id):
    """
    Mark an active experiment for deletion. This also applies to experiment's metadata, runs and
    associated data, and artifacts if they are store in default location. Use ``list`` command to
    view artifact location. Command will throw an error if experiment is not found or already
    marked for deletion.

    Experiments marked for deletion can be restored using ``restore`` command, unless they are
    permanently deleted.

    Specific implementation of deletion is dependent on backend stores. ``FileStore`` moves
    experiments marked for deletion under a ``.trash`` folder under the main folder used to
    instantiate ``FileStore``. Experiments marked for deletion can be permanently deleted by
    clearing the ``.trash`` folder. It is recommended to use a ``cron`` job or an alternate
    workflow mechanism to clear ``.trash`` folder.
    """
    store = _get_store()
    store.delete_experiment(experiment_id)
    print("Experiment with ID %s has been deleted." % str(experiment_id))


@commands.command("restore")
@EXPERIMENT_ID
def restore_experiment(experiment_id):
    """
    Restore a deleted experiment. This also applies to experiment's metadata, runs and associated
    data. The command throws an error if the experiment is already active, cannot be found, or
    permanently deleted.
    """
    store = _get_store()
    store.restore_experiment(experiment_id)
    print("Experiment with id %s has been restored." % str(experiment_id))


@commands.command("rename")
@EXPERIMENT_ID
@click.option("--new-name", type=click.STRING, required=True)
def rename_experiment(experiment_id, new_name):
    """
    Renames an active experiment.
    Returns an error if the experiment is inactive.
    """
    store = _get_store()
    store.rename_experiment(experiment_id, new_name)
    print("Experiment with id %s has been renamed to '%s'." % (experiment_id, new_name))


@commands.command("csv")
@EXPERIMENT_ID
@click.option("--filename", "-o", type=click.STRING)
def generate_csv_with_runs(experiment_id, filename):
    # type: (str, str) -> None
    """
    Generate CSV with all runs for an experiment
    """
    runs = fluent.search_runs(experiment_ids=experiment_id)
    if filename:
        runs.to_csv(filename, index=False)
        print(
            "Experiment with ID %s has been exported as a CSV to file: %s."
            % (experiment_id, filename)
        )
    else:
        print(runs.to_csv(index=False))
