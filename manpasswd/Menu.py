import getpass
from .Psql import Psql
from .Key import MasterKey


class Data:
    def __init__(self, db_username, db_name, db_table, master_key, user_data=None):
        self.user_data = user_data
        self.master_key = master_key
        self.db_username = db_username
        self.db_name = db_name
        self.db_table = db_table

    def store(self):
        status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                      db_table=self.db_table, user_data=list(self.user_data.values())).insert_data()
        print('-' * 30 + '\n')
        return status

    def retrieve(self):
        retrieved_data = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                              db_table=self.db_table, user_data=self.user_data).retrieve_data()
        if retrieved_data == 'No Data Found' or retrieved_data == "No Input Is Given":
            exit('-' * 30 + '\n' + retrieved_data)
        return retrieved_data

    def modify(self):
        status = Psql(db_password=self.master_key, db_username=self.db_username, db_name=self.db_name,
                      db_table=self.db_table, user_data=self.user_data).modify_data()
        print('-' * 30 + '\n')
        return status


class Key:
    def __init__(self, master_key, db_username, db_name):
        self.master_key = master_key
        self.db_username = db_username
        self.db_name = db_name

    def validate(self):
        master_key_status = MasterKey(master_key=self.master_key).validate(db_username=self.db_username,
                                                                           db_name=self.db_name)
        return master_key_status

    def set(self):
        default_pass = getpass.getpass('Please provide the password for default user [postgres] : ')
        if not self.master_key:
            self.master_key = getpass.getpass('Please set the master key to your vault : ')
        master_key_status = MasterKey(master_key=self.master_key, db_username=self.db_username).set_master_key(
            default_pass, db_name=self.db_name)
        if master_key_status:
            exit("\n[+] Vault created... You can access vault using CLI")


def ques_prompt(input_needed):
    input_dict = {'Website': None, 'Website_Url': None, 'Username': None, 'Password': None, 'Email_Id': None}
    prompt = {'Website': 'Enter the website name : ',
              'Website_Url': 'Enter the website url : ',
              'Username': 'Enter the user name : ',
              'Password': 'Enter the password : ',
              'Email_Id': 'Enter the email : '}
    for key in input_needed:
        input_dict[key] = input(prompt[key]) if key != 'Password' else getpass.getpass(prompt[key])
    return input_dict


class Menu:
    def __init__(self, master_key=False, db_username='manpasswd', db_name='manpasswd', db_table='passman'):
        self.master_key = master_key
        self.db_username = db_username
        self.db_name = db_name
        self.db_table = db_table

    def main_menu(self):
        try:
            Key(self.master_key, self.db_username, self.db_name).set()
            # if not self.master_key:
            # self.master_key = getpass.getpass('Please provide the master key to access manpasswd : ')
            # Key(self.master_key, self.db_username, self.db_name).validate()
            # Key('my_gen_passwd_rand', self.db_username, self.db_name).set()
            print('\n' + ('-' * 11) + 'MANPASSWD' + ('-' * 11))
            print("1.Create and Store new data\n2.Retrieve stored data\n3.Modify existing data\n4.Exit\n" + '-' * 30)
            choice = input("Enter your Choice : ")
            if choice == '1':
                print("Press ENTER if you don't have Required Data\n" + '-' * 30)
                userdata = ques_prompt(['Website', 'Website_Url', 'Username', 'Password', 'Email_Id'])
                result = Data(master_key=self.master_key, user_data=userdata, db_username=self.db_username,
                              db_name=self.db_name, db_table=self.db_table).store()
                if result:
                    return "\n[+] Data is stored"
            elif choice == '2':
                print("Press ENTER if you don't have Required Data\n" + '-' * 30)
                userdata = ques_prompt(['Website', 'Username', 'Email_Id'])
                return Data(master_key=self.master_key, user_data=userdata, db_username=self.db_username,
                            db_name=self.db_name, db_table=self.db_table).retrieve()
            elif choice == '3':
                print('-' * 30 + '\nEnter the old data')
                old_data = ques_prompt(['Website', 'Website_Url', 'Username', 'Password', 'Email_Id'])
                print('-' * 30 + '\nEnter the new data to replace the old data')
                new_data = ques_prompt(['Website', 'Website_Url', 'Username', 'Password', 'Email_Id'])
                userdata = [list(old_data.values()), new_data]
                result = Data(master_key=self.master_key, user_data=userdata, db_username=self.db_username,
                              db_name=self.db_name, db_table=self.db_table).modify()
                if result:
                    return "\n[+] Data is modified"
            elif choice == '4':
                return exit()
            else:
                return exit('Invalid choice')
        except KeyboardInterrupt:
            exit('\n[-] You pressed CTRL-C.')
