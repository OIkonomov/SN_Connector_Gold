TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "IP"
SILO = "NO"
REALM = "NO"
DATE = "NO"

SQL_REQ =   '''
SELECT DISTINCT
    T_PlayerConection.DATA_CENTER_ID AS "SILO",
    T_PlayerConection.EVENT_DATA:realm_id::INT AS "REALM",
    T_PlayerConection.FED_ID AS "FED",
    T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING AS "NAME",
    T_Country.NAME AS "COUNTRY",
    MAX(T_PlayerConection.CLIENT_TIME) AS "LAST_SEEN",
    COUNT(DISTINCT FED) OVER() AS "TOTAL_ACCOUNTS",
    CONCAT(IFNULL(T_PlayerConection.EVENT_DATA:clientip::STRING,SUBSTRING(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))), CHARINDEX(':',try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+')))) + LEN(':'), LEN(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))))))) AS IP,
    T_PlayerConection.USER_ID AS "DEVICE",
    T_PlayerConection.ANON_ID AS "ANON",
    T_PlayerConection.EVENT_DATA:game_player_id::INT AS "PLAYER_ID",
    MAX(T_PlayerConection.EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
    MAX(T_PlayerConection.EVENT_DATA:all_id::INT) AS "ALLIANCE_ID",
    MAX(T_PlayerConection.EVENT_DATA:all_name_tag::STRING) AS "ALLIANCE_TAG",
    MAX(T_PlayerConection.EVENT_DATA:all_name::STRING) AS "ALLIANCE_NAME",
    MAX(T_PlayerConection.EVENT_DATA:consumable_power_balance::INT) AS "MAX ARMY_MIGHT",
    MAX(T_PlayerConection.EVENT_DATA:permanent_power_balance::INT) AS "MAX CITY_MIGHT",
    "MAX ARMY_MIGHT" + "MAX CITY_MIGHT" AS "MAX TOTAL_MIGHT"

FROM "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection

LEFT JOIN "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW" AS T_InventoryStatus
      ON (DATE(T_PlayerConection.CLIENT_TIME) = DATE(T_InventoryStatus.CLIENT_TIME)
        AND T_PlayerConection.FED_ID = T_InventoryStatus.FED_ID
        AND T_PlayerConection.USER_ID = T_InventoryStatus.USER_ID
        AND T_InventoryStatus.CLIENT_TIME >= '2020-01-01')

LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."COUNTRY" AS T_Country
    ON (T_InventoryStatus.COUNTRY = T_Country.CODE)
WHERE
    "DEVICE" > 0
    AND T_PlayerConection.CLIENT_TIME > '2020-01-01'
    AND "IP" LIKE '{filter_value}'
GROUP BY 1,2,3,4,5,8,9,10,11
ORDER BY LAST_SEEN DESC
LIMIT 5000
;
'''