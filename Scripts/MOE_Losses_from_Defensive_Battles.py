TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
    BATTLE_TARGET,
    PLAYER_LOST_UNITS:l::STRING AS "LOST",
    PLAYER_LOST_UNITS:w::STRING AS "WOUNDED",
    RESOURCES_STOLEN AS "RESOURCES",
    COUNT(DISTINCT COMBAT_ID) AS "TOTAL_BATTLES"

FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION"

WHERE 
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'

GROUP BY 
    BATTLE_TARGET, 
    LOST, 
    WOUNDED, 
    RESOURCES

LIMIT 10000
;
'''