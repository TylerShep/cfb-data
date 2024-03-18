import datetime
import psycopg2
import pandas as pd


# PostgresConnect
class PusherService():

    def getConnection(self):
        conn = psycopg2.connect(
            dbname='cfb_db',
            user='cfb',
            password='cs1400SUCKS!',
            host='dfb-db.cb4e0eyekomu.us-east-1.rds.amazonaws.com',
            port=5432
        )

        return conn

    def correctNullValuesPostgres(df, table_name):
        conn = PusherService.getConnection()
        cursor = conn.cursor()

        for col in df.columns:
            if df[col].isna().any():
                query = f"{col} = null"
                conditions = f"{col} = 'NaN'"
                update_query = f"UPDATE {table_name} SET {query} WHERE {conditions};"

                cursor.execute(update_query)
                conn.commit()

    def createPostgresTable(df: pd.DataFrame, table_name: str):
        PG_TYPE_MAPPING = {
            'int64': 'integer',
            'datetime64[ns]': 'timestamp',
            'float64': 'numeric'}

        conn = PusherService.getConnection()
        cursor = conn.cursor()

        columns = ', '.join([col + ' ' + PG_TYPE_MAPPING.get(df[col].dtype.name, df[col].dtype.name) for col in df])
        columns = columns.replace("object", "text")
        create_table_query = f"CREATE TABLE IF NOT EXISTS d_{table_name} ({columns}, updated_on timestamp);"
        table_name = f"d_{table_name}"

        cursor.execute(create_table_query)
        conn.commit()

        return table_name

    def pushToPostgres(df, table_name):
        conn = PusherService.getConnection()
        cursor = conn.cursor()

        for index, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(['%s'] * len(row))
            placeholders = ', '.join(['%s'] * len(row))
            row_data = [None if pd.isna(value) else value for value in row]

            query = f"INSERT INTO {table_name} ({columns}, updated_on) VALUES ({placeholders}, %s)"
            data = list(row.values) + [datetime.datetime.now()]

            cursor.execute(query, data)
            conn.commit()

        cursor.close()
        conn.close()