TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    DATE(T_RewardsReceived.CLIENT_TIME) AS DATE,
    T_RewardsReceived.CLIENT_TIME AS DATE_TIME,
    T_Platform.NAME AS PLATFORM,
    T_RewardsReceived.DATA_CENTER_ID AS SILO,
    T_RewardsReceived.FED_ID AS FED,
    T_Element.NAME AS INTERACTION,
    T_RewardsReceived.EVENT_DATA:item_data::STRING AS REWARD_TYPE,
    T_RewardsReceived.EVENT_DATA:hard_currency_earned::INT AS GOLD_RECEIVED,
    T_RewardsReceived.EVENT_DATA:item_name::INT AS ITEM_ID,
    T_Element_2.NAME AS ITEM_NAME
FROM 
    MOE.REWARD_RECEIVED_RAW AS T_RewardsReceived
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."PLATFORM" AS T_Platform
    ON (T_RewardsReceived.GAME_ID::INT = T_Platform.GGI)
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_RewardsReceived.EVENT_DATA:reward_int::INT = T_Element.ID)
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_RewardsReceived.EVENT_DATA:item_name::INT = T_Element_2.ID)

WHERE
    DATE_TIME > '{st_date}'
      AND DATE_TIME < '{end_date}'
      AND SILO LIKE '{silo}'
      AND FED = '{account}'
      AND T_RewardsReceived.EVENT_DATA:reward_int::INT = 361324
ORDER BY 2,7
LIMIT 1000
;
'''