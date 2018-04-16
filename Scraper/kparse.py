from ksqlite import ksqlite
from bs4 import BeautifulSoup
import re
import json

class kparse:

    def json_text(self, soup):
        script = soup.find("script", string=re.compile(r'window.current_project'))
        json_str = script.string
        json_str = re.search('window\.current_project.*', json_str).group(0)
        json_str = json_str[26:-2]
        json_str = json_str.replace('&quot;', '"')
        json_str = json_str.replace(r'\\', '\\')
        json_load = json.loads(json_str)
        return json_load

    #for debuggging json strings
    def print_json_segment(self, json_str, begin_range, end_range):
        segment = "".join(list(json_str)[begin_range:end_range])
        return segment

    def pretty_print_json(self, json_str):
        print(json.dumps(json_str, indent=4, sort_keys=True))

    def extract_full_description(self, soup):
        div = soup.find("div", {"class": "full-description"})
        return div

    def flatten_dict(self, d):
        def expand(key, value):
            if isinstance(value, dict):
                return [ (key + '_' + k, v) for k, v in self.flatten_dict(value).items() ]
            else:
                return [ (key, value) ]
        items = [ item for k, v in d.items() for item in expand(k, v) ]
        return dict(items)

    def my_str(self, arg):
            try:
                arg = str(arg)
            except:
                arg = arg.encode('utf-8')
            return arg

    def parse_projects(self):
        conn_mlks = ksqlite().db_connection("../Data/mlks.db")
        cur_mlks = conn_mlks.cursor()
        cur_mlks.execute('SELECT project_id, campaign FROM Projects LIMIT 10000')
        data = cur_mlks.fetchall()
        conn_mlks_parse = ksqlite().db_connection("../Data/mlks_parsed.db")
        count = 0
        for row in data:
            count = count + 1
            print(count)
            project_id = row[0]
            ksqlite().insert_project(conn_mlks_parse, project_id)
            campaign = row[1]
            soup = BeautifulSoup(campaign, 'html.parser')
            x = self.json_text(soup)
            for key, value in self.flatten_dict(x).items():
                ksqlite().update_field(conn_mlks_parse, project_id, key, self.my_str(value))
        cur_mlks.close()
        conn_mlks.close()
        conn_mlks_parse.close()

    def parse_and_update_creator_id(self):
        ksq = ksqlite()
        db_connection = ksq.db_connection("../Data/mlks.db")
        projects = ksq.select_creator_is_null(db_connection)
        for project in projects:
            soup = BeautifulSoup(project["campaign"], 'html.parser')
            creator_id = self.json_text(soup)["creator"]["id"]
            ksq.update_creator_id(db_connection, creator_id, project["id"])
        db_connection.close()






    # def make_all_the_columns(self):
    #     conn_mlks = ksqlite().db_connection("../Data/mlks.db")
    #     cur_mlks = conn_mlks.cursor()
    #     cur_mlks.execute('SELECT campaign FROM Projects LIMIT 10000')
    #     data = cur_mlks.fetchall()
    #     conn_mlks_parse = ksqlite().db_connection("../Data/mlks_parsed.db")
    #     for campaign in data:
    #         soup = BeautifulSoup(campaign[0], 'html.parser')
    #         x = self.json_text(soup)
    #         for key, value in self.flatten_dict(x).items() :
    #             ksqlite().add_column(conn_mlks_parse, "Projects", key, "TEXT")
    #     c.close()
    #     conn.close()

count = 0
while True:
        kparse().parse_and_update_creator_id()
        count = count + 100
        print(count)



# kparse().parse_projects()
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks_parsed.db")
# db_connection = ksq.db_connection(db_file_path)
# # ksq.create_table(db_connection)
# # ksq.add_column(db_connection, "Projects", "JJJJJ", "TEXT")
# db_connection.close()
