TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT
    DATE(T_ArmyInt.CLIENT_TIME) AS "DATE",
    HOUR(T_ArmyInt.CLIENT_TIME) AS "HOUR",
    COUNT(DISTINCT("HOUR")) OVER (PARTITION BY DATE) AS "TOTAL_HOURS",
    T_ArmyInt.USER_ID AS "DEVICE",
    T_User_Device.EVENT_DATA:d_device_family::STRING AS "DEVICE_TYPE",
    T_Element.NAME AS "PURPOSE",
    COUNT(DISTINCT(T_ArmyInt.EVENT_DATA:march::INT)) AS "MARCHES_FOR_HOUR",
    SUM(MARCHES_FOR_HOUR) OVER (PARTITION BY DATE) AS "MARCHES_FOR_DAY",
    TO_NUMBER(MARCHES_FOR_DAY / TOTAL_HOURS,10,0) AS "AVG_M_FOR_DAY",
    SUM(MARCHES_FOR_HOUR) OVER () AS "T_MARCHES_PERIOD",
    T_ArmyInt.FED_ID AS "FED"
FROM 
    "ELEPHANT_DB"."MOE"."ARMY_INTERACTION_RAW" AS T_ArmyInt
LEFT JOIN
    "ELEPHANT_DB"."DIMENSIONS"."ELEMENT" AS T_Element
        ON (T_ArmyInt.EVENT_DATA:army_purpose::INT = T_Element.ID)
LEFT JOIN
    "ELEPHANT_DB"."MOE"."USER_DEVICE_RAW" AS T_User_Device
        ON (T_ArmyInt.USER_ID = T_User_Device.USER_ID
            AND T_User_Device.CLIENT_TIME > '{st_date}'
            AND T_User_Device.CLIENT_TIME < '{end_date}'
            AND T_User_Device.FED_ID = '{account}')
WHERE
    T_ArmyInt.CLIENT_TIME > '{st_date}'
    AND T_ArmyInt.CLIENT_TIME < '{end_date}'
    AND T_ArmyInt.DATA_CENTER_ID LIKE '{silo}'
    AND T_ArmyInt.FED_ID = '{account}'
    AND T_ArmyInt.EVENT_DATA:army_int = '223795'
GROUP BY 1,2,4,5,6,11
ORDER BY DATE,HOUR ASC
LIMIT 10000
;
'''