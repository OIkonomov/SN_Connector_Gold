TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
    Combat.EVENT_ID::STRING as "Event",
    Combat.FED_ID as "FED ID",
    Combat.COMBAT_ID as "Combat id",
    Combat.CLIENT_TIME as "Client time",
    Combat.SERVER_TIME as "Server time",
    Combat.TARGET_TYPE as "Target type",
    Combat.TARGET_LEVEL as "Target level",
    NULL as ARMY_PURPOSE,
    NULL as ARMY_INT,
    Combat.END_COORD_DATA as "Coordinates data",
    Combat.COMBAT_INT as "Combat result",
    Combat.INVOLVED_PLAYER_IDS as "Involved feds",
    Combat.INVOLVED_PLAYER_IDS2 as "Involved feds 2",
    Combat.PROGRESS_INDEX as "HQ Level",
    Combat.REALM_ID_CURRENT as "Realm ID",
    Combat.STRENGTH_BALANCE as "Strength Balance",
    Combat.STRENGTH_LOST as "Strength lost"
FROM "ELEPHANT_DB"."WPO"."COMBAT_INTERACTION" as Combat
WHERE DATE(Combat.CLIENT_TIME) >= '{st_date}' AND DATE(Combat.CLIENT_TIME) <= '{end_date}' and Combat.FED_ID = '{account}'
UNION
SELECT
    Army.EVENT_ID::STRING as "Event",
    Army.FED_ID as "FED ID",
    NULL as COMBAT_ID,
    Army.CLIENT_TIME as "Client time",
    Army.SERVER_TIME as "Server time",
    Army.TARGET_TYPE as "Target type",
    Army.TARGET_LEVEL as "Target Level",
    Army.ARMY_PURPOSE as "Army purpose",
    Army.ARMY_INT as "Army interaction",
    NULL as END_COORD_DATA,
    NULL as COMBAT_INT,
    NULL as INVOLVED_PLAYER_IDS,
    NULL as INVOLVED_PLAYER_IDS2,
    NULL as PROGRESS_INDEX,
    NULL as REALM_ID_CURRENT,
    NULL as STRENGTH_BALANCE,
    NULL as STRENGTH_LOST
    FROM "ELEPHANT_DB"."WPO"."ARMY_INTERACTION" as Army
WHERE DATE(Army.CLIENT_TIME) >= '{st_date}' AND DATE(Army.CLIENT_TIME) <= '{end_date}' and Army.FED_ID = '{account}'
ORDER BY 1,4,5,6
;
'''