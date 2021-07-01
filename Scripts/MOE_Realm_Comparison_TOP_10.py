TYPE = "Alliance"
CREDENTIAL = "NO"
FILTER = "...TO REALM"
SILO = "YES"
REALM = "YES"
DATE = "YES"

SQL_REQ =   '''
SELECT
    T_IN.SILO,
    T_IN.REALM,
    RANK_N,
    T_IN.FED,
    T_IN.NAME,
    T_IN.CASTLE_LEVEL,
    T_IN.MAX_ARMY_MIGHT,
    T_IN.FOOD,
    T_IN.WOOD,
    T_IN.STONE,
    T_IN.IRON,
    T_IN.SILVER,
    MAX(T_REVENUE.COUNTRY) AS COUNTRY,
    SUM(T_REVENUE.TRANSACTIONS_TODAY) AS Period_Transactions,
    SUM(TO_NUMBER(T_REVENUE.REVENUE_TODAY,20,2)) AS Period_Revenue,
    MAX(TO_NUMBER(T_REVENUE.REVENUE_TO_DATE,20,2)) AS All_Time_Revenue
        FROM(SELECT
            DATA_CENTER_ID AS "SILO",
            EVENT_DATA:realm_id::INT AS "REALM",
            FED_ID AS "FED",
            MAX(EVENT_DATA:ingame_nickname_active::STRING) AS "NAME",
            MAX(EVENT_DATA:progress_index02::INT) AS "CASTLE_LEVEL",
            MAX(EVENT_DATA:consumable_power_balance::INT) AS "MAX_ARMY_MIGHT",
            MAX(EVENT_DATA:soft_currency1_balance::INT) AS "FOOD",
            MAX(EVENT_DATA:soft_currency2_balance::INT) AS "WOOD",
            MAX(EVENT_DATA:soft_currency3_balance::INT) AS "STONE",
            MAX(EVENT_DATA:soft_currency4_balance::INT) AS "IRON",
            MAX(EVENT_DATA:soft_currency5_balance::INT) AS "SILVER",
            ROW_NUMBER() OVER (PARTITION BY REALM ORDER BY MAX_ARMY_MIGHT DESC) AS RANK_N
        FROM
            "ELEPHANT_DB"."MOE"."PLAYER_CONNECTION_REPORT_RAW"
        WHERE
            SERVER_TIME >= '{st_date}'
            AND SERVER_TIME < '{end_date}'
            AND "SILO" LIKE '{silo}'
            AND "REALM" >= {realm}
            AND "REALM" <= {filter_value}
            AND USER_ID > 0
        GROUP BY 1,2,3) AS T_IN
    LEFT JOIN
        "ELEPHANT_DB"."MOE"."USER_ACTIVITY_FED" AS T_REVENUE
            ON (T_IN.FED = T_REVENUE.FED_ID
                AND T_REVENUE.ACTIVE_DATE >= '{st_date}'
                AND T_REVENUE.ACTIVE_DATE < '{end_date}'
                AND T_REVENUE.GAME_BUILD = 'moe')
WHERE
    T_IN.RANK_N <= 10
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12
ORDER BY REALM ASC, MAX_ARMY_MIGHT DESC
;
'''