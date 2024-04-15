import sys

sys.path.append("./src")
sys.path.append("./tests")

from tests.fixtures import assert_column_types, assert_columns_given

from calsim_scenario_server.models import ScenarioModel

EXPECTED_COLUMNS = {
    "id": int,
    "name": str,
}


def test_columns():
    assert_columns_given(ScenarioModel, EXPECTED_COLUMNS)


def test_column_types():
    assert_column_types(ScenarioModel, EXPECTED_COLUMNS)
