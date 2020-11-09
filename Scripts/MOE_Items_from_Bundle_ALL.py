TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "PACK NAME"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    DATE(T_II.CLIENT_TIME) AS "DATE",
    T_II.CLIENT_TIME AS "TIME",
    I_EL.NAME AS "INTERACTION",
    T_II.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_EL.NAME AS "ITEM_NAME",
    TO_NUMBER(T_II.EVENT_DATA:item_amount, 20, 0) AS "ITEM_AMOUNT",
    TO_NUMBER(SPLIT_PART(T_II.EVENT_DATA:item_data::STRING, '_', 2), 20, 0) AS "TRANSACTION_ID",
    T_CNTRY.NAME AS "COUNTRY",
    T_IAP.PLATFORM AS "STORE",
    T_IAP.ORIGINAL_CONTENT_ID::STRING AS "PACK_NAME",
    TO_NUMBER (T_IAP.REVENUE_EUR, 10, 2) AS "REVENUE_EUR",
    T_II.FED_ID AS "FED",
    T_II.DATA_CENTER_ID AS "SILO"
FROM "ELEPHANT_DB"."MOE"."ITEM_INTERACTION_RAW" AS T_II
    LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_EL 
    ON (T_II.EVENT_DATA:item_name::INT = T_EL.ID)
    LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS I_EL
    ON (T_II.EVENT_DATA:item_int::INT = I_EL.ID)
    LEFT JOIN "ELEPHANT_DB"."MOE"."IAP" AS T_IAP 
    ON (TO_NUMBER(SPLIT_PART(T_II.EVENT_DATA:item_data::STRING, '_', 2)) = TO_NUMBER(T_IAP.TRANSACTION_ID))
    LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."COUNTRY" AS T_CNTRY 
    ON (T_IAP.COUNTRY = T_CNTRY.CODE)
WHERE
    "TIME" >= '{st_date}'
    AND "TIME" < '{end_date}'
    AND T_II.EVENT_DATA :item_int::INT = 199840
    AND T_IAP.ORIGINAL_CONTENT_ID::STRING LIKE '%{filter_value}%'
ORDER BY ITEM_AMOUNT DESC
LIMIT 10000
;
'''