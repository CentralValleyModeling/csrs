import sys
from os import remove
from pathlib import Path

import toml

here = Path(__file__).parent
sys.path.append(str((here / "../src").resolve()))
import csrs

DB = here / "dcr.db"


def main(bootstrap_file: Path):

    with open(bootstrap_file, "r", encoding="utf-8") as F:
        data = toml.load(F)

    client = csrs.LocalClient(DB)

    assumption: dict[str, str]
    for assumption in data["assumptions"]:
        result = client.get_assumption(name=assumption["name"])
        assert assumption["detail"] == result[0].detail

    scenario: dict[str, str]
    for scenario in data["scenarios"]:
        result = client.get_scenario(name=scenario["name"])
        assert result[0].version is not None

    run: dict[str, str | bool | list[str]]
    for run in data["runs"]:
        result = client.get_run(scenario=run["scenario"])
        assert result[0].version == result[0].version
        result_ts = client.get_timeseries(
            scenario=run["scenario"],
            version=run["version"],
            path="/CALSIM/SWP_IN_TOTAL/SWP_DELIVERY/.*/1MON/L2020A/",
        )
        df = result_ts.to_frame()
        print(df)


if __name__ == "__main__":
    file = here / "dcr_bootstrap.toml"
    main(file)
