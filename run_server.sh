# assume that the container already has activated the right environment
# asumme current working directory is at the top level of this repo
gunicorn calsim_scenario_server.main:app