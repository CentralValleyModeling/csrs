import argparse
import logging
import tomllib
from pathlib import Path

logger = logging.getLogger(__name__)


def file_exists(f: str) -> Path:
    p = Path(f).resolve()
    if not p.exists():
        raise argparse.ArgumentTypeError(f"file {f} not found\n\tresolved to {p}")
    return p


def cli():
    parser = argparse.ArgumentParser(description="Convert fv toml files to csv.")
    parser.add_argument("src", type=file_exists, help="the toml file to convert")
    args = parser.parse_args()
    src: Path = args.src
    dst = src.with_suffix(".csv")
    main(src, dst)


def main(src: Path, dst: Path):
    logging.info(f"reading: {src}")
    with open(src, "rb") as SRC:
        content: dict[str, list[dict]] = tomllib.load(SRC)
    if "paths" not in content:
        raise KeyError(f"required table 'paths' not found in toml: {src}")
    total = len(content["paths"])
    logging.info(f"{total:,} items in toml")
    columns = set()
    for obj in content["paths"]:
        for k in obj:
            columns.add(k)
    columns = sorted(columns)
    logging.info(f"columns found: {columns}")
    logging.info(f"writing: {dst}")
    with open(dst, "w") as DST:
        DST.write(",".join(columns))
        for obj in content["paths"]:
            DST.write("\n")
            for k in columns:
                DST.write(str(obj.get(k, "")) + ",")
    logging.info("done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli()
