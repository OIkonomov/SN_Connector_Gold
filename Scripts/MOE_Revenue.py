TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT DISTINCT
    DATE(CLIENT_TIME) AS "DATE",
    DATA_CENTER_ID AS "SILO",
    PLATFORM AS "PLATFORM",
    SUM(REVENUE_EUR)::INT AS "TOTAL_REVENUE",
    COUNT(DISTINCT FED_ID) AS "TOTAL_ACCOUNTS",
    COUNT(DISTINCT TRANSACTION_ID) AS "TOTAL_TR",
    SUM(TOTAL_REVENUE) OVER() AS "TOTAL_PERIOD_REV",
    (TOTAL_REVENUE / TOTAL_PERIOD_REV * 100)::INT AS "%_REV_OVER_PERIOD",
    SUM(TOTAL_TR) OVER() AS "TOTAL_PERIOD_TR",
    (TOTAL_TR / TOTAL_PERIOD_TR * 100)::INT AS "%_TR_OVER_PERIOD"
FROM
    "ELEPHANT_DB"."MOE"."IAP"
WHERE
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND IAP_ACTION = 'New Purchase'
    AND SILO LIKE '{silo}'
GROUP BY
    DATE, SILO, PLATFORM
ORDER BY DATE ASC
LIMIT 100000
;
'''