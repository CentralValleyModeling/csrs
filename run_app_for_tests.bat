SETLOCAL
    CALL activate dev_calsim_scenario_server
    SET database-name=test.sqlite
    SET database-dir=.\tests\db
    SET log-level=1
    CALL uvicorn src.calsim_scenario_server.main:app --reload
ENDLOCAL

RMDIR ".\tests\db" /S /Q
PAUSE