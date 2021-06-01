TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT * FROM "ELEPHANT_DB"."WPO"."TLE_USER_SOLO_EVENT_RESULTS" 
WHERE DATE(TLE_EVENT_LAUNCHTIME) >= '{st_date}'  and fed_id = '{account}' 
order by TLE_EVENT_LAUNCHTIME




'''