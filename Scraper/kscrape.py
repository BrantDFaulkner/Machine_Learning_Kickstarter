
from ksqlite import ksqlite
import urllib.request
import urllib.error
import time
import numpy as np

class kscrape:

    def campaign_url(self, project_id, project_keywords):
        project_id = project_id[4:]
        campaign_url = "https://www.kickstarter.com/projects/" + project_id + "/" + project_keywords
        return  campaign_url

    # def get_campaign(self):
    #     ksql = ksqlite()
    #     db_connection = ksql.db_connection(ksql.abs_file_path("../Data/mlks.db"))
    #     project = ksql.select_campaign_is_null(db_connection)
    #     url = self.campaign_url(project["id"], project["keywords"])
    #     print url #visual cl progress
    #     campaign = urllib2.urlopen(url).read()
    #     ksql.update_campaign(db_connection, url, campaign, project["id"])
    #     db_connection.close()
    #     return campaign

    def get_campaign(self):
        ksql = ksqlite()
        db_connection = ksql.db_connection(ksql.abs_file_path("../Data/mlks.db"))
        projects = ksql.select_campaign_is_null(db_connection)
        print(projects)
        for project in projects:
            url = self.campaign_url(project["id"], project["keywords"])
            print(url) #visual cl progress
            campaign = urlopen.urlopen(url).read()
            ksql.update_campaign(db_connection, url, campaign, project["id"])
            time.sleep(10)
        db_connection.close()

    def crawl_campaigns(self):
        while True:
            try:
                self.get_campaign()
            except:
                pass

    def creator_url(self, creator_id):
        creator_url = "https://www.kickstarter.com/profile/" + creator_id + "/about"
        return creator_url

    def get_creator(self):
        ksql = ksqlite()
        db_connection = ksql.db_connection(ksql.abs_file_path("../Data/mlks.db"))
        creators = ksql.select_creator_about_is_null(db_connection)
        for creator in creators:
            url = self.creator_url(creator["id"])
            print(url)
            about = urllib.request.urlopen(url).read()
            ksql.update_creator_about(db_connection, about, creator["id"])
            time.sleep(5)
        db_connection.close()


    def crawl_creators(self):
        while True:
            try:
                self.get_creator()
            except:
                pass




kscrape().crawl_campaigns()
# kscrape().crawl_campaigns()
