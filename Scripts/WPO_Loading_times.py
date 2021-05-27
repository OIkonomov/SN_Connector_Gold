TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT * FROM "ELEPHANT_DB"."WPO"."LOADING_TIMES" 
WHERE DATE(SERVER_TIME) >= '{st_date}' and DATE(SERVER_TIME) <= '{end_date}'  and fed_id = '{account}' and load_int = 'Progress'
order by server_time




'''