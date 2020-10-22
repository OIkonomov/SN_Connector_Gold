TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    T_BaseInt.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Base Interaction' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    NULL AS "Quantity",
    T_BaseInt.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    NULL AS "Source/TargetItem"
    
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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    
UNION ALL

SELECT DISTINCT
    T_C_Spent.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Currency Spent' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    T_C_Spent.EVENT_DATA:item_number::INT AS "Quantity",
    NULL AS "ItemBalance",
    T_C_Spent.EVENT_DATA:item_level::INT AS "ItemLevel",
    T_C_Spent.EVENT_DATA:target_player_id::STRING AS "Source/TargetItem"

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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_D_Q_P_Int.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Daily Quest and Project Interaction' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_3.NAME AS "ItemID",
    T_D_Q_P_Int.EVENT_DATA:item_amount::INT AS "Quantity",
    T_D_Q_P_Int.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    T_Element_2.NAME AS "Source/TargetItem"
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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_Hermes.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Hermes Message Received' AS "EVENT",
    T_Hermes.EVENT_DATA:gift_source::STRING AS "Interaction",
    T_Element.NAME AS "ItemID",
    T_Hermes.EVENT_DATA:item_amount01::INT AS "Quantity",
    NULL AS "ItemBalance",
    T_Hermes.EVENT_DATA:item_level::INT AS "ItemLevel",
    T_Hermes.EVENT_DATA:gift_source::STRING AS "Source/TargetItem"

FROM "ELEPHANT_DB"."MOE"."HERMES_MESSAGE_RECEIVED_RAW" AS T_Hermes

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Hermes.EVENT_DATA:item_name01::INT = T_Element.ID)

WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_Item_Int.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Item Interaction' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_3.NAME AS "ItemID",
    T_Item_Int.EVENT_DATA:item_amount::INT AS "Quantity",
    T_Item_Int.EVENT_DATA:item_balance::INT AS "ItemBalance",
    T_Item_Int.EVENT_DATA:item_level::INT AS "ItemLevel",
    T_Item_Int.EVENT_DATA:item_data::STRING AS "Source/TargetItem"
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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_Lot.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Lottery Gatcha played' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    T_Lot.EVENT_DATA:item_amount::INT AS "Quantity",
    T_Lot.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    T_Lot.EVENT_DATA:reward_type::STRING AS "Source/TargetItem"

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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_R_T_Can.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Refund Through Cancellation' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    T_R_T_Can.EVENT_DATA:item_number::INT AS "Quantity",
    NULL AS "ItemBalance",
    T_R_T_Can.EVENT_DATA:item_level::INT AS "ItemLevel",
    NULL AS "Source/TargetItem"

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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_Reward.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Reward Received' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    T_Reward.EVENT_DATA:item_amount::INT AS "Quantity",
    T_Reward.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    T_Reward.EVENT_DATA:item_data::STRING AS "Source/TargetItem"

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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_Score.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Score Interaction' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    NULL AS "Quantity",
    T_Score.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    T_Score.EVENT_DATA:event_name::STRING AS "Source/TargetItem"
    
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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL
    
UNION ALL

SELECT DISTINCT
    T_TimeLim.CLIENT_TIME AS "TIME",
    FED_ID AS "FED",
    'Time Limited Event Rewards' AS "EVENT",
    T_Element.NAME AS "Interaction",
    T_Element_2.NAME AS "ItemID",
    T_TimeLim.EVENT_DATA:item_amount::INT AS "Quantity",
    T_TimeLim.EVENT_DATA:item_balance::INT AS "ItemBalance",
    NULL AS "ItemLevel",
    T_TimeLim.EVENT_DATA:event_type::STRING AS "Source/TargetItem"
    
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
    AND DATA_CENTER_ID LIKE '{silo}'
    AND FED_ID = '{account}'
    AND "ItemID" IS NOT NULL

ORDER BY "TIME" ASC
LIMIT 10000
;
'''