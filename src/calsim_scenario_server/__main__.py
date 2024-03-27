import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--database-name", default="example")
args = parser.parse_args()
os.environ["DATABASE_NAME"] = args.database_name

if __name__ == "__main__":
    import uvicorn

    from .main import app

    uvicorn.run(app)
