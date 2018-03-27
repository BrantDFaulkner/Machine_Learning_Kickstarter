import sqlite3
from sqlite3 import Error
import os.path
import pandas as pd
from bs4 import BeautifulSoup
import re
import json


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

def json_text(soup):
    script = soup.find("script", string=re.compile(r'window.current_project'))
    json_str = script.string
    json_str = re.search('window\.current_project.*', json_str).group(0)
    json_str = json_str[26:-2]
    json_str = json_str.replace('&quot;', '"')
    json_str = json_str.replace(r'\\', '\\')
    json_load = json.loads(json_str)
    return json_str

def print_json_segment(json_str, begin_range, end_range):
    segment = "".join(list(json_str)[begin_range:end_range])
    return segment

def pretty_print_json(json_str):
    print json.dumps(json_str, indent=4, sort_keys=True)

def get_text(soup):#MOVE TO PARSER
    div = soup.find("div", {"class": "full-description"})
    return div

def get_soup():
    conn = gen_connection(gen_path())
    c = conn.cursor()
    c.execute('SELECT campaign FROM Projects LIMIT 5')
    data = c.fetchall()
    for campaign in data:
        soup = BeautifulSoup(campaign[0], 'html.parser')
        div = get_text(soup)
        x = json_text(soup)
        # print x["backers_count"]
    c.close()
    conn.close()

get_soup()
