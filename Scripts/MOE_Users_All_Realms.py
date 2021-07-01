TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "MORE THAN X ACCOUNTS PER IP"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    LAST_SEEN,
    SILO,
    REALM,
    D_PLATFORM,
    IP,
    TOTAL_ACC_PER_IP,
    DEVICE,
    COUNT(DISTINCT FED) OVER(PARTITION BY DEVICE) AS "TOTAL_ACC_PER_DEVICE",
    D_MODEL,
    D_FWR,
    FED,
    ARMY_MIGHT,
    ANON_ID,
    PLAYER_ID,
    NAME,
    CASTLE_LEVEL,
    ALLIANCE_ID,
    ALLIANCE_TAG,
    ALLIANCE_NAME
    
FROM
    (SELECT DISTINCT
        T_PlayerConection.FED_ID AS "FED",
        T_PlayerConection.DATA_CENTER_ID AS "SILO",
        T_PlayerConection.CLIENT_TIME AS "DATE_TIMES",
        LAST_VALUE(DATE_TIMES) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "LAST_SEEN",
        T_PlayerConection.EVENT_DATA:realm_id::INT AS "REALMS",
        LAST_VALUE(REALMS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "REALM",
        CONCAT(IFNULL(T_PlayerConection.EVENT_DATA:clientip::STRING,SUBSTRING(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))), CHARINDEX(':',try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+')))) + LEN(':'), LEN(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))))))) AS IP,
        T_PlayerConection.USER_ID AS "DEVICES",
        LAST_VALUE(DEVICES) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "DEVICE",
        T_Platform.NAME AS "D_PLATFORMS",
        LAST_VALUE(D_PLATFORMS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "D_PLATFORM",
        T_Device.DEVICE_NAME AS "D_MODELS",
        LAST_VALUE(D_MODELS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "D_MODEL",
        T_Device.FIRMWARE::STRING AS "D_FWRS",
        LAST_VALUE(D_FWRS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "D_FWR",
        T_PlayerConection.ANON_ID AS "ANON_IDS",
        LAST_VALUE(ANON_IDS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "ANON_ID",
        T_PlayerConection.EVENT_DATA:game_player_id::INT AS "PLAYER_IDS",
        LAST_VALUE(PLAYER_IDS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "PLAYER_ID",
        COUNT(DISTINCT FED) OVER(PARTITION BY IP) AS "TOTAL_ACC_PER_IP",
        T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING AS "NAMES",
        LAST_VALUE(NAMES) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "NAME",
        T_PlayerConection.EVENT_DATA:progress_index02::INT AS "CASTLE_LEVELS",
        LAST_VALUE(CASTLE_LEVELS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "CASTLE_LEVEL",
        T_PlayerConection.EVENT_DATA:all_id::INT AS "ALLIANCE_IDS",
        LAST_VALUE(ALLIANCE_IDS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "ALLIANCE_ID",
        T_PlayerConection.EVENT_DATA:all_name_tag::STRING AS "ALLIANCE_TAGS",
        LAST_VALUE(ALLIANCE_TAGS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "ALLIANCE_TAG",
        T_PlayerConection.EVENT_DATA:all_name::STRING AS "ALLIANCE_NAMES",
        LAST_VALUE(ALLIANCE_NAMES) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "ALLIANCE_NAME",
        T_PlayerConection.EVENT_DATA:consumable_power_balance::INT AS "ARMY_MIGHTS",
        LAST_VALUE(ARMY_MIGHTS) OVER (PARTITION BY FED ORDER BY DATE_TIMES) AS "ARMY_MIGHT"
    FROM
        "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
    LEFT JOIN 
        "ELEPHANT_DB"."DIMENSIONS"."PLATFORM" AS T_Platform
        ON (T_PlayerConection.EVENT_DATA:client_platform::INT = T_Platform.GGI)
    LEFT JOIN 
        "ELEPHANT_DB"."MOE"."USER_DEVICE_INFO" AS T_Device
        ON (T_PlayerConection.USER_ID = T_Device.USER_ID)

    WHERE 
        T_PlayerConection.CLIENT_TIME >= '{st_date}'
          AND T_PlayerConection.CLIENT_TIME < '{end_date}'
          AND "SILO" LIKE '{silo}'
          AND "DEVICES" > 0
    GROUP BY 
              DATE_TIMES,
              SILO, 
              REALMS, 
              FED, 
              IP, 
              D_PLATFORMS, 
              D_MODELS, 
              DEVICES, 
              D_FWRS,
              ANON_IDS,
              PLAYER_IDS, 
              D_FWRS,
              NAMES,
              ALLIANCE_IDS,
              ALLIANCE_TAGS,
              ALLIANCE_NAMES,
              ARMY_MIGHTS,
              CASTLE_LEVELS

    ORDER BY TOTAL_ACC_PER_IP DESC, ARMY_MIGHT DESC
    LIMIT 100000) AS T_GROUPED

GROUP BY
    LAST_SEEN,
    SILO,
    REALM,
    D_PLATFORM,
    IP,
    TOTAL_ACC_PER_IP,
    DEVICE,
    D_MODEL,
    D_FWR,
    FED,
    ARMY_MIGHT,
    ANON_ID,
    PLAYER_ID,
    NAME,
    CASTLE_LEVEL,
    ALLIANCE_ID,
    ALLIANCE_TAG,
    ALLIANCE_NAME

HAVING TOTAL_ACC_PER_IP >= {filter_value}

ORDER BY TOTAL_ACC_PER_IP DESC, DEVICE ASC, ARMY_MIGHT DESC
    
;

'''