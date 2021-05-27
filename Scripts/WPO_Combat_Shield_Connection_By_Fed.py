TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
A.FED_ID as "FED ID",
A.PLATFORM as "Platform",
elem.NAME as "Event",
A.CLIENT_TIME as "Client Time",
A.SERVER_TIME as "Server Time",
A.TOKEN as "Token Server ID",
A.COMBAT_ID as "Combat ID",
A.COMBAT_INT as "Combat interaction",
A.END_COORD_DATA as "Combat meta data",
A.INVOLVED_PLAYER_IDS as "Fed Participantes",
A.INVOLVED_PLAYER_IDS as "Fed Participantes2",
A.PLAYER_LOST_ARMY as "Lost Army",
A.PROGRESS_INDEX as "HQ Level",
A.STRENGTH_LOST as "Strength Lost",
A.TARGET_LEVEL as "Target level",
A.TARGET_TYPE as "Target Type",
A.REALM_ID as "Realm ID",
A.REALM_ID_CURRENT as "Current Realm ID",
NULL as CONNECT_INT,
NULL as GAME_PLAYER_ID, 
NULL as INGAME_NICKNAME_ACTIVE, 
NULL as HOMEBASE_INT,
NULL as HOMEBASE_INT_PURPOSE,
NULL as SHIELD_DURATION, 
NULL as ITEM_NAME 
FROM "ELEPHANT_DB"."WPO"."COMBAT_INTERACTION" as A
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" elem ON (A.EVENT_ID = elem.ID)
WHERE DATE(A.CLIENT_TIME) >= '{st_date}' AND DATE(A.CLIENT_TIME) <= '{end_date}' and A.FED_ID = '{account}'
UNION
SELECT 
B.FED_ID as "FED ID",
B.PLATFORM as "Platform",
B.EVENT_NAME as "Event",
B.CLIENT_TIME as "Client Time",
B.SERVER_TIME as "Server Time",
B.TOKEN as "Token Server ID",
NULL as COMBAT_ID,
NULL as COMBAT_INT, 
NULL as END_COORD_DATA, 
NULL as INVOLVED_PLAYER_IDS,
NULL as INVOLVED_PLAYER_IDS2,
NULL as PLAYER_LOST_ARMY ,
NULL as PROGRESS_INDEX, 
NULL as STRENGTH_LOST, 
NULL as TARGET_LEVEL,
NULL as TARGET_TYPE ,
B.REALM_ID as "Realm ID",
B.REALM_ID_CURRENT as "Current Realm ID",
B.CONNECT_INT as "Connection interaction",
B.GAME_PLAYER_ID as "Gameloft ID",
B.INGAME_NICKNAME_ACTIVE as "Ingame name",
NULL as HOMEBASE_INT,
NULL as HOMEBASE_INT_PURPOSE,
NULL as SHIELD_DURATION,
NULL as ITEM_NAME
FROM "ELEPHANT_DB"."WPO"."PLAYER_CONNECTION_REPORT" as B
WHERE DATE(B.CLIENT_TIME) >= '{st_date}' AND DATE(B.CLIENT_TIME) <= '{end_date}' and B.FED_ID = '{account}'
UNION
SELECT
C.FED_ID as "FED ID",
C.PLATFORM as "Platform",
elem2.NAME as "Event",
C.CLIENT_TIME as "Client Time",
C.SERVER_TIME as "Server Time",
C.TOKEN as "Token Server ID",
NULL as COMBAT_ID,
NULL as COMBAT_INT, 
NULL as END_COORD_DATA,
NULL as INVOLVED_PLAYER_IDS,
NULL as INVOLVED_PLAYER_IDS2,
NULL as PLAYER_LOST_ARMY, 
C.PROGRESS_INDEX as "HQ Level",
NULL as STRENGTH_LOST,
NULL as TARGET_LEVEL,
NULL as TARGET_TYPE, 
C.REALM_ID as "Realm ID",
C.REALM_ID_CURRENT as "Current Realm ID",
NULL as CONNECT_INT,
NULL as GAME_PLAYER_ID ,
NULL as INGAME_NICKNAME_ACTIVE,
C.HOMEBASE_INT as "Homebase Interaction",
C.HOMEBASE_INT_PURPOSE as "Purpose",
C.SHIELD_DURATION as "Shield Duration",
C.ITEM_NAME as "Item Used"
FROM "ELEPHANT_DB"."WPO"."HOMEBASE_INTERACTION" as C
LEFT JOIN "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" elem2 ON (C.EVENT_ID = elem2.ID)
WHERE DATE(C.CLIENT_TIME) >= '{st_date}' AND DATE(C.CLIENT_TIME) <= '{end_date}' and C.FED_ID = '{account}' and (C.HOMEBASE_INT = 'Cloak Activated' or C.HOMEBASE_INT = 'Cloak Re-Activated' or C.HOMEBASE_INT = 'Shield Activated' or C.HOMEBASE_INT = 'Shield Cancelled by Action' or C.HOMEBASE_INT = 'Shield Re-Activated')
Order by 5
;
'''