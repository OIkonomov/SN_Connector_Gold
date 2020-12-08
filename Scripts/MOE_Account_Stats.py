TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    DATE(T_PlayerConection.CLIENT_TIME) AS "DATE",
    MAX(T_PlayerConection.CLIENT_TIME) AS "LAST_SEEN",
    T_PlayerConection.DATA_CENTER_ID AS "SILO",
    T_PlayerConection.EVENT_DATA:realm_id_current::INT AS "REALM",
    T_PlayerConection.USER_ID AS "DEVICE",
    T_InventoryStatus.VERSION AS "VERSION",
    T_PlayerConection.ANON_ID AS "ANON",
    T_PlayerConection.FED_ID AS "FED",
    T_PlayerConection.EVENT_DATA:ingame_nickname_active::STRING AS "NAME",
    T_Element.NAME AS "LANGUAGE",
    T_InventoryStatus.COUNTRY AS "COUNTRY",
    T_PlayerConection.EVENT_DATA:game_player_id::INT AS "PLAYER_ID",
    T_PlayerConection.EVENT_DATA:all_id::INT AS "ALLIANCE_ID",
    T_PlayerConection.EVENT_DATA:all_name_tag::STRING AS "ALLIANCE_TAG",
    T_PlayerConection.EVENT_DATA:all_name::STRING AS "ALLIANCE_NAME",
    MAX(T_InventoryStatus.EVENT_DATA:progress_index01::INT) AS "CHAMPION_LEVEL",
    MAX(T_PlayerConection.EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
    MAX(T_InventoryStatus.EVENT_DATA:progress_index03::INT) AS "PARAGON_LEVEL",
    MAX(T_PlayerConection.EVENT_DATA:consumable_power_balance::INT) AS "MAX ARMY_MIGHT",
    MIN(T_PlayerConection.EVENT_DATA:consumable_power_balance::INT) AS "MIN ARMY_MIGHT",
    MAX(T_PlayerConection.EVENT_DATA:permanent_power_balance::INT) AS "MAX CITY_MIGHT",
    "MAX ARMY_MIGHT" + "MAX CITY_MIGHT" AS "MAX TOTAL_MIGHT",
    MAX(T_InventoryStatus.EVENT_DATA:hard_currency_balance::INT) AS "MAX GOLD_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:soft_currency1_balance::INT) AS "MAX FOOD_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:soft_currency2_balance::INT) AS "MAX WOOD_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:soft_currency3_balance::INT) AS "MAX STONE_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:soft_currency4_balance::INT) AS "MAX IRON_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:soft_currency5_balance::INT) AS "MAX SILVER_BALANCE",
    MAX(T_InventoryStatus.EVENT_DATA:quests_completed_amount::INT) AS "QUESTS_COMPLETED",
    MAX(T_InventoryStatus.EVENT_DATA:vip_level::INT) AS "VIP_LEVEL",
    MAX(T_InventoryStatus.EVENT_DATA:xp_balance::INT) AS "XP_BALANCE"

FROM
    "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PlayerConection
INNER JOIN
    "ELEPHANT_DB"."MOE"."INVENTORY_STATUS_RAW" AS T_InventoryStatus
    ON (T_PlayerConection.FED_ID = T_InventoryStatus.FED_ID
       AND DATE(T_PlayerConection.CLIENT_TIME) = DATE(T_InventoryStatus.CLIENT_TIME)
       AND T_PlayerConection.USER_ID = T_InventoryStatus.USER_ID
       AND T_InventoryStatus.FED_ID = '{account}'
       AND T_InventoryStatus.CLIENT_TIME > '{st_date}'
       AND T_InventoryStatus.CLIENT_TIME < '{end_date}'
       )
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_InventoryStatus.EVENT_DATA:game_language::INT = T_Element.ID)
WHERE 
    T_PlayerConection.CLIENT_TIME >= '{st_date}'
      AND T_PlayerConection.CLIENT_TIME < '{end_date}'
      AND "DEVICE" > 0
      AND T_PlayerConection.FED_ID = '{account}'
GROUP BY 1,3,4,5,6,7,8,9,10,11,12,13,14,15
ORDER BY LAST_SEEN DESC
LIMIT 1000
;
'''