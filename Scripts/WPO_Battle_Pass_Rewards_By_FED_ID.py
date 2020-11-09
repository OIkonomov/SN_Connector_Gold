TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT * FROM "ELEPHANT_DB"."WPO"."ITEM_DATA"
WHERE DATE(SERVER_TIME) >= '{st_date}' AND DATE(SERVER_TIME) <= '{end_date}' AND FED_ID = '{account}' and EVENT_ID = '266612' and (EVENT_INTERACTION = 'Reward from Battle Pass - Paid' or EVENT_INTERACTION = 'Reward from Battle Pass - Free' or EVENT_INTERACTION = 'Reward from Battle Pass - Autoclaim')
ORDER BY SERVER_TIME
LIMIT 6000;
'''