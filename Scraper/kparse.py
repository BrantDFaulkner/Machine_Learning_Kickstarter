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

    def print_json_segment(self, json_str, begin_range, end_range):
        segment = "".join(list(json_str)[begin_range:end_range])
        return segment

    def pretty_print_json(self, json_str):
        print json.dumps(json_str, indent=4, sort_keys=True)

    def get_text(self, soup):
        div = soup.find("div", {"class": "full-description"})
        return div

    def get_soup(self):
        conn = ksqlite().db_connection("../Data/mlks.db")
        c = conn.cursor()
        c.execute('SELECT campaign FROM Projects LIMIT 10')
        data = c.fetchall()
        for campaign in data:
            soup = BeautifulSoup(campaign[0], 'html.parser')
            about = self.get_text(soup)
            print about #poc text parse
            x = self.json_text(soup)
            print x["backers_count"] #poc dictionary parse
        c.close()
        conn.close()

kparse().get_soup()
