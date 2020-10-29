TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT * FROM "ELEPHANT_DB"."WPO"."ITEM_DATA"
WHERE DATE(SERVER_TIME) >= '{st_date}' AND DATE(SERVER_TIME) <= '{end_date}' AND FED_ID = '{account}' 
and (EVENT_INTERACTION = 'Material used for Crafting' or EVENT_INTERACTION = 'Material Used For Commander Add-On Crafting' or EVENT_INTERACTION = 'Item Collected From Crafting' or EVENT_INTERACTION = 'Add-On Item Collected from Crafting')
and EVENT_ID = '266612'
ORDER BY SERVER_TIME
LIMIT 6000;
'''