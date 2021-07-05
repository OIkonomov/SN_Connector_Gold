TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    MIN(CLIENT_TIME),
    MAX(CLIENT_TIME),
    DATA_CENTER_ID AS "SILO",
    FED_ID AS "FED",
    INGAME_NICKNAME_ACTIVE AS "NAME",
    MAX(PROGRESS_INDEX01) AS "LEVEL",
    COUNT(DISTINCT FED_ID)
FROM
    "ELEPHANT_DB"."AOV"."PLAYER_CONNECTION_REPORT"
WHERE
    SERVER_TIME >= '{st_date}'
    AND SERVER_TIME < '{end_date}'
    AND FED = '{account}'
GROUP BY
    FED,
    SILO,
    NAME
ORDER BY
    MAX(CLIENT_TIME) DESC
LIMIT 10000
;
'''