TYPE = "Player"
CREDENTIAL = "NO"
FILTER = "Device ID"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
A.REALM_ID as "Realm ID",
A.USER_ID as "Device",
max(A.SERVER_TIME) as "Server time",
A.FED_ID as "Fed",
max(b.PROGRESS_INDEX) as "HQ Level",
max(A.INGAME_NICKNAME_ACTIVE) as "Nickname"
From "ELEPHANT_DB"."WPO"."PLAYER_CONNECTION_REPORT" as A
LEFT JOIN "ELEPHANT_DB"."WPO"."PROGRESSION_GS" as b
ON (A.FED_ID = b.FED_ID)
WHERE DATE(A.SERVER_TIME) >= '{st_date}' AND DATE(A.SERVER_TIME) <= '{end_date}' AND A.USER_ID = '{filter_value}'
group by 1,2,4
'''