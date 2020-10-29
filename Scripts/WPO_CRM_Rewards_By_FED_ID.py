TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT 
DATE(A.SERVER_TIME),
A.EVENT_DATA:reward_name::STRING as "Reward name",
A.EVENT_DATA:reward_amount::INT as "Reward amount",
A.FED_ID as "Fed id",
A.EVENT_DATA:action_id::string as "Event"
FROM "CC_DB"."WPO"."GOLD" as A
WHERE DATE(A.SERVER_TIME) >= '{st_date}' AND DATE(A.SERVER_TIME) <= '{end_date}' AND A.FED_ID = '{account}' and EVENT_ID = 51855 
UNION
SELECT
DATE(B.SERVER_TIME),
B.ITEM_NAME as "Reward name",
B.ITEM_AMOUNT as "Reward amount",
B.FED_ID as "Fed id",
B.EVENT_NAME as "Event"
from "ELEPHANT_DB"."WPO"."ITEM_DATA" as B
where EVENT_ID = '266612' and DATE(B.SERVER_TIME) >= '{st_date}' and DATE(B.SERVER_TIME) <= '{end_date}' and B.FED_ID = '{account}' and event_interaction = 'CRM Pointcut'
group by 1,2,3,4,5
order by 1 desc
LIMIT 6000;
'''