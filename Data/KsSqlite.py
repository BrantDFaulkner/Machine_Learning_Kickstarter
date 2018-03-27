import sqlite3
import os.path
import csv
import pandas as pd

class KsSqlite:

    def db_connection(self, db_file_path):
        try:
            conn = sqlite3.connect(db_file_path)
            return conn
        except Error as e:
            print(e)
        return None

    def abs_file_path(self, rel_file_path):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, rel_file_path)
        return path

    def csv_to_sqlite(self, csv_path, db_connection, table_name):
        db_connection.text_factory = str
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, db_connection, if_exists='replace', index=False)
        db_connection.close()
        return df

# CONVERT CSV TO SQLite
# ksq = KsSqlite()
# db_file_path = ksq.abs_file_path("mlks_sample.db")
# db_connection = ksq.db_connection(db_file_path)
# df = ksq.csv_to_sqlite("train_sample.csv", db_connection, "Projects")
