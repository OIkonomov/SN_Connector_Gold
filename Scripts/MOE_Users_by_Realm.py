TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "NO"
SILO = "YES"
REALM = "YES"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    MAX(CLIENT_TIME) AS LAST_SEEN,
    DATA_CENTER_ID AS "SILO",
    EVENT_DATA:realm_id::INT AS "REALM",
    EVENT_DATA:game_player_id::INT AS "PLAYER_ID",
    FED_ID AS "FED",
    USER_ID AS "DEVICE",
    ANON_ID AS "ANON_ID",
    CONCAT(IFNULL(T_PlayerConection.EVENT_DATA:clientip::STRING,SUBSTRING(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))), CHARINDEX(':',try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+')))) + LEN(':'), LEN(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))))))) AS IP,
    COUNT(DISTINCT FED) OVER(PARTITION BY DEVICE) AS "TOTAL_ACC_PER_DEVICE",
    COUNT(DISTINCT FED) OVER(PARTITION BY IP) AS "TOTAL_ACC_PER_IP",
    MAX(EVENT_DATA:ingame_nickname_active::STRING) AS "NAME",
    MAX(EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
    MAX(EVENT_DATA:all_id::INT) AS "ALLIANCE_ID",
    MAX(EVENT_DATA:all_name_tag::STRING) AS "ALLIANCE_TAG",
    MAX(EVENT_DATA:all_name::STRING) AS "ALLIANCE_NAME",
    MAX(EVENT_DATA:consumable_power_balance::INT) AS "ARMY_MIGHT",
    MAX(EVENT_DATA:permanent_power_balance::INT) AS "CITY_MIGHT",
    ARMY_MIGHT + CITY_MIGHT AS "TOTAL_MIGHT"
FROM
    "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
WHERE 
    CLIENT_TIME >= '{st_date}'
      AND CLIENT_TIME < '{end_date}'
      AND "SILO" LIKE '{silo}'
      AND "REALM" = '{realm}'
      AND "DEVICE" > 0
GROUP BY SILO, REALM, IP, PLAYER_ID, FED, DEVICE, ANON_ID
ORDER BY TOTAL_ACC_PER_IP DESC, TOTAL_ACC_PER_DEVICE DESC, DEVICE ASC, FED ASC, LAST_SEEN DESC
LIMIT 100000
;
'''