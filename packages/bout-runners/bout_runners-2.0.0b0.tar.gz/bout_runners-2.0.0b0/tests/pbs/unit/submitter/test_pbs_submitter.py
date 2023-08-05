"""Contains unittests for the PBS part of the PBS submitter."""


from pathlib import Path

import pytest

from bout_runners.submitter.pbs_submitter import PBSSubmitter
from tests.utils.submitters import (
    add_waiting_for_tester,
    completed_tester,
    submit_command_tester,
)


@pytest.mark.timeout(60)
def test_submit_command(tmp_path: Path) -> None:
    """
    Test that we can submit a command.

    Parameters
    ----------
    tmp_path : Path
        Temporary path (pytest fixture)
    """
    job_name = "PBS_submit_test"
    submitter_class = PBSSubmitter
    submit_command_tester(tmp_path, job_name, submitter_class)


@pytest.mark.timeout(60)
def test_completed(tmp_path: Path) -> None:
    """
    Test the completed function.

    This will test the part of the function which is not tested by normal
    completion

    Parameters
    ----------
    tmp_path : Path
        Temporary path (pytest fixture)
    """
    job_name = "PBS_test_completed"
    submitter_class = PBSSubmitter
    completed_tester(tmp_path, job_name, submitter_class)


@pytest.mark.timeout(60)
def test_add_waiting_for(tmp_path: Path) -> None:
    """
    Test the functionality which adds jobs to wait for.

    Parameters
    ----------
    tmp_path : Path
        Temporary path (pytest fixture)
    """
    # Create first submitter
    job_name = "PBS_test_first_submitter"
    submitter_class = PBSSubmitter
    add_waiting_for_tester(tmp_path, job_name, submitter_class)
