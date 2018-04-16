import sqlite3
from sqlite3 import Error
import os.path
import csv
import pandas as pd

class ksqlite:

    def db_connection(self, db_file_path):
        try:
            conn = sqlite3.connect(db_file_path)
            conn.text_factory = str
            return conn
        except Error as e:
            print(e)
        return None

    def abs_file_path(self, rel_file_path):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, rel_file_path)
        return path

    def csv_to_sqlite(self, csv_path, db_connection, table_name):
        db_connection.text_factory = str
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, db_connection, if_exists='replace', index=False)
        db_connection.close()
        return df

    # def select_campaign_is_null(self, db_connection):
        # cursor = db_connection.cursor()
        # cursor.execute('SELECT project_id, keywords FROM Projects WHERE campaign IS NULL or campaign = 0 LIMIT 1')
        # data = cursor.fetchall()[0]
        # print data
        # cursor.close()
        # project = {"id": data[0], "keywords": data[1]}
        # return project

    def select_campaign_is_null(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT project_id, keywords FROM Projects WHERE campaign IS NULL or campaign = 0 LIMIT 100')
        rows = cursor.fetchall()
        cursor.close()
        projects = []
        for row in rows:
            projects.append({"id": row[0], "keywords": row[1]})
        return projects



    # def select_campaign_is_null(self, db_connection):
    #     cursor = db_connection.cursor()
    #     cursor.execute('SELECT project_id, keywords FROM Projects WHERE campaign IS NULL or campaign = 0 LIMIT 1')
    #     rows = cursor.fetchall()
    #     print rows
    #     projects = []
    #     for row in fow:
    #          projects.append({"id": row[0], "keywords": row[1]})
    #     cursor.close()
    #     return projects


    def select_creator_is_null(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT project_id, campaign FROM Projects WHERE campaign IS NOT NULL AND creator_id IS NULL LIMIT 100')
        rows = cursor.fetchall()
        cursor.close()
        projects = []
        for row in rows:
            projects.append({"id": row[0], "campaign": row[1]})
        return projects

    def select_creator_about_is_null(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('SELECT creator_id FROM Creators WHERE about IS NULL LIMIT 1')
        rows = cursor.fetchall()
        cursor.close()
        creators = []
        for row in rows:
            creators.append({"id": row[0]})
        return creators


    def update_creator_id(self, db_connection, creator_id, project_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Projects SET creator_id = ? WHERE project_id = ?', [creator_id, project_id])
        db_connection.commit()
        cursor.close()


    def update_campaign(self, db_connection, url, campaign, project_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Projects SET url = ?, campaign = ? WHERE project_id = ?', [url, campaign, project_id])
        db_connection.commit()
        cursor.close()

    def update_creator_about(self, db_connection, about, creator_id):
        cursor = db_connection.cursor()
        cursor.execute('UPDATE Creators SET about = ? WHERE creator_id = ?', [about, creator_id])
        db_connection.commit()
        cursor.close()

    def insert_project(self, db_connection, proj_id):
        cursor = db_connection.cursor()
        cursor.execute("""INSERT INTO Projects VALUES (?, NULL, NULL, NULL,
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
        db_connection.commit()
        cursor.close()

    def insert_creator(self, db_conection, creator_id):
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO Creators Values (?, NULL)", [creator_id])
        db_connection.commit()
        cursor.close()

    def update_field(self, db_connection, project_id, column_name, value):
        cursor = db_connection.cursor()
        cursor.execute("UPDATE Projects SET {0} = ? WHERE project_id = ?".format(column_name), [value, project_id])
        db_connection.commit()
        cursor.close()

    def add_column(self, db_connection, table_name, column_name, column_type):
        cursor = db_connection.cursor()
        # cursor.execute("ALTER TABLE Projects ADD campaign TEXT")
        # cursor.close()
        try:
            cursor.execute("ALTER TABLE {0} ADD {1} {2};".format(table_name, column_name, column_type))
        except:
            pass
        cursor.close()

    def create_table(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute('CREATE TABLE Creators (creator_id TEXT PRIMARY KEY, about TEXT)')
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





#TEST SELECT CREATOR ABOUT IS NULL
# ksq = ksqlite()
# db_file_path = ksq.abs_file_path("../Data/mlks.db")
# db_connection = ksq.db_connection(db_file_path)
# print ksq.select_creator_about_is_null(db_connection)
# db_connection.close()


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
