"""
Functions to validate projects before executing/exporting them
"""

from pathlib import Path

from ploomber.spec import DAGSpec


def project(config):
    """
    Verify project has the right structure before running the script.
    This runs as a sanity check in the development machine
    """
    if not Path(config.paths.environment).exists():
        raise FileNotFoundError(
            'Expected a conda "environment.yml" at: {}'.format(
                config.paths.environment))

    # TODO: warn if the environment file does not have pinned versions
    # TODO: warn if the setup.py dependencies (if any), does not have pinned
    # versions

    if config.environment_name is None:
        raise ValueError('Failed to extract the environment name from the '
                         'conda "environment.yaml"')

    pipeline_yaml = Path(config.paths.project, 'pipeline.yaml')
    if not pipeline_yaml.exists():
        raise FileNotFoundError('Expected a "pipeline.yaml" file at: ' +
                                str(pipeline_yaml))

    try:
        # NOTE: should lazy_import be an option from config?
        dag = DAGSpec(pipeline_yaml, lazy_import=True).to_dag()
        # forcing makes it faster because we don't have to check task status
        dag.render(force=True, show_progress=False)
    except Exception as e:
        raise RuntimeError(
            'Failed to initialize DAG from pipeline.yaml') from e

    return dag
