import sqlite3
from sqlite3 import Error
import os.path
import csv
import pandas as pd
import urllib2
import time


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def gen_project_url(project_id, name):
    project_id = project_id[4:]
    name = name.decode("utf-8")
    name = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '').replace('---', '-').replace('"', '').replace("'", '')[:50]
    project_url = "https://www.kickstarter.com/projects/" + project_id + "/" + name
    return  project_url

def test_gen_project_url():

# def get_campaign(row):
#     if row['campaign'] == None:
#         # try:
#         content = urllib2.urlopen(row['url']).read()
#         print "Content found"
#         time.sleep(5)
#         return content
#         # except Exception:
#             # print "Content not found found"
#             # print row['url']
#             # time.sleep(5)
#             # return None
#     else:
#         print "Already have campaign"
#         time.sleep(5)
#         return row['campaign']

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
    c.execute('SELECT project_id, name, url, campaign FROM Projects WHERE campaign IS NULL LIMIT 1')
    data = c.fetchall()
    for row in data:
        project_id = row[0]
        print project_id
        name = row[1]
        print name
        url = gen_project_url(project_id, name)
        print url
        c.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [False, False, project_id])
        conn.commit()
        campaign = urllib2.urlopen(url).read()
        c.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [url, campaign, project_id])
        conn.commit()
    c.close()
    conn.close()

for i in range(1, 100):
    get_campaign()
    time.sleep(30)


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
