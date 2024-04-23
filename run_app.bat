SETLOCAL
    CALL activate csrs
    SET database-name=calsim_scenario_database.sqlite
    CALL uvicorn src.csrs.main:app --reload
ENDLOCAL

PAUSE