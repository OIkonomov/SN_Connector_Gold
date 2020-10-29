TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    DATE(T_Tour.CLIENT_TIME) AS "DATE",
    T_Tour.CLIENT_TIME AS "TIME",
    T_Tour.DATA_CENTER_ID AS "SILO",
    T_Tour.EVENT_DATA:realm_id_current::INT AS "REALM",
    T_Tour.FED_ID AS "FED",
    T_Tour.EVENT_DATA:progress_index02::INT AS "PLAYER_LEVEL",
    T_Event.EVENT_NAME AS "EVENT",
    T_Element.NAME AS "ACTION",
    T_Element_3.NAME AS "UNITS/FORMATION",
    T_Tour.EVENT_DATA:tournament_slot::INT AS "SLOT",
    T_Tour.EVENT_DATA:tournament_round::INT AS "ROUND",
    T_Tour.EVENT_DATA:target_fed_id::STRING AS "ENEMY",
    T_Element_2.NAME AS "RESULT",
    T_Tour.EVENT_DATA:event_type::STRING AS "EVENT_DETAILS",
    T_Tour.EVENT_DATA:player_load::STRING AS "PLAYER_ARMY",
    T_Tour.EVENT_DATA:player_damages::STRING AS "PLAYER_LOSSES",
    T_Tour.EVENT_DATA:target_load::STRING AS "ENEMY_ARMY",
    T_Tour.EVENT_DATA:target_damages::STRING AS "ENEMY_LOSSES",
    T_Tour.EVENT_DATA:hard_currency_spent::INT AS "GOLD_SPENT",
    T_Tour.EVENT_DATA:item_balance::INT AS "ITEM_BALANCE"
    
FROM
    "ELEPHANT_DB"."MOE"."TOURNAMENT_INTERACTION_RAW" AS T_Tour

LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."EVENT" AS T_Event
    ON (T_Tour.EVENT_ID = T_Event.EVENT_ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Tour.EVENT_DATA:tournament_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Tour.EVENT_DATA:tournament_result::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_Tour.EVENT_DATA:item_name::INT = T_Element_3.ID)
    
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND T_Tour.DATA_CENTER_ID LIKE '{silo}'
    AND T_Tour.FED_ID = '{account}'

ORDER BY TIME ASC
LIMIT 5000
;

'''