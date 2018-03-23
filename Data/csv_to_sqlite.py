
import sqlite3
# from sqlite3 import Error
import os.path
import csv
import pandas as pd
# import urllib2
# import time





def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "mlks.db")
conn = create_connection(path)
conn.text_factory = str

df = pd.read_csv('train.csv')
df.to_sql("Projects", conn, if_exists='replace', index=False)
