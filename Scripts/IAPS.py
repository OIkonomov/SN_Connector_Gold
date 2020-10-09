TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT DISTINCT
    CLIENT_TIME AS "TIME",
    ANON_ID AS "ANON",
    PLATFORM AS "PLATFORM",
    COUNTRY AS "COUNTRY",
    USER_ID AS "DEVICE",
    SUM(TO_NUMBER(REVENUE_EUR,20,2)) OVER(PARTITION BY DEVICE) AS "REVENUE_PER_DEVICE",
    TRANSACTION_ID AS "TRANSACTION",
    TO_NUMBER(PRICE_PAID,20,2) AS "PRICE",
    CURRENCY AS "CURRENCY",
    TO_NUMBER(REVENUE_EUR,20,2) AS "REVENUE_EUR",
    SUM(TO_NUMBER(REVENUE_EUR,20,2)) OVER() AS "TOTAL_REVENUE"
FROM
    "ELEPHANT_DB"."MOE"."IAP"
WHERE
    CLIENT_TIME > '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
ORDER BY TIME
LIMIT 10000
;
'''