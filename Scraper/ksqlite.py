import sqlite3
from sqlite3 import Error
import os.path
import csv
import pandas as pd
from pandas import DataFrame

class ksqlite:

    def __init__(self, rel_file_path):
        self._db_connection = self._connect_to(self._abs_file_path(rel_file_path))
        self._db_cur = self._db_connection.cursor()

    def __del__(self):
        self._db_connection.close()

    def _connect_to(self, db_file_path):
        try:
            conn = sqlite3.connect(db_file_path)
            conn.text_factory = str
            return conn
        except Error as e:
            print(e)
        return None

    def _abs_file_path(self, rel_file_path):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, rel_file_path)
        return path

    def csv_to_sqlite(self, csv_path, table_name):
        self._db_connection.text_factory = str
        df = pd.read_csv(self.abs_file_path(csv_path))
        df.to_sql(table_name, self._db_connection, if_exists='replace', index=False)
        return df




    def update_field(self, table_name, column_name, column_value, pk, pk_value):
        self._db_cur.execute("UPDATE {0} SET {1} = ? WHERE {2} = ?".format(table_name, column_name, pk), [column_value, pk_value])
        self._db_connection.commit()

    def update_creator_id(self, db_connection, creator_id, project_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Projects SET creator_id = ? WHERE project_id = ?', [creator_id, project_id])
        db_connection.commit()
        cursor.close()


    def update_campaign(self, db_connection, campaign, project_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Projects SET campaign = ? WHERE project_id = ?', [campaign, project_id])
        db_connection.commit()
        cursor.close()

    def update_creator_about(self, db_connection, about, creator_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Creators SET about = ? WHERE creator_id = ?', [about, creator_id])
        db_connection.commit()
        cursor.close()

    def insert_creator(self, db_conection, creator_id):
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO Creators Values (?, NULL)", [creator_id])
        db_connection.commit()
        cursor.close()



    def populate_creators_table(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT creator_id FROM Projects WHERE creator_id IS NOT NULL')
        creator_ids = cursor.fetchall()
        count = 0
        for creator_id in creator_ids:
            try:
                cursor.execute("INSERT INTO Creators VALUES (?, NULL)", [creator_id[0]])
                count = count + 1
                print(count)
            except:
                pass
            db_connection.commit()
        cursor.close()

    def select_creator_is_null(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT project_id, campaign FROM Projects WHERE campaign IS NOT NULL AND creator_id IS NULL LIMIT 100')
        rows = cursor.fetchall()
        cursor.close()
        projects = []
        for row in rows:
            projects.append({"id": row[0], "campaign": row[1]})
        return projects

####################################################################################################################
## RANDOM SELECTS ## RANDOM SELECTS ## RANDOM SELECTS
####################################################################################################################

    def select_creator_ids_where_about_is_null(self):
        rows = self._db_cur.execute('SELECT creator_id FROM Creators WHERE about IS NULL').fetchall()
        creators = []
        for row in rows:
            creators.append(row[0])
        return creators

    def select_creator_ids_where_backers_is_null(self):
        rows = self._db_cur.execute('SELECT creator_id FROM Creators WHERE backers IS NULL').fetchall()
        creators = []
        for row in rows:
            creators.append(row[0])
        return creators

    def select_all_campaigns(self):
        rows = self._db_cur.execute('SELECT campaign FROM Projects').fetchall()
        campaigns = []
        for row in rows:
            campaigns.append({"campaign": row[0]})
        return campaigns

    def select_all_project_ids(self):
        rows = self._db_cur.execute('SELECT project_id FROM Projects').fetchall()
        project_ids = []
        for row in rows:
            project_ids.append({"project_id": row[0]})
        return project_ids

    def select_all_creator_ids(self):
        rows = self._db_cur.execute('SELECT creator_id FROM Projects').fetchall()
        creator_ids = []
        for row in rows:
            creator_ids.append(row[0])
        return creator_ids

    def select_all_creator_id_about_backers(self):
        rows = self._db_cur.execute('SELECT creator_id, about, backers FROM Creators WHERE about IS NOT NULL').fetchall()
        creators = []
        for row in rows:
            creators.append({"creator_id": row[0], "about": row[1], "backers": row[1]})
        return creators

    def select_all_project_ids_and_campaigns(self):
        rows = self._db_cur.execute('SELECT project_id, campaign FROM Projects').fetchall()
        projects = []
        for row in rows:
            projects.append({"project_id": row[0], "campaign": row[1]})
        return projects

    def select_all_creator_about(self):
            rows = self._db_cur.execute("SELECT creator_id, about FROM Creators").fetchall()
            # rows = self._db_cur.execute("SELECT creator_id, about FROM Creators WHERE creator_id = '1983840459'").fetchall()
            creators = []
            for row in rows:
                creators.append({"creator_id": row[0], "about": row[1]})
            return creators

    def select_all_creator_social(self):
            rows = self._db_cur.execute("SELECT facebook, twitter, youtube FROM Creators LIMIT 1000").fetchall()
            creators = []
            for row in rows:
                creators.append({"facebook": row[0], "twitter": row[1], "youtube": row[2]})
            return creators


####################################################################################################################
## DATABASE STRUCTURE ## DATABASE STRUCTURE ## DATABASE STRUCTURE
####################################################################################################################

    def create_table(self):
        self._db_cur.execute('CREATE TABLE Creators (creator_id TEXT PRIMARY KEY)')
        # self._db_cur.execute('CREATE TABLE Projects (project_id TEXT PRIMARY KEY)')
        # self._db_cur.execute('CREATE TABLE Projects (project_id TEXT PRIMARY KEY, keywords TEXT, campaign TEXT)')

    def delete_projects_where_campaign_is_null(self):
        self._db_cur.execute("DELETE FROM Projects WHERE campaign IS NULL")
        self._db_connection.commit()

    def select_important_data(self):
        rows = self._db_cur.execute('SELECT project_id, keywords, campaign FROM Projects').fetchall()
        projects = []
        for row in rows:
            projects.append({"project_id": row[0], "keywords": row[1], "campaign": row[2]})
        return projects

    def insert_important_data(self, project_id, keywords, campaign):
        self._db_cur.execute("""INSERT INTO Projects VALUES (?, ?, ?)""", [project_id, keywords, campaign])
        self._db_connection.commit()

    def count_projects(self):
        rows = self._db_cur.execute('SELECT project_id FROM Projects').fetchall()
        print(len(rows))

    def add_column(self, table_name, column_name, column_type):
        self._db_cur.execute("ALTER TABLE {0} ADD {1} {2};".format(table_name, column_name, column_type))

    def add_columns(self, table_name, column_names, column_type):
        for column_name in column_names:
            self.add_column(table_name, column_name, column_type)

    def insert_project_id(self, proj_id):
        #113 NULL VALUES
        self._db_cur.execute("""INSERT INTO Projects VALUES (?, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                        NUll, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)""", [proj_id])
        self._db_connection.commit()

    def insert_creator_id(self, creator_id):
        self._db_cur.execute("""INSERT INTO Creators VALUES (?)""", [creator_id])
        self._db_connection.commit()


# # ==============================================
# # Check if Social Parse is Working
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# backed = ksq_parsed.select_all_creator_backed()
# for back in backed:
#     print(back)

# # ==============================================
# # Add Backed Columns to mlks_parsed creators
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# column_names = [
#     'biograpy'
# ]
# ksq_parsed.add_columns("Creators", column_names, "TEXT")


# # ==============================================
# # Add Social Columns to mlks_parsed creators
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# column_names = [
#     'facebook',
#     'twitter',
#     'youtube'
# ]
# ksq_parsed.add_columns("Creators", column_names, "TEXT")

# # ==============================================
# # Add Creators Table to mlks_parsed
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# creator_ids = ksq_parsed.select_all_creator_ids()
# creator_ids = list(set(creator_ids))
# ksq_parsed.create_table()
# count = len(creator_ids)
# for creator_id in creator_ids:
#     ksq_parsed.insert_creator_id(creator_id)
#     count = count - 1
#     print(count)


# # ==============================================
# # Transfer Scraped Creator Values from mlks to mlks_scraped
# # ==============================================
# ksq_mlks = ksqlite("../Data/mlks.db")
# creators = ksq_mlks.select_all_creator_id_about_backers()
# ksq_scraped = ksqlite("../Data/mlks_scraped.db")
# # ksq_scraped.add_columns("Creators", ["about", "backers"], "TEXT")
#
# count = 0
# for creator in creators:
#     ksq_scraped.update_field("Creators", "about", creator["about"], "creator_id", creator["creator_id"])
#     ksq_scraped.update_field("Creators", "backers", creator["backers"], "creator_id", creator["creator_id"])
#     count = count + 1
#     print(count)

# # ==============================================
# # Add Creators Table to mlks_scraped
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# creator_ids = ksq_parsed.select_all_creator_ids()
# creator_ids = list(set(creator_ids))
# print(len(creator_ids))
#
# ksq_scraped = ksqlite("../Data/mlks_scraped.db")
# # ksq_scraped.create_table()
# count = 0
# for creator_id in creator_ids:
#     try:
#         ksq_scraped.insert_creator_id(creator_id)
#     except:
#         pass
#     count = count + 1
#     print(count)

# # ==============================================
# # Transfer Project IDs from Scraped to Parsed Database
# # ==============================================
# ksq_scraped = ksqlite("../Data/mlks_scraped.db")
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# project_ids = ksq_scraped.select_all_project_ids()
# count = 0
# for project_id in project_ids:
#     ksq_parsed.insert_project_id(project_id["project_id"])
#     count = count + 1
#     print(count)

# # ==============================================
# # Add All Columns to mlks_parsed
# # ==============================================
# ksq_parsed = ksqlite("../Data/mlks_parsed.db")
# ksq_parsed.create_table()
# column_names = [
#     'backers_count',
#     'blurb',
#     'canceled_at',
#     'category_color',
#     'category_id',
#     'category_name',
#     'category_parent_id',
#     'category_position',
#     'category_slug',
#     'category_urls_web_discover',
#     'comments_count',
#     'converted_pledged_amount',
#     'country',
#     'created_at',
#     'creator_avatar_medium',
#     'creator_avatar_small',
#     'creator_avatar_thumb',
#     'creator_chosen_currency',
#     'creator_id',
#     'creator_is_registered',
#     'creator_name',
#     'creator_slug',
#     'creator_urls_api_user',
#     'creator_urls_web_user',
#     'currency',
#     'currency_symbol',
#     'currency_trailing_code',
#     'current_currency',
#     'deadline',
#     'disable_communication',
#     'failed_at',
#     'fx_rate',
#     'goal',
#     'id',
#     'is_starrable',
#     'items',
#     'launched_at',
#     'livestreams',
#     'location_country',
#     'location_displayable_name',
#     'location_id',
#     'location_is_root',
#     'location_localized_name',
#     'location_name',
#     'location_short_name',
#     'location_slug',
#     'location_state',
#     'location_type',
#     'location_urls_api_nearby_projects',
#     'location_urls_web_discover',
#     'location_urls_web_location',
#     'name',
#     'photo_1024x576',
#     'photo_1536x864',
#     'photo_ed',
#     'photo_full',
#     'photo_key',
#     'photo_little',
#     'photo_med',
#     'photo_small',
#     'photo_thumb',
#     'pledged',
#     'potd_at',
#     'profile_background_color',
#     'profile_background_image_attributes_id',
#     'profile_background_image_attributes_image_urls_baseball_card',
#     'profile_background_image_attributes_image_urls_default',
#     'profile_background_image_opacity',
#     'profile_blurb',
#     'profile_feature_image_attributes_id',
#     'profile_feature_image_attributes_image_urls_baseball_card',
#     'profile_feature_image_attributes_image_urls_default',
#     'profile_id',
#     'profile_link_background_color',
#     'profile_link_text',
#     'profile_link_text_color',
#     'profile_link_url',
#     'profile_name',
#     'profile_project_id',
#     'profile_should_show_feature_image_section',
#     'profile_show_feature_image',
#     'profile_state',
#     'profile_state_changed_at',
#     'profile_text_color',
#     'rewards',
#     'slug',
#     'spotlight',
#     'staff_pick',
#     'state',
#     'state_changed_at',
#     'static_usd_rate',
#     'successful_at',
#     'suspended_at',
#     'updated_at',
#     'updates_count',
#     'urls_api_comments',
#     'urls_api_project',
#     'urls_api_updates',
#     'urls_web_project',
#     'urls_web_project_short',
#     'urls_web_rewards',
#     'urls_web_updates',
#     'usd_pledged',
#     'usd_type',
#     'video',
#     'video_base',
#     'video_frame',
#     'video_height',
#     'video_high',
#     'video_hls',
#     'video_id',
#     'video_status',
#     'video_width',
#     "full_description"
# ]
# ksq_parsed.add_columns("Projects", column_names, "TEXT")

# # ==============================================
# # Transfer Raw Database to Scraped Database
# # ==============================================
# ksq_raw = ksqlite("../Data/mlks.db")
# ksq_scraped = ksqlite("../Data/mlks_scraped.db")
# ksq_scraped.create_table()
# projects = ksq_raw.select_important_data()
# count = 0
# for project in projects:
#     ksq_scraped.insert_important_data(project["project_id"], project["keywords"], project["campaign"])
#     count = count + 1
#     print(count)


# ==============================================
# Transfer Courneys Projects to Main databae
# ==============================================
# ksq_court = ksqlite("../Data/projects_courtney.db")
# ksq_brant = ksqlite("../Data/mlks.db")
# projects = ksq_court.select_projects_courtney()
# count = 0
# for i, project in projects.iterrows():
#     ksq_brant.update_field("Projects", "campaign", str(project.campaign, 'utf-8'), "project_id", project.project_id)
#     count = count + 1
#     print(count)

# def create_db_for_courtney(self):
#     db_file_path = self.abs_file_path("../Data/mlks.db")
#     db_connection_brant = self.db_connection(db_file_path)
#     cursor = db_connection_brant.cursor()
#     # cursor.execute('SELECT * FROM Projects WHERE campaign IS NULL LIMIT 10')
#     cursor.execute('SELECT project_id, keywords FROM Projects LIMIT 10')
#     rows = cursor.fetchall()
#     df = pd.DataFrame(data = rows, columns = ["project_id", "keywords"])
#     print(df)
#     db_connection_brant.close()
#
#     db_file_path = self.abs_file_path("../Data/courtney_projects.db")
#     db_connection_courtney = self.db_connection(db_file_path)
#     df.to_sql(df, db_connection_courtney, if_exists='replace', index=False)
#     db_connection_courtney.close()


#CREATe creators table from projects
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks.db")
# db_connection = ksq.db_connection(db_file_path)
# ksq.populate_creators_table(db_connection)
# db_connection.close()

# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks.db")
# db_connection = ksq.db_connection(db_file_path)
# ksq.select_campaign_is_null(db_connection)
# db_connection.close()


# #ADD NEW COLUMN
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/projects_courtney.db")
# db_connection = ksq.db_connection(db_file_path)
# ksq.add_column(db_connection, "Projects", "campaign", "TEXT")
# db_connection.close()

# #ADD NEW TABLE
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks.db")
# db_connection = ksq.db_connection(db_file_path)
# ksq.create_table(db_connection)
# db_connection.close()




# #CONVERT CSV TO SQLite
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/projects_courtney.db")
# db_connection = ksq.db_connection(db_file_path)
# df = ksq.csv_to_sqlite("../Data/train_courtney.csv", db_connection, "Projects")

# ADD NEW COLUMNS
# cur.execute("ALTER TABLE Projects ADD 'url' 'TEXT';")
# cur.execute("ALTER TABLE Projects ADD 'campaign' 'TEXT';")
