import sys
import pandas as pd
import xlsxwriter
import pyarrow
import snowflake.connector

import datetime
import json
import importlib
from os import path, listdir, remove, startfile
import ctypes

res_dict = {
                0:'Food',
                1:'Wood',
                2:'Stone',
                3:'Iron',
                4:'Silver',
                5:'Other'
            }

units_dict = {
                197896:'kni_sword_t1',
                197897:'kni_sword_t2',
                197898:'kni_sword_t3',
                197990:'kni_sword_t4',
                197991:'kni_sword_t5',
                197992:'kni_spear_t1',
                197993:'kni_spear_t2',
                197994:'kni_spear_t3',
                197995:'kni_spear_t4',
                197996:'kni_spear_t5',
                197997:'kni_mount_t1',
                197998:'kni_mount_t2',
                197999:'kni_mount_t3',
                198000:'kni_mount_t4',
                198001:'kni_mount_t5',
                198002:'kni_range_t1',
                198003:'kni_range_t2',
                198004:'kni_range_t3',
                198005:'kni_range_t4',
                198006:'kni_range_t5',
                198007:'kni_siege_t1',
                198008:'kni_siege_t2',
                198009:'kni_siege_t3',
                198010:'kni_siege_t4',
                198011:'kni_siege_t5',
                198012:'sar_sword_t1',
                198013:'sar_sword_t2',
                198014:'sar_sword_t3',
                198015:'sar_sword_t4',
                198016:'sar_sword_t5',
                198017:'sar_spear_t1',
                198018:'sar_spear_t2',
                198019:'sar_spear_t3',
                198020:'sar_spear_t4',
                198021:'sar_spear_t5',
                198022:'sar_mount_t1',
                198023:'sar_mount_t2',
                198024:'sar_mount_t3',
                198025:'sar_mount_t4',
                198026:'sar_mount_t5',
                198027:'sar_range_t1',
                198028:'sar_range_t2',
                198029:'sar_range_t3',
                198030:'sar_range_t4',
                198031:'sar_range_t5',
                198032:'sar_siege_t1',
                198033:'sar_siege_t2',
                198034:'sar_siege_t3',
                198035:'sar_siege_t4',
                198036:'sar_siege_t5',
                198037:'rus_sword_t1',
                198038:'rus_sword_t2',
                198039:'rus_sword_t3',
                198040:'rus_sword_t4',
                198041:'rus_sword_t5',
                198042:'rus_spear_t1',
                198043:'rus_spear_t2',
                198044:'rus_spear_t3',
                198045:'rus_spear_t4',
                198046:'rus_spear_t5',
                198047:'rus_mount_t1',
                198048:'rus_mount_t2',
                198049:'rus_mount_t3',
                198050:'rus_mount_t4',
                198051:'rus_mount_t5',
                198052:'rus_range_t1',
                198053:'rus_range_t2',
                198054:'rus_range_t3',
                198055:'rus_range_t4',
                198056:'rus_range_t5',
                198057:'rus_siege_t1',
                198058:'rus_siege_t2',
                198059:'rus_siege_t3',
                198060:'rus_siege_t4',
                198061:'rus_siege_t5',
                204806:'kni_trap_t1',
                204807:'kni_trap_t2',
                204808:'kni_trap_t3',
                204809:'kni_trap_t4',
                204810:'kni_trap_t5',
                204811:'sar_trap_t1',
                204812:'sar_trap_t2',
                204813:'sar_trap_t3',
                204814:'sar_trap_t4',
                204815:'sar_trap_t5',
                204816:'rus_trap_t1',
                204817:'rus_trap_t2',
                204818:'rus_trap_t3',
                204819:'rus_trap_t4',
                204820:'rus_trap_t5',
                204821:'kni_faction_unit_1',
                204822:'sar_faction_unit_1',
                204823:'rus_faction_unit_1',
                307364:'merc_sword_t1',
                307365:'merc_sword_t2',
                307366:'merc_sword_t3',
                307367:'merc_sword_t4',
                307368:'merc_sword_t5',
                307369:'merc_spear_t1',
                307370:'merc_spear_t2',
                307371:'merc_spear_t3',
                307372:'merc_spear_t4',
                307373:'merc_spear_t5',
                307374:'merc_mount_t1',
                307375:'merc_mount_t2',
                307376:'merc_mount_t3',
                307377:'merc_mount_t4',
                307378:'merc_mount_t5',
                307379:'merc_range_t1',
                307380:'merc_range_t2',
                307381:'merc_range_t3',
                307382:'merc_range_t4',
                307383:'merc_range_t5',
                307384:'merc_siege_t1',
                307385:'merc_siege_t2',
                307386:'merc_siege_t3',
                307387:'merc_siege_t4',
                307388:'merc_siege_t5',
                320906:'kni_faction_unit_2',
                320907:'sar_faction_unit_2',
                320908:'rus_faction_unit_2'}

user = 'orlin.ikonomov'
password = 'Mnogositapg0she5'
account = 'gameloft.eu-west-1'
database = 'ELEPHANT_DB'
role = 'SOF_RAW_DATA'
schema = 'MOE'


ctx = snowflake.connector.connect(
                            user = user,
                            password = password,
                            account = account,
                            database = database,
                            schema = schema
                            )

cs = ctx.cursor()

SQL_REQ = F'''
SELECT
    DATE(CLIENT_TIME) AS "DATE",
    COMBAT_INT AS "ACTION",
    PLAYER_LOST_UNITS:l::STRING AS "LOST",
    PLAYER_LOST_UNITS:w::STRING AS "WOUNDED",
    RESOURCES_STOLEN AS "RESOURCES"
FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION"
WHERE 
    CLIENT_TIME >= '2020-09-10'
    AND CLIENT_TIME < '2020-09-11'
    AND FED_ID = 'e5470b58-f905-11e9-aca4-b8ca3a60b6e4'
ORDER BY DATE,ACTION
LIMIT 5000
;
                            '''        
# print(SQL_REQ)

# try:
cs.execute(F"USE ROLE {role};")
cs.execute(SQL_REQ)

print("Request type: " + str(type(SQL_REQ)))
q_result = pd.read_sql(SQL_REQ, ctx)
print("Return type: " + str(type(q_result)))

if len(q_result) != 0:
    # print(q_result)
    lost_df = pd.json_normalize(q_result["LOST"].apply(json.loads))
    lost_df = lost_df.sum(axis=0)
    lost_df = lost_df.rename_axis('UNITS')
    lost_df = lost_df.to_frame().reset_index()
    lost_df.rename(columns = {lost_df.columns[1]: "LOST"}, inplace=True)
    lost_df = lost_df.apply(pd.to_numeric, errors='ignore')
    lost_df['UNITS'] = lost_df['UNITS'].map(units_dict)

    w_df = pd.DataFrame(q_result["WOUNDED"])
    w_df = pd.json_normalize(w_df["WOUNDED"].apply(json.loads))
    w_df = w_df.sum(axis=0)
    w_df = w_df.rename_axis('UNITS')
    w_df = w_df.to_frame().reset_index()
    w_df.rename(columns = {w_df.columns[1]: "WOUNDED"}, inplace=True)
    w_df = w_df.apply(pd.to_numeric, errors='ignore')
    w_df['UNITS'] = w_df['UNITS'].map(units_dict)
    # print(w_df)

    units_df = pd.merge(lost_df, w_df, how = 'outer', on = ['UNITS'])
    # print(final_df)

    res_df = pd.DataFrame(q_result["RESOURCES"])
    res_df = pd.json_normalize(res_df["RESOURCES"].apply(json.loads))
    res_df = res_df.sum(axis=0)
    res_df = res_df.rename_axis('UNITS')
    res_df = res_df.to_frame().reset_index()
    res_df.rename(columns = {res_df.columns[1]: "LOST"}, inplace=True)
    res_df = res_df.apply(pd.to_numeric, errors='ignore')
    res_df['UNITS'] = res_df['UNITS'].map(res_dict)
    # print(res_df)

    final_df = pd.merge(units_df, res_df, how = 'outer', on = ['UNITS','LOST'])
    # print(final_df)
    final_df.to_csv("temp.csv")

# except:
#     pass