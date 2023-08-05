"""Contains PBS unit tests for the runner."""


from pathlib import Path

import pytest

from bout_runners.submitter.pbs_submitter import PBSSubmitter
from tests.utils.submitters import submitter_graph_tester


@pytest.mark.timeout(60)
def test_pure_pbs_graph(tmp_path: Path):
    """
    Test dependency with several PBS nodes.

    Parameters
    ----------
    tmp_path : Path
        Temporary path (pytest fixture)
    """
    job_name = "PBS_test_pure_pbs_runner"
    submitter_class = PBSSubmitter
    submitter_graph_tester(tmp_path, job_name, submitter_class, local_node_two=False)


@pytest.mark.timeout(60)
def test_mixed_pbs_graph(tmp_path: Path):
    """
    Test dependency with several PBS and local nodes.

    Parameters
    ----------
    tmp_path : Path
        Temporary path (pytest fixture)
    """
    job_name = "PBS_test_mixed_pbs_runner"
    submitter_class = PBSSubmitter
    submitter_graph_tester(tmp_path, job_name, submitter_class, local_node_two=True)
