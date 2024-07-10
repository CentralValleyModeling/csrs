import enum
import tomllib
from pathlib import Path

from ..schemas import NamedPath


class PeriodTypeEnum(enum.StrEnum):
    per_aver = "PER-AVER"
    per_cum = "PER-CUM"
    inst_val = "INST-VAL"
    inst_cum = "INST-CUM"


class IntervalEnum(enum.StrEnum):
    mon_1 = "1MON"
    year_1 = "1YEAR"


def standard_paths_factory(src: Path | None = None) -> enum.Enum:
    """Create the StandardPathsEnum from a toml file specification.

    The toml file should be a table with a key "paths" at the top level. The "paths"
    should be an array of  tables. Each table in that array will be treated as the
    kwargs to initialize a NamedPath object. For example, the following content would
    create an enumeration with two NamedPaths:

    ```toml
    [[paths]]
    name="PERDV_CVPAG_SYS"
    path="/CALSIM/PERDV_CVPAG_SYS/PERCENT-DELIVERY/.*/1MON/L2020A/"
    category=""
    units="NONE"
    period_type="PER-AVER"
    interval="1MON"
    detail=""

    [[paths]]
    name="PERDV_CVPMI_SYS"
    path="/CALSIM/PERDV_CVPMI_SYS/PERCENT-DELIVERY/.*/1MON/L2020A/"
    category=""
    units="NONE"
    period_type="PER-AVER"
    interval="1MON"
    detail=""
    ```


    Parameters
    ----------
    src : Path | None, optional
        The path to the toml file, by default None

    Returns
    -------
    enum.Enum
        The constructed enumeration of standard paths

    Raises
    ------
    ValueError
        Raised when the content of the toml file is incorrectly specified.
    """
    if src is None:
        src = Path(__file__).parent / "calsim3-fv.toml"
    with open(src, "rb") as SRC:
        content = tomllib.load(SRC)
    if "paths" not in content:
        raise ValueError("TOML config doesn't contain the anticipated key: paths")
    paths_list: list[dict[str, str]] = content["paths"]
    sentinel = object()  # Construct a new, empty object to use as a hashable default
    all_kwargs = {p.get("name", sentinel): p for p in paths_list}
    if sentinel in all_kwargs:
        raise ValueError("At least one path table is missing the required `name` key.")
    all_path_objects = {k: NamedPath(**v) for k, v in all_kwargs.items()}
    return enum.Enum("StandardPathsEnum", all_path_objects)


StandardPathsEnum = standard_paths_factory()
