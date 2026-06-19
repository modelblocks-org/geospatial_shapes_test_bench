"""Quick tests to ensure the workflow is in good health."""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def module_path():
    """Parent directory of the project."""
    return Path(__file__).parent.parent


@pytest.mark.parametrize("scenario", ["EUROPE_S_C1_ADM1"])
def test_snakemake_integration_testing(module_path, scenario):
    """Run a light-weight test for a small-scale scenario."""
    file = f"results/shapes/{scenario}.parquet"
    assert subprocess.run(
        f"snakemake --use-conda --cores 1 --forceall {file}",
        shell=True,
        check=True,
        cwd=module_path,
    )


def test_dry_run(module_path):
    """Execute a dry-run of the module to verify DAG / config health."""
    assert subprocess.run(
        "snakemake --use-conda --cores 1 --dry-run",
        shell=True,
        check=True,
        cwd=module_path,
    )
