TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "NAME"
SILO = "YES"
REALM = "YES"
DATE = "YES"

SQL_REQ =   '''
SELECT
    MAX(T_PlayerConection.CLIENT_TIME) AS "LAST_SEEN",
    MAX(T_PlayerConection.EVENT_DATA:clientip::STRING) AS "LAST_IP",
    T_Country.NAME AS COUNTRY,
    T_PlayerConection.FED_ID AS "FED",
    T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING AS "NAME",
    T_PlayerConection.USER_ID AS "DEVICE",
    T_PlayerConection.DATA_CENTER_ID AS "SILO",
    T_PlayerConection.EVENT_DATA:realm_id::INT AS "REALM",
    MAX(T_PlayerConection.EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
    MAX(T_PlayerConection.EVENT_DATA:all_id::INT) AS "ALLIANCE_ID",
    MAX(T_PlayerConection.EVENT_DATA:all_name_tag::STRING) AS "ALLIANCE_TAG",
    MAX(T_PlayerConection.EVENT_DATA:all_name::STRING) AS "ALLIANCE_NAME",
    MAX(T_PlayerConection.EVENT_DATA:consumable_power_balance::INT) AS "MAX ARMY_MIGHT",
    MAX(T_PlayerConection.EVENT_DATA:permanent_power_balance::INT) AS "MAX CITY_MIGHT",
    "MAX ARMY_MIGHT" + "MAX CITY_MIGHT" AS "MAX TOTAL_MIGHT",
    T_PlayerConection.EVENT_DATA:game_player_id::INT AS "PLAYER_ID"
FROM
    "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
    INNER JOIN
        "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW" AS T_InventoryStatus
    ON (DATE(T_PlayerConection.CLIENT_TIME) = DATE(T_InventoryStatus.CLIENT_TIME)
        AND T_PlayerConection.FED_ID = T_InventoryStatus.FED_ID
        AND T_PlayerConection.USER_ID = T_InventoryStatus.USER_ID
        AND T_InventoryStatus.CLIENT_TIME > '{st_date}'
        AND T_InventoryStatus.CLIENT_TIME < '{end_date}'
        AND T_InventoryStatus.DATA_CENTER_ID LIKE '{silo}'
       )
    INNER JOIN
    "ELEPHANT_DB"."DIMENSIONS"."COUNTRY" AS T_Country
    ON (T_InventoryStatus.COUNTRY = T_Country.CODE)
WHERE
    T_PlayerConection.CLIENT_TIME > '{st_date}'
    AND T_PlayerConection.CLIENT_TIME < '{end_date}'
    AND SILO LIKE '{silo}'
    AND REALM = {realm}
    AND LOWER(T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING) LIKE LOWER('%{filter_value}%')
    AND DEVICE > 0

GROUP BY 3,4,5,6,7,8,16
ORDER BY LAST_SEEN DESC
LIMIT 1000
;
'''