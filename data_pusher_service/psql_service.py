from psycopg2 import sql
import psycopg2
import pandas as pd
import datetime

class PusherService ():

  def __init__(self) -> None:
    pass

  def getConnection():
    conn = psycopg2.connect(
      dbname='cfb_db',
      user='cfb',
      password='cs1400SUCKS!',
      host='dfb-db.cb4e0eyekomu.us-east-1.rds.amazonaws.com',
      port=5432
      )
    
    return conn

  def pushToPostgres(df, table_name):
        conn = PusherService.getConnection()
        cursor = conn.cursor()

        for index, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(['%s'] * len(row))
            placeholders = ', '.join(['%s'] * len(row))

            query = f"INSERT INTO {table_name} ({columns}, updated_on) VALUES ({placeholders}, %s)"
            data = list(row.values) + [datetime.datetime.now()]

            cursor.execute(query, data)
            conn.commit()

        cursor.close()
        conn.close()
    
