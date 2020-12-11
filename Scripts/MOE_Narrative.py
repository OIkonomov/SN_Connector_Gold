TYPE = "Player"
CREDENTIAL = "Yes"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT DISTINCT
    T_GameServer.CLIENT_TIME AS "TIME",
    T_Element_2.NAME AS "INTERACTION",
    T_Element.NAME AS "CAMPAIGN",
    T_GameServer.EVENT_DATA:sequence_name::STRING AS "SEQUENCE",
    T_GameServer.EVENT_DATA:option_choice::STRING AS "CHOICE",
    T_GameServer.EVENT_DATA:campaign_side::STRING AS "SIDE",
    T_GameServer.EVENT_DATA:combat_result::STRING AS "COMBAT_RESSULT",
    T_GameServer.EVENT_DATA:energy_spent::INT AS "ENERGY_SPENT",
    T_GameServer.EVENT_DATA:energy_balance::INT AS "ENERGY_BALANCE",
    T_Element_3.NAME AS "REWARD",
    T_GameServer.EVENT_DATA:event_type::STRING AS "EVENT_TYPE",
    T_GameServer.EVENT_DATA:tle_event_id::STRING AS "EVENT_ID",
    T_GameServer.FED_ID AS "FED",
    T_GameServer.EVENT_DATA:realm_id_current::INT AS "REALM",
    T_GameServer.EVENT_DATA:all_id::INT AS "ALLIANCE_ID",
    T_GameServer.EVENT_DATA:option_name1::STRING AS "OPT_1",
    T_GameServer.EVENT_DATA:option_name2::STRING AS "OPT_2",
    T_GameServer.EVENT_DATA:option_name3::STRING AS "OPT_3",
    T_GameServer.EVENT_DATA:option_name4::STRING AS "OPT_4"

FROM
    "CC_DB"."MOE"."GAMESERVERS" AS T_GameServer
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."EVENT" AS T_Event
    ON (T_GameServer.EVENT_ID::INT = T_Event.EVENT_ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_GameServer.EVENT_DATA:campaign_name::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_GameServer.EVENT_DATA:story_int::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_GameServer.EVENT_DATA:item_name::INT = T_Element_3.ID)

WHERE
    T_GameServer.EVENT_ID = 330262
    AND T_GameServer.CLIENT_TIME >= '{st_date}'
    AND T_GameServer.CLIENT_TIME <= '{end_date}'
    AND T_GameServer.FED_ID = '{account}'

ORDER BY TIME ASC
LIMIT 5000
;
'''