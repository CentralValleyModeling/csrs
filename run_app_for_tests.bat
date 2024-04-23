SETLOCAL
    CALL activate csrs
    SET database-name=test.sqlite
    SET database-dir=.\tests\db
    SET log-level=1
    CALL uvicorn csrs.main:app --reload
ENDLOCAL

RMDIR ".\tests\db" /S /Q
PAUSE