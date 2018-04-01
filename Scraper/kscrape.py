
from ksqlite import ksqlite
import urllib2
import time
import numpy as np

class kscrape:

    def campaign_url(self, project_id, project_keywords):
        project_id = project_id[4:]
        campaign_url = "https://www.kickstarter.com/projects/" + project_id + "/" + project_keywords
        return  campaign_url

    def get_campaign(self):
        ksql = ksqlite()
        db_connection = ksql.db_connection(ksql.abs_file_path("../Data/mlks.db"))
        project = ksql.select_campaign_is_null(db_connection)
        url = self.campaign_url(project["id"], project["keywords"])
        print url #visual cl progress
        campaign = urllib2.urlopen(url).read()
        ksql.update_campaign(db_connection, url, campaign, project["id"])
        db_connection.close()
        return campaign

    def crawl_campaigns(self):
        while True:
            self.get_campaign()
            sleep = np.random.normal(15,2,1)
            time.sleep(sleep)

kscrape().crawl_campaigns()
