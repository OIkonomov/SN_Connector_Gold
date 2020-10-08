TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "PACK NAME"
SILO = "NO"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    T_IAP.DATE,
    T_IAP.PACK,
    T_IAP.R_GROUP,
    T_IAP.TRANSACTONS,
    SUM(T_IAP.ACCOUNTS) AS "ACC_BY_GROUP",
    SUM(T_IAP.TRANSACTONS) AS "TR_BY_GROUP",
    SUM(ACC_BY_GROUP) OVER() AS "TOTAL_ACC",
    SUM(TR_BY_GROUP) OVER() AS "TOTAL_TR",
    TO_NUMBER(TR_BY_GROUP / TOTAL_TR * 100,10,2) AS "TR %",
    TO_NUMBER(ACC_BY_GROUP / TOTAL_ACC * 100,10,2) AS "ACC %",
    CONCAT(T_IAP.R_GROUP,', ',ACC_BY_GROUP, ' Account(s)') AS "FINAL"
    
FROM(SELECT
        DATE(CLIENT_TIME) AS "DATE",
        FED_ID AS "FED",
        PLATFORM,
        SUBSTRING(ORIGINAL_CONTENT_ID, CHARINDEX('_',ORIGINAL_CONTENT_ID) + LEN('_'), LEN(ORIGINAL_CONTENT_ID)) AS "PACK",
        COUNT(DISTINCT(FED)) AS "ACCOUNTS",
        COUNT(DISTINCT(TRANSACTION_ID)) AS "TRANSACTONS",
        DENSE_RANK() OVER(PARTITION BY PACK ORDER BY TRANSACTONS DESC) AS "RANK",
        CONCAT ('Rank ',RANK,' - ',TRANSACTONS,' Transaction(s)') AS "R_GROUP"
        
     FROM 
        "ELEPHANT_DB"."MOE"."IAP"
     WHERE
        CLIENT_TIME >= '{st_date}'
        AND CLIENT_TIME <= '{end_date}'
        AND ORIGINAL_CONTENT_ID LIKE '%{filter_value}'
     GROUP BY 
        DATE,
        FED,
        PLATFORM,
        PACK
      ORDER BY DATE ASC, TRANSACTONS DESC
      LIMIT 10000
    ) AS T_IAP

WHERE 
    DATE >= '{st_date}'
    AND DATE <= '{end_date}'
GROUP BY
    DATE,
    PACK,
    R_GROUP,
    TRANSACTONS
ORDER BY DATE,R_GROUP ASC
LIMIT 10000
;
'''