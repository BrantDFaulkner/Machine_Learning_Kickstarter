
import sqlite3
from sqlite3 import Error
import os.path
import csv
import pandas as pd
import urllib2
import time
from KsUrl import KsUrl
import numpy as np



def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def gen_path():
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/mlks.db")
    return path

def gen_connection(path):
    conn = create_connection(path)
    conn.text_factory = str
    return conn

def get_campaign():
    conn = gen_connection(gen_path())
    c = conn.cursor()
    c.execute('SELECT project_id, keywords, url, campaign FROM Projects WHERE campaign IS NULL or campaign = 0 LIMIT 1')
    data = c.fetchall()
    for row in data:
        project_id = row[0]
        print project_id
        keywords = row[1]
        print keywords
        # url = gen_project_url(project_id, name)
        ksurl = KsUrl(project_id, keywords)
        url = ksurl.gen_url()
        print url
        c.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [False, False, project_id])
        conn.commit()
        campaign = urllib2.urlopen(url).read()
        c.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [url, campaign, project_id])
        conn.commit()
    c.close()
    conn.close()

for i in range(1, 10000):
    get_campaign()
    sleep = np.random.normal(30,4,1)
    print sleep
    time.sleep(sleep)


# def del_and_update():
#     c.execute('SELECT * FROM stuffToPlot')
#     for row in c.fetchall():
#         print row



# conn = gen_connection(gen_path())
# my_path = os.path.abspath(os.path.dirname(__file__))
# path = os.path.join(my_path, "../data/mlks.db")
# conn = create_connection(path)
# conn.text_factory = str
# cur = conn.cursor()

# ADD NEW COLUMNS
# cur.execute("ALTER TABLE Projects ADD 'url' 'TEXT';")
# cur.execute("ALTER TABLE Projects ADD 'campaign' 'TEXT';")

# df = pd.read_sql_query("SELECT * FROM Projects WHERE campaign == NULL limit 1;", conn)
# print df
# df['url'] = df.apply(gen_project_url, axis = 1)
# df['campaign'] = df.apply(get_campaign, axis = 1)
# print df[0]



# df = pd.read_sql_query("SELECT * FROM Projects WHERE limit 5;", conn)
# df['url'] = df.apply(gen_project_url, axis = 1)
# df['campaign'] = df.apply(get_campaign, axis = 1)
# df.to_sql("Projects", conn, if_exists='replace', index=False)

# conn.close()

# results = cur.fetchall()
# print(results)

# df = pd.read_sql_query("select * from projets;", conn)


# df['url'] = df.apply(gen_project_url, axis = 1)
# df['campaign'] = df.apply(get_campaign, axis = 1)
# df.apply(print_campaign, axis = 1)


# for project in df.itertuples():
#     url = gen_project_url(project_id, project_name)
#     print url
#     content = urllib2.urlopen(url).read()
#     # soup = BeautifulSoup(content, 'lxml')
#     # current_project = gen_json_from(soup)
#     # validate_project(project, current_project)
#     time.sleep(5)

#df = pd.read_csv('../data/train.csv')
# df.to_sql("Projects", conn, if_exists='replace', index=False)
