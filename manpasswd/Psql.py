import psycopg2
import collections
import tabulate


def tabulate_retrieved(data):
    password, username, email, website, url = [], [], [], [], []
    for word in data:
        password.append(word[3])
        username.append(word[2])
        email.append(word[4])
        website.append(word[0])
        url.append(word[1])
    filter_data = tabulate.tabulate(
        {'Username': [*username], 'Email': [*email], 'Password': [*password], 'Website': [*website], 'Url': [*url]},
        headers='keys', tablefmt='psql')
    return filter_data


class Psql:
    def __init__(self, db_password=None, db_username='manpasswd', db_name='manpasswd', db_table='passman',
                 user_data=None):
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.db_table = db_table
        self.user_data = user_data

    def connect(self, query):
        try:
            connection = psycopg2.connect(user=self.db_username, password=self.db_password, database=self.db_name,
                                          host='localhost', port='5432')
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(query)
            connection.close()
            return True
        except Exception as e:
            if str(e).strip().title() == 'Role "Manpasswd" Already Exists':
                return str(e).strip().title()
            exit("\n[-] " + str(e).strip().title())

    def create_user(self, db_password, db_username='manpasswd'):
        psql_create_user_query = "CREATE ROLE " + db_username + " PASSWORD '" + db_password + "' LOGIN SUPERUSER CREATEDB CREATEROLE INHERIT;"
        database_status = self.connect(psql_create_user_query)
        return database_status

    def change_user_pass(self, db_password):
        psql_alter_pass_query = "ALTER ROLE " + self.db_username + " WITH PASSWORD '" + db_password + "';"
        database_status = self.connect(psql_alter_pass_query)
        return database_status

    def delete_user(self, db_username):
        psql_delete_user_query = "DROP ROLE " + db_username + ";"
        database_status = self.connect(psql_delete_user_query)
        return database_status

    def create_database(self, db_name='manpasswd'):
        psql_create_db_query = "CREATE DATABASE " + db_name + ";"
        database_status = self.connect(psql_create_db_query)
        return database_status

    def delete_database(self, db_name):
        psql_delete_db_query = "DROP DATABASE " + db_name + ";"
        database_status = self.connect(psql_delete_db_query)
        return database_status

    def create_table(self):
        psql_alter_db_query = "ALTER DATABASE " + self.db_name + " OWNER TO " + self.db_username + ";"
        self.connect(psql_alter_db_query)
        psql_create_table_query = "CREATE TABLE IF NOT EXISTS " + self.db_table + "(Website VARCHAR(50), Website_Url VARCHAR(50), Username VARCHAR(75), Password VARCHAR(100), Email_Id VARCHAR(50));"
        database_status = self.connect(psql_create_table_query)
        return database_status

    def insert_data(self):
        website, url, user, password, email = self.user_data
        psql_insert_query = "INSERT INTO " + self.db_table + " (Website, Website_Url, Username, Password, Email_Id) VALUES ('" + website + "', '" + url + "', '" + user + "', '" + password + "', '" + email + "');"
        database_status = self.connect(psql_insert_query)
        return database_status

    def retrieve_data(self):
        try:
            retrieved_data, none, no, where_key = [], 0, 0, ""
            connection = psycopg2.connect(user=self.db_username, password=self.db_password, database=self.db_name,
                                          host='localhost', port='5432')
            connection.autocommit = True
            cursor = connection.cursor()
            find_empty = []
            select_dict = {'Website': f"Website = '{self.user_data['Website']}'", 'Username': f"Username = '{self.user_data['Username']}'", 'Email_Id': f"Email_Id = '{self.user_data['Email_Id']}'"}
            for key in ['Website', 'Username', 'Email_Id']:
                if self.user_data[key] is not None and self.user_data[key] != '':
                    find_empty.append(key)
                else:
                    if none == 2:
                        return "\n[-] No Input Is Given"
                    none += 1
            for value in find_empty:
                where_key += " AND " + select_dict[value] if no > 0 else select_dict[value]
                no += 1
            psql_select_query = "SELECT * FROM " + self.db_table + " WHERE " + where_key + ";"
            cursor.execute(psql_select_query)
            for result in cursor.fetchall():
                retrieved_data.append(result)
            if len(retrieved_data) == 0:
                return "\n[-] No Data Found"
            elif len(retrieved_data) > 1:
                duplicates = collections.Counter(retrieved_data)
                result = list([data for data in duplicates if duplicates[data] > 0])
                result = tabulate_retrieved(result) if len(result) > 0 else "\n[-] No Data Found"
                return result
            else:
                result = [list(retrieved_data[0])]
                result = tabulate_retrieved(result)
                return result
        except Exception as e:
            exit("\n[-] " + str(e).strip().title())

    def modify_data(self):
        try:
            i = 0
            database_status = False
            for key in ["Website", "Website_Url", "Username", "Password", "Email_Id"]:
                if self.user_data[1][key] != '':
                    psql_update_query = "UPDATE " + self.db_table + " SET " + key + "='" + self.user_data[1][
                        key] + "' WHERE Website='" + self.user_data[0][0] + "' AND Website_Url='" + self.user_data[0][
                                            1] + "' AND Username='" + self.user_data[0][2] + "' AND Password='" + \
                                        self.user_data[0][3] + "' AND Email_Id='" + self.user_data[0][4] + "';"
                    self.user_data[0][i] = self.user_data[1][key]
                    database_status = self.connect(psql_update_query)
                i += 1
            return database_status
        except (Exception, psycopg2.Error) as e:
            exit("\n[-] " + str(e).strip().title())
