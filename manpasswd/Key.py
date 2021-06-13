import genpasswd
import subprocess
import psycopg2
import os
from .Psql import Psql


def generate_key():
    gen_pass = genpasswd.Password(only='uppercase,numbers', length=25, separator_length=5)
    secret_key = gen_pass.generate()
    return secret_key


def rewrite(changes):
    file = open(changes[0], 'r')
    read_file = file.readlines()
    file.close()
    changes_dict = {75: "\t\t\t# Key(self.master_key, self.db_username, self.db_name).set()\n",
                    76: "\t\t\tif not self.master_key:\n",
                    77: "\t\t\t\tself.master_key = getpass.getpass('Please provide the master key to access manpasswd : ')\n",
                    78: "\t\t\tKey(self.master_key, self.db_username, self.db_name).validate()\n",
                    79: "\t\t\tKey('my_gen_passwd_rand', self.db_username, self.db_name).set()\n"}
    for line in changes[1]:
        read_file[line] = changes_dict[line]
        old_key = open(changes[0], 'w')
        old_key.writelines([*read_file])
        old_key.close()


class MasterKey:
    def __init__(self, master_key=False, db_username='manpasswd'):
        self.master_key = master_key
        self.db_username = db_username
        if not self.master_key:
            self.master_key = generate_key()

    def set_master_key(self, default_pass=False, db_name='manpasswd'):
        if self.master_key == 'my_gen_passwd' or self.master_key == 'my_gen_passwd_rand':
            self.master_key = generate_key()
            subprocess.check_call(['echo', self.master_key, '|clip'], shell=True)
        file = [f"{os.path.dirname(os.path.realpath(__file__))}/Menu.py", [75, 76, 77, 78]]
        if self.master_key == 'my_gen_passwd_rand':
            file[1].append(79)
        error = Psql(db_username='postgres', db_password=default_pass, db_name='postgres').create_user(
            db_password=self.master_key, db_username=self.db_username)
        if error == 'Role "Manpasswd" Already Exists':
            if input(
                    "[-] " + error + '\n\nDo you want to create new vault or use existing vault (N/E) ? ').capitalize() == 'N':
                self.db_username = input("[-] " + error + '\n\nEnter new username to your vault : ')
                db_name = input('Enter a name to your vault : ')
                Psql(db_username='postgres', db_password=default_pass, db_name='postgres').create_user(
                    db_password=self.master_key, db_username=self.db_username)
                Psql(db_username='postgres', db_password=default_pass, db_name='postgres').create_database(
                    db_name=db_name)
                Psql(db_password=self.master_key, db_username=self.db_username, db_name=db_name).create_table()
            else:
                rewrite(file)
                exit("[+] You can access existing vault using CLI")
        else:
            Psql(db_username='postgres', db_password=default_pass, db_name='postgres').create_database(
                db_name='manpasswd')
            Psql(db_password=self.master_key, db_username=self.db_username, db_name=db_name).create_table()
        rewrite(file)
        return True

    def update_master_key(self, default_pass):
        status = Psql(db_password=self.master_key, db_username=self.db_username).change_user_pass(
            db_password=default_pass)
        return status

    def validate(self, db_username='manpasswd', db_name='manpasswd'):
        try:
            connection = psycopg2.connect(user=db_username, password=self.master_key, database=db_name,
                                          host='localhost', port='5432')
            connection.autocommit = True
            connection.close()
            return True
        except (Exception, psycopg2.Error):
            # exit("\n[-] " + str(e).strip().title())
            exit('\n[-] Master Key you entered is Wrong...\n[-] If you forget MasterKey, You cannot access Manpasswd')
