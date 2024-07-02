import logging
import os
import sys
import tomllib
from pathlib import Path
from typing import Any

import click

sys.path.append("../src")
import csrs

USER = os.getlogin()
logger = logging.getLogger(__name__)


def load(src: Path, expected_attr: tuple[str, ...]) -> list[dict[str, Any]]:
    logger.info(f"reading {src}")
    with open(src, "rb") as SRC:
        content = tomllib.load(SRC)
    if "objects" not in content:
        content = {"objects": content}
    for obj in content["objects"]:
        for attr in expected_attr:
            if attr not in obj:
                logger.error(f"missing data in toml, missing attr is `{attr}`")
                raise click.BadArgumentUsage(
                    f"toml supplied is missing data: {attr}, {obj}"
                )
        for attr in obj:
            if attr not in expected_attr:
                logger.warning(f"extra data in toml, extra attr is `{attr}`")
    return content["objects"]  # return the array of tables


def assumption(client: csrs.clients.LocalClient, src: Path):
    logger.info("adding assumptions")
    expected = (
        "name",
        "kind",
        "detail",
    )
    content = load(src, expected)
    for o in content:
        logger.info(o)
        client.put_assumption(**o)


def scenario(client: csrs.clients.LocalClient, src: Path):
    logger.info("adding scenarios")
    expected = (
        "name",
        "assumptions",
    )
    content = load(src, expected)
    for o in content:
        logger.info(o)
        client.put_scenario(**o)


def run(client: csrs.clients.LocalClient, src: Path):
    logger.info("adding runs")
    expected = (
        "scenario",
        "version",
        "contact",
        "confidential",
        "published",
        "code_version",
        "detail",
    )
    content = load(src, expected)
    for o in content:
        logger.info(o)
        client.put_run(**o)


def timseries(client: csrs.clients.LocalClient, src: Path):
    logger.info("adding timeseries")
    expected = (
        "scenario",
        "version",
        "dss",
        "paths",
    )
    content = load(src, expected)
    for o in content:
        logger.info(o)
        client.put_many_timeseries(**o)


def path(client: csrs.clients.LocalClient, src: Path):
    logger.info("adding path")
    expected = (
        "name",
        "path",
        "category",
        "detail",
        "period_type",
        "interval",
        "units",
    )
    content = load(src, expected)
    for o in content:
        logger.info(o)
        client.put_path(**o)


TABLES = {
    "assumption": assumption,
    "scenario": scenario,
    "run": run,
    "timeseries": timseries,
    "path": path,
}


@click.command()
@click.option(
    "--kind",
    type=click.Choice(TABLES),
    required=True,
    help="The kind of object to be created.",
)
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.option("--dst", nargs=1, type=click.Path(), default=f"csrs-{USER}.db")
def cli(kind: str, src: Path, dst: Path) -> tuple[str, Path]:
    src = Path(src).resolve()
    dst = Path(dst).resolve()
    logger.info(f"Adding {kind} to {dst}")
    logger.info(f"{src=}")
    client = csrs.LocalClient(dst)
    return TABLES[kind](client, src)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    cli()
