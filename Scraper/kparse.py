from ksqlite import ksqlite
from bs4 import BeautifulSoup
import re
import json
import numpy as np

class kparse:

    def load_json_from_campaign(self, soup):
        script = soup.find("script", string=re.compile(r'window.current_project')).string
        json_str = re.search('window\.current_project.*', script).group(0)[26:-2]
        json_str = json_str.replace('&quot;', '"').replace(r'\\', '\\')
        json_load = json.loads(json_str)
        return json_load

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

    def parse_project_campaigns(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        ksq_parsed = ksqlite("../Data/mlks_parsed.db")
        projects = ksq_scraped.select_all_project_ids_and_campaigns()
        count = 0
        for project in projects:
            soup = BeautifulSoup(project["campaign"], 'html.parser')
            x = self.load_json_from_campaign(soup)
            count = count + 1
            print(count)
            for key, value in self.flatten_dict(x).items():
                ksq_parsed.update_field("Projects", key, str(value), "project_id", project["project_id"])

    def parse_full_descriptions(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        ksq_parsed = ksqlite("../Data/mlks_parsed.db")
        projects = ksq_scraped.select_all_project_ids_and_campaigns()
        count = 0
        no_text = 0
        for project in projects:
            try:
                soup = BeautifulSoup(project["campaign"], 'html.parser')
                full_description = soup.find("div", {"class": "full-description"})
                full_description =  ' '.join(re.sub(r'[\t\r\n]', '', full_description.text).split())
                ksq_parsed.update_field("Projects", "full_description", full_description, "project_id", project["project_id"])
                count = count + 1
                print(count)
            except:
                no_text = no_text + 1
                print(no_text)
                pass


    def parse_and_insert_creator_id(self):
        ksq = ksqlite()
        db_connection = ksq.db_connection("../Data/mlks.db")
        projects = ksq.select_creator_is_null(db_connection)
        for project in projects:
            soup = BeautifulSoup(project["campaign"], 'html.parser')
            creator_id = self.load_json_from_campaign(soup)["creator"]["id"]
            ksq.update_creator_id(db_connection, creator_id, project["id"])
        db_connection.close()

    #DEBUGGING JSON
    def segment_string(self, string, begin_range, end_range):
        segment = "".join(list(string)[begin_range:end_range])
        return segment

    def pretty_print_json(self, json_str):
        print(json.dumps(json_str, indent=4, sort_keys=True))

    def list_all_fields(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        campaigns = ksq_scraped.select_all_campaigns()
        fields = []
        count = 0
        for campaign in campaigns:
            soup = BeautifulSoup(campaign["campaign"], 'html.parser')
            json_dict = self.load_json_from_campaign(soup)
            for key, value in self.flatten_dict(json_dict).items() :
                fields.append(key)
                fields = list(set(fields))
            count = count + 1
            print(count)
            print(len(fields))

        print(sorted(fields))

    def parse_creator_social(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        ksq_parsed = ksqlite("../Data/mlks_parsed.db")
        creators = ksq_scraped.select_all_creator_about()
        count = 0
        for creator in creators:
            soup = BeautifulSoup(creator["about"], 'html.parser')
            for link in soup.find_all('a'):
                link = link.get('href')
                if re.search('//www\.facebook\.com/', link):
                    ksq_parsed.update_field("Creators", "facebook", link, "creator_id", creator["creator_id"])
                if re.search('//www\.twitter\.com/', link):
                    ksq_parsed.update_field("Creators", "twitter", link, "creator_id", creator["creator_id"])
                if re.search('//www\.youtube\.com/', link):
                    ksq_parsed.update_field("Creators", "youtube", link, "creator_id", creator["creator_id"])
            count = count + 1
            print(count)

    def parse_creator_backed(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        ksq_parsed = ksqlite("../Data/mlks_parsed.db")
        creators = ksq_scraped.select_all_creator_about()
        count = 0
        for creator in creators:
            soup = BeautifulSoup(creator["about"], 'html.parser')
            for link in soup.find_all('a'):
                for link in soup.findAll("a", {"class": "js-backed-link"}):
                    for span in link.findAll("span", {"class": "count"}):
                        backed = span.string.strip()
                        ksq_parsed.update_field("Creators", "backed", backed, "creator_id", creator["creator_id"])
            count = count + 1
            print(count)

    def parse_creator_biograpy(self):
        ksq_scraped = ksqlite("../Data/mlks_scraped.db")
        ksq_parsed = ksqlite("../Data/mlks_parsed.db")
        creators = ksq_scraped.select_all_creator_about()
        count = 0
        for creator in creators:
            soup = BeautifulSoup(creator["about"], 'html.parser')
            for biograpy in soup.findAll("p", {"class": "mb3"}):
                biograpy =  ' '.join(re.sub(r'[\t\r\n]', '', biograpy.text.strip()).split())
                ksq_parsed.update_field("Creators", "biograpy", biograpy, "creator_id", creator["creator_id"])
            count = count + 1
            print(count)


        #biography






kparse().parse_creator_biograpy()




    # def make_all_the_columns(self):
    #     conn_mlks = ksqlite().db_connection("../Data/mlks.db")
    #     cur_mlks = conn_mlks.cursor()
    #     cur_mlks.execute('SELECT campaign FROM Projects LIMIT 10000')
    #     data = cur_mlks.fetchall()
    #     conn_mlks_parse = ksqlite().db_connection("../Data/mlks_parsed.db")
    #     for campaign in data:
    #         soup = BeautifulSoup(campaign[0], 'html.parser')
    #         x = self.load_json_from_campaign(soup)
    #         for key, value in self.flatten_dict(x).items() :
    #             ksqlite().add_column(conn_mlks_parse, "Projects", key, "TEXT")
    #     c.close()
    #     conn.close()





# kparse().parse_projects()
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks_parsed.db")
# db_connection = ksq.db_connection(db_file_path)
# # ksq.create_table(db_connection)
# # ksq.add_column(db_connection, "Projects", "JJJJJ", "TEXT")
# db_connection.close()
