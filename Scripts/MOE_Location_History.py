TYPE = "Player"
CREDENTIAL = "Yes"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    DATE(T_PlayerConection.CLIENT_TIME) AS "DATE",
    T_Country.NAME AS "COUNTRY",
    MIN(T_PlayerConection.CLIENT_TIME) AS "LOG_IN",
    MAX(T_PlayerConection.CLIENT_TIME) AS "LOG_OUT",
    T_PlayerConection.USER_ID AS "DEVICE",
    CONCAT(IFNULL(T_PlayerConection.EVENT_DATA:clientip::STRING,SUBSTRING(base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))), CHARINDEX(':',base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+')))) + LEN(':'), LEN(base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))))))) AS IP,
    T_PlayerConection.ANON_ID AS "ANON",
    T_PlayerConection.DATA_CENTER_ID AS "SILO",
    T_PlayerConection.EVENT_DATA:realm_id::INT AS "REALM",
    T_PlayerConection.EVENT_DATA:game_player_id::INT AS "PLAYER_ID",
    T_PlayerConection.FED_ID AS "FED",
    COUNT(DISTINCT T_Country.NAME) OVER() AS "TOTAL_COUNTRIES",
    COUNT(DISTINCT DEVICE) OVER() AS "TOTAL_DEVICES",
    COUNT(DISTINCT IP) OVER() AS "TOTAL_IPs",
    MAX(T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING) AS "NAME",
    MAX(T_PlayerConection.EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
    MAX(T_PlayerConection.EVENT_DATA:all_id::INT) AS "ALLIANCE_ID",
    MAX(T_PlayerConection.EVENT_DATA:all_name_tag::STRING) AS "ALLIANCE_TAG",
    MAX(T_PlayerConection.EVENT_DATA:all_name::STRING) AS "ALLIANCE_NAME",
    MAX(T_PlayerConection.EVENT_DATA:consumable_power_balance::INT) AS "MAX ARMY_MIGHT",
    MAX(T_PlayerConection.EVENT_DATA:permanent_power_balance::INT) AS "MAX CITY_MIGHT",
    "MAX ARMY_MIGHT" + "MAX CITY_MIGHT" AS "MAX TOTAL_MIGHT"
FROM
    "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
LEFT JOIN
    "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW" AS T_InventoryStatus
    ON (DATE(T_PlayerConection.CLIENT_TIME) = DATE(T_InventoryStatus.CLIENT_TIME)
      AND T_PlayerConection.FED_ID = T_InventoryStatus.FED_ID
      AND T_PlayerConection.USER_ID = T_InventoryStatus.USER_ID
      AND T_InventoryStatus.CLIENT_TIME >= '{st_date}'
      AND T_InventoryStatus.CLIENT_TIME < '{end_date}'
      AND T_InventoryStatus.DATA_CENTER_ID LIKE '{silo}'
      AND T_InventoryStatus.FED_ID = '{account}'
     )
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."COUNTRY" AS T_Country
    ON (T_InventoryStatus.COUNTRY = T_Country.CODE)
WHERE
    T_PlayerConection.CLIENT_TIME >= '{st_date}'
    AND T_PlayerConection.CLIENT_TIME < '{end_date}'
    AND SILO LIKE '{silo}'
    AND FED = '{account}'
    AND DEVICE > 0
GROUP BY 1,2,5,6,7,8,9,10,11
ORDER BY LOG_OUT DESC
LIMIT 10000  
;
'''