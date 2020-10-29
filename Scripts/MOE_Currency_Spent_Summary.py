TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    DATE(T_CurrencySpent.CLIENT_TIME) AS "DATE",
    T_CurrencySpent.DATA_CENTER_ID AS "SILO",
    T_CurrencySpent.COUNTRY AS "COUNTRY",
    T_CurrencySpent.USER_ID AS "DEVICE",
    T_CurrencySpent.FED_ID AS "FED",
    T_Element_2.NAME AS "ACTION",
    SUM(EVENT_DATA:item_number::INT) AS "QNTY",
    T_CurrencySpent.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_1.NAME AS "ITEM_NAME",
    SUM(EVENT_DATA:hard_currency_spent::INT) AS "GOLD_SPENT",
    SUM(EVENT_DATA:soft_currency1_spent::INT) AS "FOOD_SPENT",
    SUM(EVENT_DATA:soft_currency2_spent::INT) AS "WOOD_SPENT",
    SUM(EVENT_DATA:soft_currency3_spent::INT) AS "STONE_SPENT",
    SUM(EVENT_DATA:soft_currency4_spent::INT) AS "IRON_SPENT",
    SUM(EVENT_DATA:soft_currency5_spent::INT) AS "SILVER_SPENT",
    SUM(EVENT_DATA:soft_currency7_spent::INT) AS "DUCATS_SPENT"
FROM "ELEPHANT_DB"."MOE"."CURRENCY_SPENT_RAW" AS T_CurrencySpent
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_1
    ON (T_CurrencySpent.EVENT_DATA:item_name::INT = T_Element_1.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_CurrencySpent.EVENT_DATA:spend_action::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_CurrencySpent.EVENT_DATA:item_name::INT = T_Element_3.ID)
WHERE 
    DATA_CENTER_ID LIKE '{silo}'
    AND CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
GROUP BY DATE,ACTION,ITEM_ID,ITEM_NAME,SILO,COUNTRY,DEVICE,FED
ORDER BY DATE,ACTION,ITEM_NAME ASC
LIMIT 5000
;
'''