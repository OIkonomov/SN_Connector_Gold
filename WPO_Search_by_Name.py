TYPE = "Player"
CREDENTIAL = "NO"
FILTER = "Name"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT 
FED_ID as "fed id",
SERVER_TIME as "Server time",
EVENT_DATA:player_alias::STRING as "Gloft id",
EVENT_DATA:player_name::STRING as "Name",
EVENT_DATA:progress_index::STRING as "Progress index",
EVENT_DATA:realm_id:STRING as "Realm"
FROM "TRACKING_DB"."WPO"."GOLD" 
WHERE EVENT_ID = '51904' and DATE(SERVER_TIME) >= '{st_date}' AND DATE(SERVER_TIME) <= '{end_date}' and EVENT_DATA:player_name::STRING like '%{filter_value}%'
ORDER BY SERVER_TIME;




'''