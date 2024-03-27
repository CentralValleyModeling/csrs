SETLOCAL
CALL conda activate dev_calsim_scenario_server
SET database-name=calsim_scenario_database.sqlite
CALL uvicorn src.calsim_scenario_server.main:app --reload
ENDLOCAL

PAUSE