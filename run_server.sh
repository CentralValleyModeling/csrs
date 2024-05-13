# assume that the container already has activated the right environment
# asumme current working directory is at the top level of this repo
conda init bash
conda activate csrs
uvicorn src.csrs.main:app --host 0.0.0.0 --port 80