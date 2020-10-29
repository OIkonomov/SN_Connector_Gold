TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
        SELECT
            Combat.FED_ID as "FED ID",
            Combat.COMBAT_ID as "Combat id",
            Combat.CLIENT_TIME::STRING as "Client time",
            Combat.SERVER_TIME::STRING as "Server time",
            Combat.TOKEN as "Token",
            Combat.TARGET_TYPE as "Target type",
            Combat.TARGET_LEVEL as "Target level",
            Combat.END_COORD_DATA as "Coordinates data",
            Combat.COMBAT_INT as "Combat result",
            Combat.INVOLVED_PLAYER_IDS as "Involved feds",
            Combat.INVOLVED_PLAYER_IDS2 as "Involved feds 2",
            Combat.PROGRESS_INDEX as "HQ Level",
            Combat.REALM_ID as "Realm ID",
            Combat.REALM_ID_CURRENT as "Realm ID",
            Combat.STRENGTH_BALANCE as "Strength Balance",
            Combat.STRENGTH_LOST as "Strength lost",
            NULL as EFFECT_INT,
            NULL as EFFECT_NAME,
            NULL as EFFECT_TARGET,
            NULL as EFFECT_REMAINING_TIME,
            NULL as EFFECT_TIME,
            NULL as EFFECT_TYPE
        FROM "ELEPHANT_DB"."WPO"."COMBAT_INTERACTION" as Combat
            WHERE DATE(Combat.CLIENT_TIME) >= '{st_date}' AND DATE(Combat.CLIENT_TIME) <= '{end_date}' and Combat.FED_ID = '{account}'
        UNION
        SELECT
            Effect.FED_ID as "FED ID",
            NULL as COMBAT_ID,
            Effect.CLIENT_TIME::STRING as "Client time",
            Effect.SERVER_TIME::STRING as "Server time",
            Effect.TOKEN as "Token",
            NULL as TARGET_TYPE,
            NULL as TARGET_LEVEL,
            NULL as END_COORD_DATA,
            NULL as COMBAT_INT,
            NULL as INVOLVED_PLAYER_IDS,
            NULL as INVOLVED_PLAYER_IDS2,
            NULL as PROGRESS_INDEX,
            Effect.REALM_ID as "Realm ID",
            Effect.REALM_ID_CURRENT as "Current Realm ID",
            NULL as STRENGTH_BALANCE,
            NULL as STRENGTH_LOST,
            Effect.EFFECT_INT as "Effect interaction",
            Effect.EFFECT_NAME as "Effect name",
            Effect.EFFECT_TARGET as "Effect target",
            Effect.EFFECT_REMAINING_TIME as "Effect remaining time",
            Effect.EFFECT_TIME as "Effect time",
            Effect.EFFECT_TYPE as "Effect type"
            FROM "ELEPHANT_DB"."WPO"."EFFECT_CHANGE" as Effect
            WHERE DATE(Effect.CLIENT_TIME) >= '{st_date}' AND DATE(Effect.CLIENT_TIME) <= '{end_date}' and Effect.FED_ID = '{account}' AND Effect.EFFECT_NAME = 'Bulletproof Battleplan Active Skill'
        ORDER BY 1,4,5
;
'''