import argparse
import os

from .logger import logger


def update_environ_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-name", default="example")
    args = parser.parse_args()
    logger.info(args)
    os.environ["database-name"] = args.database_name


if __name__ == "__main__":
    logger.info(f"running app from {__file__}")

    import uvicorn

    from .main import app

    update_environ_from_args()
    uvicorn.run(app)
