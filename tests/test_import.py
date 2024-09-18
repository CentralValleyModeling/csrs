import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def test_import():
    cur_dir = Path(".").resolve()
    logger.info(f"{cur_dir=}")
    new_dir = cur_dir / "foo/bar/baz"
    new_dir.mkdir(parents=True)
    try:
        os.chdir(new_dir)
        import csrs
    except Exception as e:
        assert e is None
    finally:
        os.chdir(cur_dir)
        new_dir.rmdir()
