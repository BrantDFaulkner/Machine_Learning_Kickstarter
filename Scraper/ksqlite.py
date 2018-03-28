import sqlite3
from sqlite3 import Error
import os.path
import csv
import pandas as pd

class ksqlite:

    def db_connection(self, db_file_path):
        try:
            conn = sqlite3.connect(db_file_path)
            conn.text_factory = str
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

    def select_campaign_is_null(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT project_id, keywords FROM Projects WHERE campaign IS NULL or campaign = 0 LIMIT 1')
        data = cursor.fetchall()[0]
        cursor.close()
        project = {"id": data[0], "keywords": data[1]}
        return project

    def update_campaign(self, db_connection, url, campaign, project_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [url, campaign, project_id])
        db_connection.commit()
        cursor.close()

# CONVERT CSV TO SQLite
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks_sample.db")
# db_connection = ksq.db_connection(db_file_path)
# df = ksq.csv_to_sqlite("../Data/train_sample.csv", db_connection, "Projects")

# ADD NEW COLUMNS
# cur.execute("ALTER TABLE Projects ADD 'url' 'TEXT';")
# cur.execute("ALTER TABLE Projects ADD 'campaign' 'TEXT';")
