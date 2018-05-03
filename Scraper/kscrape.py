
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

    def get_creator_backers(self):

        def url_creator_backers(creator_id):
            creator_url = "https://www.kickstarter.com/profile/" + creator_id
            return creator_url

        ksql_scraped = ksqlite("../Data/mlks_scraped.db")
        creator_ids = ksql_scraped.select_creator_ids_where_backers_is_null()
        count = len(creator_ids)
        for creator_id in creator_ids:
            url = url_creator_backers(creator_id)
            print(url)
            count = count -1
            print(count)
            backers = urllib.request.urlopen(url).read()
            ksql_scraped.update_field("Creators", "backers", backers, "creator_id", creator_id)
            time.sleep(1.5)

    def get_campaign(self):
        ksql = ksqlite()
        db_connection = ksql.db_connection(ksql.abs_file_path("../Data/projects_courtney.db"))
        projects = ksql.select_campaign_is_null(db_connection)
        print(projects)
        for project in projects:
            url = self.campaign_url(project["id"], project["keywords"])
            print(url) #visual cl progress
            campaign = urllib.request.urlopen(url).read()
            ksql.update_campaign(db_connection, campaign, project["id"])
            time.sleep(10)
        db_connection.close()

    def crawl_campaigns(self):
        while True:
            try:
                self.get_campaign()
            except:
                pass

    def get_creator(self):

        def url_creator_about(creator_id):
            creator_url = "https://www.kickstarter.com/profile/" + creator_id + "/about"
            return creator_url

        ksql_scraped = ksqlite("../Data/mlks_scraped.db")
        creator_ids = ksql_scraped.select_creator_ids_where_about_is_null()
        count = len(creator_ids)
        for creator_id in creator_ids:
            url = url_creator_about(creator_id)
            print(url)
            count = count -1
            print(count)
            about = urllib.request.urlopen(url).read()
            ksql_scraped.update_field("Creators", "about", about, "creator_id", creator_id)
            time.sleep(1.5)

    def crawl_creators(self):
        while True:
            try:
                self.get_creator()
            except:
                pass

    def crawl_creator_backers(self):
        while True:
            try:
                self.get_creator_backers()
            except:
                pass


# =============================================================================
# =============================================================================
kscrape().crawl_creator_backers()
