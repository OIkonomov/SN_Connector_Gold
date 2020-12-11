TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
    MIN(T_InventoryStatus.SERVER_TIME) AS "LOG_IN",
    MAX(T_InventoryStatus.SERVER_TIME) AS "LOG_OUT",
    T_PlayerConection.ANON_ID AS "ANON",
    T_InventoryStatus.USER_ID AS "DEVICE",
    T_InventoryStatus.COUNTRY AS "COUNTRY",
    T_InventoryStatus.EVENT_DATA:ingame_nickname_active::STRING AS "NAME",
    T_InventoryStatus.DATA_CENTER_ID AS "SILO",
    T_InventoryStatus.EVENT_DATA:realm_id::INT AS "REALM",
    T_InventoryStatus.FED_ID AS "FED"
    
FROM "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW" AS T_InventoryStatus

LEFT JOIN
    "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
    ON (T_InventoryStatus.USER_ID = T_PlayerConection.USER_ID
       AND T_PlayerConection.CLIENT_TIME >= '{st_date}'
       AND T_PlayerConection.CLIENT_TIME < '{end_date}'
       AND T_PlayerConection.FED_ID = '{account}')

WHERE
    T_InventoryStatus.SERVER_TIME > '{st_date}'
    AND T_InventoryStatus.SERVER_TIME < '{end_date}'
    AND T_InventoryStatus.FED_ID = '{account}'
    
GROUP BY
    3,4,5,6,7,8,9
ORDER BY
    LOG_OUT DESC
LIMIT 1000
;
'''