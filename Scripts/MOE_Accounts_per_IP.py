TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "TOP"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    CONCAT(IFNULL(T_PlayerConection.EVENT_DATA:clientip::STRING,SUBSTRING(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))), CHARINDEX(':',try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+')))) + LEN(':'), LEN(try_base64_decode_string(TO_VARCHAR(REPLACE(REPLACE(REPLACE((T_PlayerConection.EVENT_DATA:sessiondata::STRING), '-', '='), '_', '/'),'.','+'))))))) AS IP,
    COUNT(DISTINCT T_PlayerConection.FED_ID) AS "TOTAL_ACCOUNTS"
FROM "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection

WHERE
    T_PlayerConection.CLIENT_TIME >= '{st_date}'
    AND T_PlayerConection.CLIENT_TIME < '{end_date}'
GROUP BY IP
ORDER BY TOTAL_ACCOUNTS DESC
LIMIT {filter_value}
;
'''