TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "PLAYER_ID"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
    MIN(CLIENT_TIME) AS "FROM",
    MAX(CLIENT_TIME) AS "TO",
    DATA_CENTER_ID AS "SILO",
    EVENT_DATA:realm_id::INT AS "REALM",
    FED_ID AS FED,
    EVENT_DATA:ingame_nickname_active::STRING AS "NAME",
    MAX(EVENT_DATA:progress_index01::INT) AS "CHAMPION LEVEL",
    MAX(EVENT_DATA:progress_index02::INT) AS "CASTLE LEVEL",
    MAX(EVENT_DATA:progress_index03::INT) AS "VIP LEVEL"
FROM "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW"
WHERE
    CLIENT_TIME > '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND event_data:game_player_id::INT = '{filter_value}'
GROUP BY 3,4,5,6
ORDER BY 2 DESC
LIMIT 1000
;
'''