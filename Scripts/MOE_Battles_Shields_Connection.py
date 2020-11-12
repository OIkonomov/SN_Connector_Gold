TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "REALM"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''

SELECT
    T_CombatInt.DATA_CENTER_ID AS "SILO",
    T_CombatInt.EVENT_DATA:realm_id::INT AS "REALM",
    T_CombatInt.EVENT_DATA:realm_id_current::INT AS "C_REALM",
    DATE(T_CombatInt.CLIENT_TIME) AS "DATE",
    T_CombatInt.CLIENT_TIME AS "TIME",
    T_Element.NAME AS "INTERACTION",
    T_Element_3.NAME AS "BATTLE_FIELD",
    T_Element_2.NAME AS "RESULT",
    T_CombatInt.EVENT_DATA:battle_coord::STRING AS "BATTLE_COORD_ID",
    T_CombatInt.EVENT_DATA:involved_player_ids::STRING AS "PARTICIPANTS",
    T_CombatInt.EVENT_DATA:total_army_size::STRING AS "ARMY_SIZE",
    T_CombatInt.EVENT_DATA:power_lost::INT AS "POWER_LOST",
    T_CombatInt.EVENT_DATA:player_lost_units AS "LOST_UNITS",
    T_CombatInt.FED_ID AS "FED"

FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION_RAW" AS T_CombatInt
    
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_CombatInt.EVENT_DATA:combat_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_CombatInt.EVENT_DATA:combat_result::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_CombatInt.EVENT_DATA:battle_target::INT = T_Element_3.ID)

WHERE 
    T_CombatInt.CLIENT_TIME > '{st_date}'
    AND T_CombatInt.CLIENT_TIME < '{end_date}'
    AND T_CombatInt.DATA_CENTER_ID::STRING LIKE '{silo}'
    AND T_CombatInt.FED_ID = '{account}'
    AND C_REALM = {filter_value}

UNION ALL

SELECT 
    T_BaseInt.DATA_CENTER_ID AS "SILO",
    T_BaseInt.EVENT_DATA:realm_id::INT AS "REALM",
    T_BaseInt.EVENT_DATA:realm_id_current::INT AS "C_REALM",
    DATE(T_BaseInt.CLIENT_TIME) AS "DATE",
    T_BaseInt.CLIENT_TIME AS "TIME",
    T_Element_4.NAME AS "INTERACTION",
    T_Element_6.NAME AS "BATTLE_FIELD",
    T_Element_5.NAME AS "RESULT",
    '' AS "BATTLE_COORD_ID",
    '' AS "PARTICIPANTS",
    '' AS "ARMY_SIZE",
    0 AS "POWER_LOST",
    0 AS "LOST_UNITS",
    T_BaseInt.FED_ID AS "FED"
    
FROM "ELEPHANT_DB"."MOE"."BASE_INTERACTION_RAW" AS T_BaseInt

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_4
    ON (T_BaseInt.EVENT_DATA:base_int::INT = T_Element_4.ID)

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_5
    ON (T_BaseInt.EVENT_DATA:item_name::INT = T_Element_5.ID)

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_6
    ON (T_BaseInt.EVENT_DATA:shield_type::INT = T_Element_6.ID)

WHERE 
    T_BaseInt.CLIENT_TIME > '{st_date}'
    AND T_BaseInt.CLIENT_TIME < '{end_date}'
    AND T_BaseInt.DATA_CENTER_ID::STRING LIKE '{silo}'
    AND T_BaseInt.FED_ID = '{account}'
    AND T_BaseInt.EVENT_DATA:base_int::INT <> 223742
    AND C_REALM = {filter_value}
      
UNION ALL

SELECT 
    T_ServerState.DATA_CENTER_ID AS "SILO",
    0 AS "REALM",
    T_ServerState.REALM_ID::INT AS "C_REALM",
    DATE(T_ServerState.CLIENT_TIME) AS "DATE",
    T_ServerState.CLIENT_TIME AS "TIME",
    T_ServerState.GS_INT AS "INTERACTION",
    T_ServerState.PLATFORM AS "BATTLE_FIELD",
    '' AS "RESULT",
    '' AS "BATTLE_COORD_ID",
    '' AS "PARTICIPANTS",
    '' AS "ARMY_SIZE",
    0 AS "POWER_LOST",
    0 AS "LOST_UNITS",
    '' AS "FED"

FROM "ELEPHANT_DB"."MOE"."SERVER_STATE_REPORT" AS T_ServerState

WHERE 
    T_ServerState.CLIENT_TIME >= '{st_date}'
    AND T_ServerState.CLIENT_TIME < '{end_date}'
    AND T_ServerState.DATA_CENTER_ID::STRING LIKE '{silo}'
    AND T_ServerState.REALM_ID::INT = {filter_value}

UNION ALL

SELECT 
    T_PLayerConnection.DATA_CENTER_ID AS "SILO",
    0 AS "REALM",
    T_PLayerConnection.EVENT_DATA:realm_id::INT AS "C_REALM",
    DATE(T_PLayerConnection.CLIENT_TIME) AS "DATE",
    T_PLayerConnection.CLIENT_TIME AS "TIME",
    T_Element_7.NAME AS "INTERACTION",
    T_PLayerConnection.EVENT_DATA:session_length::STRING AS "BATTLE_FIELD",
    '' AS "RESULT",
    '' AS "BATTLE_COORD_ID",
    '' AS "PARTICIPANTS",
    '' AS "ARMY_SIZE",
    0 AS "POWER_LOST",
    0 AS "LOST_UNITS",
    T_PLayerConnection.FED_ID AS "FED"

FROM "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW" AS T_PLayerConnection

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_7
    ON (T_PLayerConnection.EVENT_DATA:connect_int::INT = T_Element_7.ID)

WHERE 
    T_PLayerConnection.CLIENT_TIME >= '{st_date}'
      AND T_PLayerConnection.CLIENT_TIME < '{end_date}'
      AND T_PLayerConnection.DATA_CENTER_ID::STRING LIKE '{silo}'
      AND T_PLayerConnection.FED_ID = '{account}'
      AND T_PLayerConnection.EVENT_DATA:connect_int::INT <> 359947

UNION ALL

SELECT
    T_LaunchResume.DATA_CENTER_ID AS "SILO",
    0 AS "REALM",
    0 AS "C_REALM",
    DATE(T_LaunchResume.CLIENT_TIME) AS "DATE",
    T_LaunchResume.CLIENT_TIME AS "TIME",
    T_Element_8.NAME AS "INTERACTION",
    T_LaunchResume.EVENT_DATA:time_spent::STRING AS "BATTLE_FIELD",
    T_Element_8.NAME AS "RESULT",
    T_LaunchResume.VERSION AS "BATTLE_COORD_ID",
    '' AS "PARTICIPANTS",
    '' AS "ARMY_SIZE",
    0 AS "POWER_LOST",
    0 AS "LOST_UNITS",
    T_LaunchResume.FED_ID AS "FED"

FROM "ELEPHANT_DB"."MOE"."LAUNCH_RESUME_RAW" AS T_LaunchResume

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_8
    ON (T_LaunchResume.EVENT_DATA:launch_type::INT = T_Element_8.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_9
    ON (T_LaunchResume.EVENT_DATA:crash_detection::INT = T_Element_9.ID)

WHERE 
    T_LaunchResume.CLIENT_TIME >= '{st_date}'
    AND T_LaunchResume.CLIENT_TIME < '{end_date}'
    AND T_LaunchResume.DATA_CENTER_ID::STRING LIKE '{silo}'
    AND T_LaunchResume.FED_ID = '{account}'
     
ORDER BY TIME ASC
LIMIT 5000
;
'''