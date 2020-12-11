TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    DATE(T_BaseInt.CLIENT_TIME) AS "DATE",
    T_BaseInt.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Base Interaction' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_BaseInt.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    NULL AS "QNTY",
    T_BaseInt.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    NULL AS "SOURCE/TARGET_ITEM"
    
FROM "ELEPHANT_DB"."MOE"."BASE_INTERACTION_RAW" AS T_BaseInt

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_BaseInt.EVENT_DATA:base_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_BaseInt.EVENT_DATA:item_name::INT = T_Element_2.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_C_Spent.CLIENT_TIME) AS "DATE",
    T_C_Spent.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Currency Spent' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_C_Spent.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_C_Spent.EVENT_DATA:item_number::INT AS "QNTY",
    NULL AS "ITEM_BALANCE",
    T_C_Spent.EVENT_DATA:item_level::INT AS "ITEM_LEVEL",
    T_C_Spent.EVENT_DATA:target_player_id::STRING AS "SOURCE/TARGET_ITEM"

FROM "ELEPHANT_DB"."MOE"."CURRENCY_SPENT_RAW" AS T_C_Spent

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_C_Spent.EVENT_DATA:spend_action::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_C_Spent.EVENT_DATA:item_name::INT = T_Element_2.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_D_Q_P_Int.CLIENT_TIME) AS "DATE",
    T_D_Q_P_Int.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Daily Quest and Project Interaction' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_D_Q_P_Int.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_3.NAME AS "ITEM_NAME",
    T_D_Q_P_Int.EVENT_DATA:item_amount::INT AS "QNTY",
    T_D_Q_P_Int.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    T_Element_2.NAME AS "SOURCE/TARGET_ITEM"
FROM "ELEPHANT_DB"."MOE"."DAILY_QUEST_PROJECT_INTERACTION_RAW" AS T_D_Q_P_Int

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_D_Q_P_Int.EVENT_DATA:quest_action::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_D_Q_P_Int.EVENT_DATA:quest_action::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_D_Q_P_Int.EVENT_DATA:item_name::INT = T_Element_3.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_Hermes.CLIENT_TIME) AS "DATE",
    T_Hermes.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Hermes Message Received' AS "EVENT",
    T_Hermes.EVENT_DATA:gift_source::STRING AS "ACTION",
    T_Hermes.EVENT_DATA:item_name01::INT AS "ITEM_ID",
    T_Element.NAME AS "ITEM_NAME",
    T_Hermes.EVENT_DATA:item_amount01::INT AS "QNTY",
    NULL AS "ITEM_BALANCE",
    T_Hermes.EVENT_DATA:item_level::INT AS "ITEM_LEVEL",
    T_Hermes.EVENT_DATA:gift_source::STRING AS "SOURCE/TARGET_ITEM"

FROM "ELEPHANT_DB"."MOE"."HERMES_MESSAGE_RECEIVED_RAW" AS T_Hermes

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Hermes.EVENT_DATA:item_name01::INT = T_Element.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_Item_Int.CLIENT_TIME) AS "DATE",
    T_Item_Int.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Item Interaction' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_Item_Int.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_3.NAME AS "ITEM_NAME",
    T_Item_Int.EVENT_DATA:item_amount::INT AS "QNTY",
    T_Item_Int.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    T_Item_Int.EVENT_DATA:item_level::INT AS "ITEM_LEVEL",
    T_Item_Int.EVENT_DATA:item_data::STRING AS "SOURCE/TARGET_ITEM"
    
FROM "ELEPHANT_DB"."MOE"."ITEM_INTERACTION_RAW" AS T_Item_Int

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Item_Int.EVENT_DATA:item_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Item_Int.EVENT_DATA:target_item::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_Item_Int.EVENT_DATA:item_name::INT = T_Element_3.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_Lot.CLIENT_TIME) AS "DATE",
    T_Lot.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Lottery Gatcha played' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_Lot.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_Lot.EVENT_DATA:item_amount::INT AS "QNTY",
    T_Lot.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    T_Lot.EVENT_DATA:reward_type::STRING AS "SOURCE/TARGET_ITEM"

FROM "ELEPHANT_DB"."MOE"."LOTTERY_GACHA_PLAYED_RAW" AS T_Lot

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Lot.EVENT_DATA:lottery_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Lot.EVENT_DATA:item_name::INT = T_Element_2.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_R_T_Can.CLIENT_TIME) AS "DATE",
    T_R_T_Can.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Refund Through Cancellation' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_R_T_Can.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_R_T_Can.EVENT_DATA:item_number::INT AS "QNTY",
    NULL AS "ITEM_BALANCE",
    T_R_T_Can.EVENT_DATA:item_level::INT AS "ITEM_LEVEL",
    NULL AS "SOURCE/TARGET_ITEM"

FROM "ELEPHANT_DB"."MOE"."REFUND_THROUGH_CANCELLATION_RAW" AS T_R_T_Can

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_R_T_Can.EVENT_DATA:cancel_option::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_R_T_Can.EVENT_DATA:item_name::INT = T_Element_2.ID)
    
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_Reward.CLIENT_TIME) AS "DATE",
    T_Reward.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Reward Received' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_Reward.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_Reward.EVENT_DATA:item_amount::INT AS "QNTY",
    T_Reward.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    T_Reward.EVENT_DATA:item_data::STRING AS "SOURCE/TARGET_ITEM"

FROM "ELEPHANT_DB"."MOE"."REWARD_RECEIVED_RAW" AS T_Reward

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Reward.EVENT_DATA:reward_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Reward.EVENT_DATA:item_name::INT = T_Element_2.ID)
    
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_Score.CLIENT_TIME) AS "DATE",
    T_Score.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Score Interaction' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_Score.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    1 AS "QNTY",
    T_Score.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    T_Score.EVENT_DATA:event_name::STRING AS "SOURCE/TARGET_ITEM"
    
FROM "ELEPHANT_DB"."MOE"."SCORE_INTERACTION_RAW" AS T_Score

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Score.EVENT_DATA:score_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Score.EVENT_DATA:item_name::INT = T_Element_2.ID)
    
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0
    
UNION ALL

SELECT DISTINCT
    DATE(T_TimeLim.CLIENT_TIME) AS "DATE",
    T_TimeLim.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Time Limited Event Rewards' AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_TimeLim.EVENT_DATA:item_name::INT AS "ITEM_ID",
    T_Element_2.NAME AS "ITEM_NAME",
    T_TimeLim.EVENT_DATA:item_amount::INT AS "QNTY",
    T_TimeLim.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE",
    NULL AS "ITEM_LEVEL",
    T_TimeLim.EVENT_DATA:event_type::STRING AS "SOURCE/TARGET_ITEM"
    
FROM "ELEPHANT_DB"."MOE"."TIME_LIMITED_EVENT_REWARDS_RAW" AS T_TimeLim

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_TimeLim.EVENT_DATA:criteria_actor::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_TimeLim.EVENT_DATA:item_name::INT = T_Element_2.ID)
    
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND "ITEM_ID" <> 0

ORDER BY "TIME" ASC
LIMIT 10000
; 
'''