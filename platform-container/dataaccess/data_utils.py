import pandas as pd
import sqlite3

APP_DATA_DB = "datastore/app_data.db"

connection = sqlite3.connect(APP_DATA_DB)


def execute_query(sql):
    print(sql)

    # Fetch rows
    rows = pd.read_sql_query(sql, connection)

    return rows


def drop_table(table_name):
    cursor = connection.cursor()
    cursor.executescript('drop table if exists {0};'.format(table_name))


def load_data_from_df(df,table_name,if_exists='replace'):
    df.to_sql(table_name, connection, if_exists=if_exists, index=False)
