TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
  DATE(T_Rewards.CLIENT_TIME) AS "DATE",
  T_Rewards.CLIENT_TIME AS "TIME",
  T_Rewards.DATA_CENTER_ID AS "SILO",
  T_Rewards.EVENT_DATA:realm_id_current::INT AS "REALM",
  T_Element_2.NAME AS "INTERACTION",
  T_Rewards.FED_ID AS "FED",
  T_Rewards.USER_ID AS "DEVICE",
  T_Rewards.EVENT_DATA:item_name::INT AS "ITEM_ID",
  T_Element.NAME AS "ITEM_NAME",
  T_Rewards.EVENT_DATA:item_amount::INT AS "QNTY",
  T_Rewards.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
  T_Rewards.EVENT_DATA:hard_currency_earned::INT AS "GOLD_RECEIVED",
  T_Rewards.EVENT_DATA:soft_currency1_earned::INT AS "FOOD_RECEIVED",
  T_Rewards.EVENT_DATA:soft_currency2_earned::INT AS "WOOD_RECEIVED",
  T_Rewards.EVENT_DATA:soft_currency3_earned::INT AS "STONE_RECEIVED",
  T_Rewards.EVENT_DATA:soft_currency4_earned::INT AS "IRON_RECEIVED",
  T_Rewards.EVENT_DATA:soft_currency5_earned::INT AS "SILVER_RECEIVED"
  
FROM
    "ELEPHANT_DB"."MOE"."REWARD_RECEIVED_RAW" AS T_Rewards
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Rewards.EVENT_DATA:item_name::INT = T_Element.ID)
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Rewards.EVENT_DATA:reward_int::INT = T_Element_2.ID)


WHERE
    T_Rewards.CLIENT_TIME >= '{st_date}'
    AND T_Rewards.CLIENT_TIME < '{end_date}'
    AND T_Rewards.FED_ID = '{account}'
    AND T_Rewards.EVENT_DATA:reward_int::INT = '240663'
ORDER BY TIME ASC
LIMIT 5000
;
'''