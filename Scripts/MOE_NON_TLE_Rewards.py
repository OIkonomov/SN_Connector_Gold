TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    DATE(T_RewardsReceived.CLIENT_TIME) AS "DATE",
    T_RewardsReceived.CLIENT_TIME AS "TIME",
    T_RewardsReceived.DATA_CENTER_ID AS "SILO",
    T_RewardsReceived.FED_ID AS "FED",
    T_Element.NAME AS "ACTION",
    T_RewardsReceived.EVENT_DATA:item_data::STRING AS "REWARD_TYPE",
    T_RewardsReceived.EVENT_DATA:hard_currency_earned::INT AS "GOLD_RECEIVED",
    T_RewardsReceived.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_RewardsReceived.EVENT_DATA:item_amount::INT AS "QNTY"
FROM
    MOE.REWARD_RECEIVED_RAW AS T_RewardsReceived
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_RewardsReceived.EVENT_DATA:reward_int::INT = T_Element.ID)
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_RewardsReceived.EVENT_DATA:item_name::INT = T_Element_2.ID)

WHERE
    DATE >= '{st_date}'
    AND DATE < '{end_date}'
    AND FED = '{account}'
ORDER BY TIME ASC
LIMIT 10000
;
'''