TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
WITH a AS
(
    SELECT
        DATE(CLIENT_TIME) AS "DATE",
        DATA_CENTER_ID AS "SILO",
        REALM_ID_CURRENT AS "REALM",
        FED_ID AS "FED",
        COMBAT_INT AS "C_ACTION",
        COMBAT_RESULT AS "RESULT",
        BATTLE_TARGET AS "TARGET",
        RESOURCES_STOLEN:"0"::INT AS "FOOD",
        RESOURCES_STOLEN:"1"::INT AS "WOOD",
        RESOURCES_STOLEN:"2"::INT AS "STONE",
        RESOURCES_STOLEN:"3"::INT AS "IRON",
        RESOURCES_STOLEN:"4"::INT AS "SILVER",
        PLAYER_LOST_UNITS:w AS "WOUNDED",
        PLAYER_LOST_UNITS:l AS "LOST",
        IFF(LENGTH (WOUNDED) > 2, 'WOUNDED', 'LOST') AS "L_TYPE",
        VALUE AS val
    FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION", 
        lateral flatten (input => PLAYER_LOST_UNITS)
    WHERE 
        CLIENT_TIME >= '{st_date}'
        AND CLIENT_TIME < '{end_date}'
        AND FED_ID = '{account}'
        AND COMBAT_INT LIKE 'Defend%'
LIMIT 10000
)
SELECT
    DATE,
    SILO,
    REALM,
    FED,
    C_ACTION,
    RESULT,
    TARGET,
    SUM(FOOD) AS "FOOD_LOST",
    SUM(WOOD) AS "WOOD_LOST",
    SUM(STONE) AS "STONE_LOST",
    SUM(IRON) AS "IRON_LOST",
    SUM(SILVER) AS "SILVER_LOST",
    T_ELEMENT.INGAME_NAME AS "TROOPS",
    L_TYPE AS "LOST?WOUNDED",
    SUM(VALUE) AS "TOTAL" FROM a, 
    lateral flatten (input => val)
    
    JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT_CATEGORY" AS T_ELEMENT
    ON (KEY = T_ELEMENT.ELEMENT_ID)
    GROUP BY
        DATE,
        FED,
        C_ACTION,
        RESULT,
        TARGET,
        L_TYPE,
        TROOPS,
        SILO,
        REALM
    ORDER BY
        C_ACTION DESC,
        L_TYPE ASC, 
        TROOPS ASC,
        TOTAL DESC
;
'''