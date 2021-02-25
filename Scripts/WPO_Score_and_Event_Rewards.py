TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
select
A.USER_ID as "Device ID",
A.FED_ID as "FED ID",
A.EVENT_ID as "Event ID",
A.EVENT_NAME as "Event name",
A.SERVER_TIME as "Server Time",
A.EVENT_INTERACTION as "EVENT_INTERACTION",
A.ITEM_NAME as "Item Name",
A.ITEM_AMOUNT as "Item amount",
A.ITEM_BALANCE as "Item Balance",
NULL as EVENT_BRACKET,
NULL as REALM_ID, 
NULL as SCORE_BALANCE, 
NULL as SCORE_EARNED, 
NULL as SCORE_INT, 
NULL as SCORE_LOST, 
NULL as SCORE_THRESHOLD, 
NULL as TLE_EVENT_TYPE, 
NULL as TLE_EVENT_ID 
FROM "ELEPHANT_DB"."WPO"."ITEM_DATA" as A
WHERE DATE(A.SERVER_TIME) >= '{st_date}' AND DATE(A.SERVER_TIME) <= '{end_date}' AND (A.EVENT_ID = '260068' or A.EVENT_ID = '266612') and (A.EVENT_INTERACTION = 'TLE Milestone Reward' or A.EVENT_INTERACTION = 'TLE Alliance Leaderboard Reward' or A.EVENT_INTERACTION = 'TLE Leaderboard Reward' or A.EVENT_INTERACTION = 'Individual' or A.EVENT_INTERACTION = 'Leaderboard') and A.FED_ID = '{account}' 
UNION
SELECT
B.USER_ID as "Device ID",
B.FED_ID as "FED ID",
B.EVENT_ID as "Event ID",
NULL as EVENT_NAME,
B.SERVER_TIME as "Server Time",
NULL as EVENT_INTERACTION,
B.ITEM_NAME as "Item Name",
B.ITEM_AMOUNT as "Item amount",
B.ITEM_BALANCE as "Item Balance",
B.EVENT_BRACKET as "Event Bracket",
B.REALM_ID as "Realm ID",
B.SCORE_BALANCE as "Score Balance",
B.SCORE_EARNED as "Score Earned",
B.SCORE_INT as "Score Interaction",
B.SCORE_LOST as "Score lost",
B.SCORE_THRESHOLD as "Threshold",
B.TLE_EVENT_TYPE as "TLE Event Type",
B.TLE_EVENT_ID as "TLE Event ID/SEM ID"
FROM "ELEPHANT_DB"."WPO"."SCORE_INTERACTION" as B
WHERE DATE(B.SERVER_TIME) >= '{st_date}' and DATE(B.SERVER_TIME) <= '{end_date}' and B.FED_ID = '{account}' and NOT B.TLE_EVENT_TYPE = 'N/A'
ORDER By 5
;
'''