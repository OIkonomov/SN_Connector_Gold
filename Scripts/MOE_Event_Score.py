TYPE = "Player"
CREDENTIAL = "Yes"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    MIN(T_Score.CLIENT_TIME) AS "MIN_TIME",
    MAX(T_Score.CLIENT_TIME) AS "MAX_TIME",
    T_Score.EVENT_DATA:event_bracket::INT AS "BRACKET",
    T_Element_4.NAME AS "EVENT_TYPE",
    T_Score.EVENT_DATA:event_name::STRING AS "EVENT_NAME",
    T_Element.NAME AS "INTERACTION",
    T_Element_2.NAME AS "THRESHOLD",
    T_Element_3.NAME AS "SCORE_TYPE",
    T_Element_5.NAME AS "OBJECTIVE",
    SUM(T_Score.EVENT_DATA:score_earned::INT) AS "SCORE_EARNED",
    SUM(T_Score.EVENT_DATA:score_lost::INT) AS "SCORE_LOST",
    T_Score.EVENT_DATA:score_leftover::INT AS "SCORE_LEFT",
    MAX(T_Score.EVENT_DATA:score_balance::INT) AS "SCORE_BALANCE",
    T_Score.EVENT_DATA:event_type::STRING AS "EVENT_DETAILS",
    T_Score.EVENT_DATA:tle_event_id::STRING AS "EVENT_ID",
    T_Score.DATA_CENTER_ID AS "SILO",
    T_Score.EVENT_DATA:realm_id::INT AS "REALM",
    T_Score.EVENT_DATA:realm_id_current::INT AS "C_REALM",
    T_Score.FED_ID AS "FED",
    T_Score.EVENT_DATA:progress_index02::INT AS "CASTLE_LEVEL",
    T_Score.EVENT_DATA:all_id::INT AS "ALLIANCE_ID"
    
FROM
    "ELEPHANT_DB"."MOE"."SCORE_INTERACTION_RAW" AS T_Score
    
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
    ON (T_Score.EVENT_DATA:score_int::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_2
    ON (T_Score.EVENT_DATA:score_threshold::INT = T_Element_2.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_3
    ON (T_Score.EVENT_DATA:score_type::INT = T_Element_3.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_4
    ON (T_Score.EVENT_DATA:criteria_actor::INT = T_Element_4.ID)
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element_5
    ON (T_Score.EVENT_DATA:score_objective::INT = T_Element_5.ID)

WHERE
    CLIENT_TIME > '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED = '{account}'
    AND EVENT_NAME NOT LIKE 'N/A'

GROUP BY 3,4,5,6,7,8,9,12,14,15,16,17,18,19,20,21
ORDER BY MIN_TIME
LIMIT 5000
;
'''