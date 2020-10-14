TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "COORD (255:255)"
SILO = "YES"
REALM = "YES"
DATE = "YES"

SQL_REQ = '''
SELECT * FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION" 
WHERE 
  END_COORD = '{filter_value}'
    AND CLIENT_TIME > '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND REALM_ID = {realm}
ORDER BY CLIENT_TIME
LIMIT 10000
;
'''