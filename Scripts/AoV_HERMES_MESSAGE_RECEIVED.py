TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''

SELECT
    *
FROM "ELEPHANT_DB"."AOV"."HERMES_MESSAGE_RECEIVED"

WHERE
    SERVER_TIME >= '{st_date}'
    AND SERVER_TIME < '{end_date}'
    AND FED_ID = '{account}'

LIMIT 10000
;
'''