TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    T_Main."DATE",
    T_Main."TIME",
    T_Main."SILO",
    T_Main."REALM",
    T_Main."FED",
    T_Event.EVENT_NAME AS "EVENT",
    T_Main."MARCH",
    T_Main."ACTION",
    T_Main."COMBAT_ID/PURPOSE",
    T_Main."TARGET_TYPE",
    T_Main."TARGET_LEVEL",
    T_Main."COORD/ID/CHAMP",
    T_Main."START_COORD",
    T_Main."END_COORD",
    T_Main."PLAYER_LEVEL",
    T_Main."PLAYER_FORMATION",
    T_Main."RESULT/CHAMPION",
    T_Main."PLAYER_ARMY_LOAD",
    T_Main."TOTAL_ARMY_SIZE",
    T_Element.NAME AS "TACTIC_NAME",
    T_Main."TACTIC_LEVEL",
    T_Element_2.NAME AS "PLAN_NAME",
    T_Main."PLAN_LEVEL",
    T_Main."OCCUPANT_TYPE",
    T_Main."POWER_LOST",
    T_Main."POWER_BALANCE",
    T_Main."PLAYER_LOST_UNITS",
    T_Main."PLAYER_BONUSES",
    T_Main."ENEMY_FORMATION",
    T_Main."ENEMY_LOAD",
    T_Element_3.NAME AS "ENEMY_TACTIC_NAME",
    T_Main."ENEMY_TACTIC_LEVEL",
    T_Main."XP_EARNED",
    T_Main."INVOLVED_PLAYERS",
    '' AS "SPECIAL_LOAD",
    0 AS "PLAYER_ALL_ID",
    '' AS "TARGET_PLAYER",
    0 AS "TARGET_ALL_ID",
    0 AS "GOLD_EARNED",
    0 AS "GOLD_SPENT",
    0 AS "GOLD_BALANCE",
    0 AS "FOOD_EARNED",
    0 AS "WOOD_EARNED",
    0 AS "STONE_EARNED",
    0 AS "IRON_EARNED",
    0 AS "SILVER_EARNED",
    0 AS "FOOD_SPENT",
    0 AS "WOOD_SPENT",
    0 AS "STONE_SPENT",
    0 AS "IRON_SPENT",
    0 AS "SILVER_SPENT"
    
    FROM(
          SELECT DISTINCT
                DATE(T_Combat.CLIENT_TIME) AS "DATE",
                T_Combat.CLIENT_TIME AS "TIME",
                T_Combat.EVENT_ID AS "EVENT_ID",
                T_Combat.DATA_CENTER_ID::STRING AS "SILO",
                T_Combat.REALM_ID_CURRENT::INT AS "REALM",
                T_Combat.FED_ID AS "FED",
                T_Combat.COMBAT_INT::STRING AS "ACTION",
                T_Combat.PROGRESS_INDEX02 AS "PLAYER_LEVEL",
                T_Combat.BATTLE_TARGET::STRING AS "TARGET_TYPE",
                T_Combat.TARGET_LEVEL::INT AS "TARGET_LEVEL",
                T_Combat.COMBAT_RESULT::STRING AS "RESULT/CHAMPION",
                T_Combat.COMBAT_ID::STRING AS "COMBAT_ID/PURPOSE",
                T_Combat.START_COORD::STRING AS "START_COORD",
                T_Combat.END_COORD::STRING AS "END_COORD",
                T_Combat.MARCH::INT AS "MARCH",
                T_Combat.BATTLE_COORD::STRING AS "COORD/ID/CHAMP",
                T_Combat.POWER_LOST::INT AS "POWER_LOST",
                T_Combat.POWER_BALANCE::INT AS "POWER_BALANCE",
                T_Combat.TOTAL_ARMY_SIZE::STRING AS "TOTAL_ARMY_SIZE",
                T_Combat.OCCUPANT_TYPE::STRING AS "OCCUPANT_TYPE",
                T_Combat.PLAYER_LOST_UNITS::STRING AS "PLAYER_LOST_UNITS",
                T_Combat.COMBAT_BONUSES::STRING AS "PLAYER_BONUSES",
                T_Combat.PLAYER_FORMATION::STRING AS "PLAYER_FORMATION",
                T_Combat.PLAYER_ARMY_LOAD::STRING AS "PLAYER_ARMY_LOAD",
                T_Combat.ENEMY_FORMATION::STRING AS "ENEMY_FORMATION",
                T_Combat.ENEMY_LOAD::STRING AS "ENEMY_LOAD",
                T_Combat.ENEMY_TACTICS_LOAD::STRING AS "ENEMY_TACTICS_LOAD",
                T_Combat.XP_EARNED::INT AS "XP_EARNED",
                T_Combat.INVOLVED_PLAYER_IDS::STRING AS "INVOLVED_PLAYERS",
                SPLIT_PART(T_Combat.PLAYER_TACTICS_LOAD, '(', 1) AS "T_Field",
                SPLIT_PART(SPLIT_PART(T_Combat.PLAYER_TACTICS_LOAD, '(', 2),')',1) AS "P_Field",
                IFF(SPLIT_PART("T_Field",':',1)='N/A','0',SPLIT_PART("T_Field",':',1)::INT) AS "TACTIC_ID",
                IFF(SPLIT_PART("T_Field",':',1)='N/A','0',SPLIT_PART(SPLIT_PART(T_Combat.PLAYER_TACTICS_LOAD, '(', 1),':',2)::INT) AS "TACTIC_LEVEL",
                IFF(SPLIT_PART("P_Field",':',1)='','0',SPLIT_PART("P_Field",':',1)::INT) AS "PLAN_ID",
                IFF(SPLIT_PART("P_Field",':',1)='','0',SPLIT_PART(SPLIT_PART(SPLIT_PART(T_Combat.PLAYER_TACTICS_LOAD, '(', 2),')',1),':',2)::INT) AS "PLAN_LEVEL",
                IFF(SPLIT_PART("ENEMY_TACTICS_LOAD",':',1)='N/A','0',SPLIT_PART("ENEMY_TACTICS_LOAD",':',1)::INT) AS "ENEMY_TACTIC_ID",
                IFF(SPLIT_PART("ENEMY_TACTICS_LOAD",':',1)='N/A','0',SPLIT_PART(SPLIT_PART(T_Combat.ENEMY_TACTICS_LOAD, '(', 1),':',2)::INT) AS "ENEMY_TACTIC_LEVEL"

            FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION" AS T_Combat

          WHERE
              CLIENT_TIME >= '{st_date}'
              AND CLIENT_TIME < '{end_date}'
              AND FED_ID = '{account}'

          ORDER BY CLIENT_TIME ASC

          LIMIT 1000) AS T_Main
    LEFT JOIN
        "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
        ON (T_Main."TACTIC_ID" = T_Element.ID)
    LEFT JOIN
        "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
        ON (T_Main."PLAN_ID" = T_Element_2.ID)
    LEFT JOIN
        "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
        ON (T_Main."ENEMY_TACTIC_ID" = T_Element_3.ID)
    LEFT JOIN
        "ELEPHANT_DB"."DIMENSIONS"."EVENT" AS T_Event
        ON (T_Main."EVENT_ID" = T_Event.EVENT_ID)
WHERE
    TIME >= '{st_date}'
    AND TIME < '{end_date}'
    AND FED = '{account}'

UNION ALL

SELECT DISTINCT
    T_Main_2."DATE",
    T_Main_2."TIME",
    T_Main_2."SILO",
    T_Main_2."REALM",
    T_Main_2."FED",
    T_Event.EVENT_NAME AS "EVENT",
    T_Main_2."MARCH",
    T_Element_2.NAME AS "ACTION",
    T_Element.NAME AS "COMBAT_ID/PURPOSE",
    T_Element_6.NAME AS "TARGET_TYPE",
    T_Main_2."TARGET_LEVEL",
    T_Main_2."COORD/ID/CHAMP",
    T_Main_2."START_COORD",
    T_Main_2."END_COORD",
    T_Main_2."PLAYER_LEVEL",
    T_Element_3.NAME AS "PLAYER_FORMATION",
    T_Element_4.NAME AS "RESULT/CHAMPION",
    T_Main_2."PLAYER_ARMY_LOAD",
    '' AS "TOTAL_ARMY_SIZE",
    T_Element_7.NAME AS "TACTIC_NAME",
    T_Main_2."TACTIC_LEVEL",
    T_Element_8.NAME AS "PLAN_NAME",
    T_Main_2."PLAN_LEVEL",
    T_Element_5.NAME AS "OCCUPANT_TYPE",
    0 AS "POWER_LOST",
    0 AS "POWER_BALANCE",
    '' AS "PLAYER_LOST_UNITS",
    '' AS "PLAYER_BONUSES",
    '' AS "ENEMY_FORMATION",
    '' AS "ENEMY_LOAD",
    '' AS "ENEMY_TACTIC_NAME",
    0 AS "ENEMY_TACTIC_LEVEL",
    0 AS "XP_EARNED",
    '' AS "INVOLVED_PLAYERS",
    T_Main_2."SPECIAL_LOAD",
    T_Main_2."PLAYER_ALL_ID",
    T_Main_2."TARGET_PLAYER",
    T_Main_2."TARGET_ALL_ID",
    T_Main_2."GOLD_EARNED",
    T_Main_2."GOLD_SPENT",
    T_Main_2."GOLD_BALANCE",
    T_Main_2."FOOD_EARNED",
    T_Main_2."WOOD_EARNED",
    T_Main_2."STONE_EARNED",
    T_Main_2."IRON_EARNED",
    T_Main_2."SILVER_EARNED",
    T_Main_2."FOOD_SPENT",
    T_Main_2."WOOD_SPENT",
    T_Main_2."STONE_SPENT",
    T_Main_2."IRON_SPENT",
    T_Main_2."SILVER_SPENT"
    
    FROM(
          SELECT DISTINCT
            DATE(T_Army.CLIENT_TIME) AS "DATE",
            T_Army.CLIENT_TIME AS "TIME",
            T_Army.DATA_CENTER_ID AS "SILO",
            T_Army.EVENT_DATA:realm_id_current::INT AS "REALM",
            T_Army.FED_ID AS "FED",
            T_Army.EVENT_ID AS "EVENT_ID",
            T_Army.EVENT_DATA:army_int::INT AS "ACTION",
            T_Army.EVENT_DATA:march::INT AS "MARCH",
            T_Army.EVENT_DATA:army_purpose::INT AS "PURPOSE",
            T_Army.EVENT_DATA:army_coord::STRING AS "COORD/ID/CHAMP",
            T_Army.EVENT_DATA:start_coord::STRING AS "START_COORD",
            T_Army.EVENT_DATA:end_coord::STRING AS "END_COORD",
            T_Army.EVENT_DATA:hard_currency_earned::INT AS "GOLD_EARNED",
            T_Army.EVENT_DATA:soft_currency1_earned::INT AS "FOOD_EARNED",
            T_Army.EVENT_DATA:soft_currency2_earned::INT AS "WOOD_EARNED",
            T_Army.EVENT_DATA:soft_currency3_earned::INT AS "STONE_EARNED",
            T_Army.EVENT_DATA:soft_currency4_earned::INT AS "IRON_EARNED",
            T_Army.EVENT_DATA:soft_currency5_earned::INT AS "SILVER_EARNED",
            T_Army.EVENT_DATA:formation::INT AS "FORMATION",
            T_Army.EVENT_DATA:formation_champion::INT AS "RESULT/CHAMPION",

            SPLIT_PART(T_Army.EVENT_DATA:tactics_load::STRING, '(', 1) AS "T_Field",
            SPLIT_PART(SPLIT_PART(T_Army.EVENT_DATA:tactics_load::STRING, '(', 2),')',1) AS "P_Field",

            IFF(SPLIT_PART("T_Field",':',1)='N/A','0',SPLIT_PART("T_Field",':',1)::INT) AS "TACTIC_ID",
            IFF(SPLIT_PART("T_Field",':',1)='N/A','0',SPLIT_PART(SPLIT_PART(T_Army.EVENT_DATA:tactics_load::STRING, '(', 1),':',2)::INT) AS "TACTIC_LEVEL",
            IFF(SPLIT_PART("P_Field",':',1)='','0',SPLIT_PART("P_Field",':',1)::INT) AS "PLAN_ID",
            IFF(SPLIT_PART("P_Field",':',1)='','0',SPLIT_PART(SPLIT_PART(SPLIT_PART(T_Army.EVENT_DATA:tactics_load::STRING, '(', 2),')',1),':',2)::INT) AS "PLAN_LEVEL",

            T_Army.EVENT_DATA:army_load::STRING AS "PLAYER_ARMY_LOAD",
            T_Army.EVENT_DATA:special_load::STRING AS "SPECIAL_LOAD",
            T_Army.EVENT_DATA:occupant_type::INT AS "OCCUPANT_TYPE",
            T_Army.EVENT_DATA:progress_index02::INT AS "PLAYER_LEVEL",
            T_Army.EVENT_DATA:all_id::INT AS "PLAYER_ALL_ID",
            T_Army.EVENT_DATA:target_level::INT AS "TARGET_LEVEL",
            T_Army.EVENT_DATA:target_player_id::STRING AS "TARGET_PLAYER",
            T_Army.EVENT_DATA:target_all_id::INT AS "TARGET_ALL_ID",
            T_Army.EVENT_DATA:target_type::INT AS "TARGET_TYPE",
            T_Army.EVENT_DATA:hard_currency_spent::INT AS "GOLD_SPENT",
            T_Army.EVENT_DATA:hard_currency_balance::INT AS "GOLD_BALANCE",
            T_Army.EVENT_DATA:soft_currency1_spent::INT AS "FOOD_SPENT",
            T_Army.EVENT_DATA:soft_currency2_spent::INT AS "WOOD_SPENT",
            T_Army.EVENT_DATA:soft_currency3_spent::INT AS "STONE_SPENT",
            T_Army.EVENT_DATA:soft_currency4_spent::INT AS "IRON_SPENT",
            T_Army.EVENT_DATA:soft_currency5_spent::INT AS "SILVER_SPENT"
          FROM
              "ELEPHANT_DB"."MOE"."ARMY_INTERACTION_RAW" AS T_Army
          WHERE
              CLIENT_TIME >= '{st_date}'
              AND CLIENT_TIME < '{end_date}'
              AND FED_ID = '{account}'

          ORDER BY CLIENT_TIME ASC
                                      ) AS T_Main_2
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."EVENT" AS T_Event
    ON (T_Main_2."EVENT_ID" = T_Event.EVENT_ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Main_2."ACTION" = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Main_2."PURPOSE" = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_Main_2."FORMATION" = T_Element_3.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_4
    ON (T_Main_2."RESULT/CHAMPION" = T_Element_4.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_5
    ON (T_Main_2."OCCUPANT_TYPE" = T_Element_5.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_6
    ON (T_Main_2."TARGET_TYPE" = T_Element_6.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_7
    ON (T_Main_2."TACTIC_ID" = T_Element_7.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_8
    ON (T_Main_2."PLAN_ID" = T_Element_8.ID)

WHERE
    TIME >= '{st_date}'
    AND TIME < '{end_date}'
    AND FED = '{account}'

ORDER BY TIME ASC
LIMIT 10000
;
'''