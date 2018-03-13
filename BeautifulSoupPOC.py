


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import urllib2
import re
import json
import time


df_train = pd.read_csv('train.csv', nrows  = 3)


def gen_project_url(project):
    project_id = project.project_id[4:]
    name = project.name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '')
    return "https://www.kickstarter.com/projects/" + project_id + "/" + name;

def validate_data(df_value, scrape_value):
    if df_value == scrape_value:
        print True
    else:
        print False
        print df_value
        print scrape_value

def gen_json_from(soup):
    json_str = str(soup.find(text=re.compile(r'window.current_project')))
    json_str = json_str.replace('&quot;', '"')
    json_str = re.search('window\.current_project.*', json_str).group(0)
    json_str = re.search('"{.*', json_str).group(0)
    json_str = json_str[1:-2]
    json_str = json_str.replace('&#39;', "'")
    json_str = json_str.replace(r'\\"', "'")
    json_str = json.loads(json_str)
    return json_str;

def validate_data(df_value, scrape_value):
    if df_value == scrape_value:
        print True
    else:
        print False
        print df_value
        print scrape_value

def validate_project(project_tup, current_project):
    validate_data(project_tup.goal, current_project['goal'])
    validate_data(project_tup.country, current_project['country'])
    validate_data(project_tup.currency, current_project['currency'])
    validate_data(project_tup.deadline, current_project['deadline'])
    validate_data(project_tup.state_changed_at, current_project['state_changed_at'])
    validate_data(project_tup.created_at, current_project['created_at'])
    validate_data(project_tup.launched_at, current_project['launched_at'])
    validate_data(project_tup.backers_count, current_project['backers_count'])
    validate_data(project_tup.final_status, (1 if float(current_project['usd_pledged']) > current_project['goal'] else 0))

for project in df_train.itertuples():
    url = gen_project_url(project)
    print url
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    current_project = gen_json_from(soup)
    validate_project(project, current_project)
    time.sleep(5)

def time_to_debug(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    json_str = str(soup.find(text=re.compile(r'window.current_project')))
    json_str = json_str.replace('&quot;', '"')
    json_str = re.search('window\.current_project.*', json_str).group(0)
    json_str = re.search('"{.*', json_str).group(0)
    json_str = json_str[1:-2]
    json_str = json_str.replace('&#39;', "'")
    json_str = json_str.replace(r'\\"', "'")
    # print json_str
    return json_str

# my_string = time_to_debug('https://www.kickstarter.com/projects/183622197/mr-squiggles')
# my_list = "".join(list(my_string)[1900:2100])
# print my_list

# https://www.kickstarter.com/projects/183622197/mr-squiggles
# Traceback (most recent call last):
#   File "BeautifulSoupPOC.py", line 63, in <module>
#     current_project = gen_json_from(soup)
#   File "BeautifulSoupPOC.py", line 36, in gen_json_from
#     json_str = json.loads(json_str)
#   File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 338, in loads
#     return _default_decoder.decode(s)
#   File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 366, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#   File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 382, in raw_decode
#     obj, end = self.scan_once(s, idx)
# ValueError: Expecting , delimiter: line 1 column 2025 (char 2024)




#Goal
