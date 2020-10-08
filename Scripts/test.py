TYPE = "Player"
CREDENTIAL = "YES"
FILTER = "NO"
SILO = "YES"
REALM = "NO"
DATE = "YES"

SQL_REQ = '''
SELECT DISTINCT
    PLAYER_LOST_UNITS:l::STRING AS "LOST",
    PLAYER_LOST_UNITS:w::STRING AS "WOUNDED",
    RESOURCES_STOLEN AS "RESOURCES"
FROM "ELEPHANT_DB"."MOE"."COMBAT_INTERACTION"
WHERE 
    CLIENT_TIME >= '{st_date}'
    AND CLIENT_TIME < '{end_date}'
    AND FED_ID = '{account}'
    AND COMBAT_INT LIKE 'Defend%'
LIMIT 5000
;
'''
POST_PY = '''
if len(q_result) != 0:
    lost_df = pd.DataFrame(q_result["LOST"])
    lost_df = pd.json_normalize(lost_df["LOST"].apply(json.loads))
    lost_df = lost_df.sum(axis=0)
    lost_df = lost_df.rename_axis('UNITS')
    lost_df = lost_df.to_frame().reset_index()
    lost_df.rename(columns = {lost_df.columns[1]: "LOST"}, inplace=True)
    lost_df = lost_df.apply(pd.to_numeric, errors='ignore')
    lost_df['UNITS'] = lost_df['UNITS'].map(interactions.units_dict)
    # print(lost_df)

    w_df = pd.DataFrame(q_result["WOUNDED"])
    w_df = pd.json_normalize(w_df["WOUNDED"].apply(json.loads))
    w_df = w_df.sum(axis=0)
    w_df = w_df.rename_axis('UNITS')
    w_df = w_df.to_frame().reset_index()
    w_df.rename(columns = {w_df.columns[1]: "WOUNDED"}, inplace=True)
    w_df = w_df.apply(pd.to_numeric, errors='ignore')
    w_df['UNITS'] = w_df['UNITS'].map(interactions.units_dict)
    # print(w_df)

    units_df = pd.merge(lost_df, w_df, how = 'outer', on = ['UNITS'])

    res_df = pd.DataFrame(q_result["RESOURCES"])
    res_df = pd.json_normalize(res_df["RESOURCES"].apply(json.loads))
    res_df = res_df.sum(axis=0)
    res_df = res_df.rename_axis('UNITS')
    res_df = res_df.to_frame().reset_index()
    res_df.rename(columns = {res_df.columns[1]: "LOST"}, inplace=True)
    res_df = res_df.apply(pd.to_numeric, errors='ignore')
    res_df['UNITS'] = res_df['UNITS'].map(interactions.res_dict)
    # print(res_df)

    q_result = pd.merge(units_df, res_df, how = 'outer', on = ['UNITS','LOST'])
    # print(q_result)
'''