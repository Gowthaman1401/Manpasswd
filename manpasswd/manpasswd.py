from .Menu import Menu
from .Key import MasterKey
from .Psql import Psql
import getpass


class Manpasswd:
    def __init__(self, default_pass=False, new_user=False, old_user=False, new_db=False, old_db=False,
                 new_master_key=False, master_key=False, db_username='manpasswd', db_name='manpasswd',
                 db_table='passman', user_data=None):
        self.db_username = db_username
        self.master_key = master_key
        self.db_name = db_name
        self.db_table = db_table
        self.user_data = user_data
        self.new_master_key = new_master_key
        self.default_pass = default_pass
        self.new_db = new_db
        self.old_db = old_db
        self.new_user = new_user
        self.old_user = old_user

    def menu(self):
        status = Menu(master_key=self.master_key, db_username=self.db_username, db_name=self.db_name,
                      db_table=self.db_table).main_menu()
        return status

    def set_master_key(self):
        if self.validate_key():
            status = MasterKey(master_key=self.master_key, db_username=self.db_username).update_master_key(
                default_pass=self.new_master_key)
            return status

    def validate_key(self):
        status = MasterKey(master_key=self.master_key).validate(db_username=self.db_username, db_name=self.db_name)
        return status

    def insert_data(self):
        if self.validate_key():
            status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                          db_table=self.db_table, user_data=list(self.user_data.values())).insert_data()
            return status

    def retrieve_data(self):
        if self.validate_key():
            status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                          db_table=self.db_table, user_data=self.user_data).retrieve_data()
            return status

    def modify_data(self):
        if self.validate_key():
            status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                          db_table=self.db_table, user_data=self.user_data).modify_data()
            return status

    def create_user(self):
        if not self.default_pass:
            try:
                self.default_pass = getpass.getpass('Please provide the password for default user [postgres] : ')
            except KeyboardInterrupt:
                exit("\n[-] You pressed CTRL-C")
        if self.validate_key():
            status = Psql(db_username='postgres', db_password=self.default_pass, db_name='postgres').create_user(
                db_password=self.new_master_key, db_username=self.new_user)
            return status

    def delete_user(self):
        if not self.default_pass:
            try:
                self.default_pass = getpass.getpass('Please provide the password for default user [postgres] : ')
            except KeyboardInterrupt:
                exit("\n[-] You pressed CTRL-C")
        if self.validate_key():
            status = Psql(db_password=self.default_pass, db_username='postgres', db_name='postgres').delete_user(
                db_username=self.old_user)
            return status

    def create_database(self):
        if not self.default_pass:
            try:
                self.default_pass = getpass.getpass('Please provide the password for default user [postgres] : ')
            except KeyboardInterrupt:
                exit("\n[-] You pressed CTRL-C")
        if self.validate_key():
            status = Psql(db_password=self.default_pass, db_username='postgres',
                          db_name='postgres').create_database(db_name=self.new_db)
            return status

    def delete_database(self):
        if self.validate_key():
            status = Psql(db_password=self.master_key, db_username=self.db_username,
                          db_name=self.db_name).delete_database(db_name=self.old_db)
            return status

    def create_table(self):
        if self.validate_key():
            status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                          db_table=self.db_table).create_table()
            return status
