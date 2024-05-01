import sys
from os import remove
from pathlib import Path

import toml

here = Path(__file__).parent
sys.path.append(str((here / "../src").resolve()))
import csrs

DB = here / "dcr.db"
if DB.exists():
    remove(DB)


def main(bootstrap_file: Path):

    with open(bootstrap_file, "r", encoding="utf-8") as F:
        data = toml.load(F)

    client = csrs.LocalClient(DB)

    assumption: dict[str, str]
    for assumption in data["assumptions"]:
        client.put_assumption(**assumption)

    scenario: dict[str, str]
    for scenario in data["scenarios"]:
        client.put_scenario(**scenario)

    run: dict[str, str | bool | list[str]]
    for run in data["runs"]:
        dss: str = run.pop("dss_to_upload")
        client.put_run(**run)

        client.put_many_timeseries(
            scenario=run["scenario"],
            version=run["version"],
            dss=Path(dss),
        )


if __name__ == "__main__":
    file = here / "dcr_bootstrap.toml"
    main(file)
