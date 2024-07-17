import argparse
import csv
import logging
from pathlib import Path

import toml

logger = logging.getLogger(__name__)

EXPECTED_COLUMNS = (
    "category",
    "detail",
    "interval",
    "name",
    "path",
    "period_type",
    "units",
)


def file_exists(f: str) -> Path:
    p = Path(f).resolve()
    if not p.exists():
        raise argparse.ArgumentTypeError(f"file {f} not found\n\tresolved to {p}")
    return p


def cli():
    parser = argparse.ArgumentParser(description="Convert fv csv files to toml.")
    parser.add_argument("src", type=file_exists, help="the csv file to convert")
    args = parser.parse_args()
    src: Path = args.src
    dst = src.with_suffix(".toml")
    main(src, dst)


def main(src: Path, dst: Path):
    logging.info(f"reading: {src}")
    with open(src, "r") as SRC:
        content = [v for v in csv.reader(SRC, delimiter=",")]
    total = len(content)
    logging.info(f"{total:,} items in csv")
    column_order = dict()
    header, *content = content
    for i, v in enumerate(header):
        column_order[v] = i
    logging.info(f"column order: {column_order}")
    logging.info(f"writing: {dst}")
    toml_content = list()
    for row in content:
        d = dict()
        for col, idx in column_order.items():
            d[col] = row[idx]
        toml_content.append(d)
    toml_content = {"paths": toml_content}
    with open(dst, "w") as DST:
        toml.dump(toml_content, DST)
    logging.info("done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli()
