TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ =   '''
SELECT
    T_IN.SILO,
    T_IN.DATE,
    T_IN.REALM,
    RANK_N,
    T_IN.FED,
    T_IN.NAME,
    T_IN.CASTLE_LEVEL,
    T_IN.MAX_ARMY_MIGHT,
    MAX(T_REVENUE.COUNTRY) AS COUNTRY,
    SUM(T_REVENUE.TRANSACTIONS_TODAY) AS Period_Transactions,
    SUM(TO_NUMBER(T_REVENUE.REVENUE_TODAY,20,2)) AS Period_Revenue,
    MAX(TO_NUMBER(T_REVENUE.REVENUE_TO_DATE,20,2)) AS All_Time_Revenue
        FROM(SELECT
              DATA_CENTER_ID AS "SILO",
              DATE(CLIENT_TIME) AS "DATE",
              EVENT_DATA:realm_id_current::INT AS "REALM",
              FED_ID AS "FED",
              MAX(EVENT_DATA:ingame_nickname_active::STRING) AS "NAME",
              MAX(EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
              MAX(EVENT_DATA:consumable_power_balance::INT) AS "MAX_ARMY_MIGHT",
              ROW_NUMBER() OVER (PARTITION BY REALM ORDER BY MAX_ARMY_MIGHT DESC) AS RANK_N
        FROM
            "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW"
        WHERE
            CLIENT_TIME >= '{st_date}'
            AND CLIENT_TIME < '{end_date}'
            AND "SILO" LIKE '{silo}'
            AND "REALM" >= 4500
            AND "REALM" <= 5000
            AND USER_ID > 0
        GROUP BY 1,2,3,4) AS T_IN
    LEFT JOIN
        "ELEPHANT_DB"."MOE"."USER_ACTIVITY_FED" AS T_REVENUE
            ON (T_IN.FED = T_REVENUE.FED_ID
                AND T_REVENUE.ACTIVE_DATE >= '{st_date}'
                AND T_REVENUE.ACTIVE_DATE < '{end_date}'
                AND T_REVENUE.GAME_BUILD = 'moe')
WHERE
    T_IN.RANK_N <= 10000
GROUP BY 1,2,3,4,5,6,7,8
ORDER BY REALM ASC, MAX_ARMY_MIGHT DESC
;
'''