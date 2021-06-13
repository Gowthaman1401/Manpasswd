import argparse
import getpass
from . import manpasswd


def get_argument():
    parser = argparse.ArgumentParser(usage="manpasswd [options]", )
    parser.add_argument('-v', '--version', action='version', help='show version number and exit', version="2.4.4")
    group = parser.add_argument_group("to access manpasswd")
    group.add_argument("--master-key", default=False, metavar='', help="masterKey to access manpasswd")
    group.add_argument("--new-masterkey", default=False, metavar='', help="to set new masterkey")
    parser.add_argument_group(group)
    group = parser.add_argument_group("to store and retrieve user data")
    group.add_argument("--store", default=False, action='store_true', help="to store data")
    group.add_argument("--retrieve", default=False, action='store_true', help="to retrieve data")
    group.add_argument("--modify", default=False, action='store_true', help="to modify data")
    group.add_argument("-w", "--website", default='', metavar='', help="name of the website")
    group.add_argument("-u", "--url", default='', metavar='', help="url for the website")
    group.add_argument("-n", "--username", default='', metavar='', help="username for the website")
    group.add_argument("-p", "--password", default='', metavar='', help="password for the user")
    group.add_argument("-e", "--email", default='', metavar='', help="email of the user")
    parser.add_argument_group(group)
    group = parser.add_argument_group("to modify database")
    group.add_argument("--db-uname", metavar='', default='manpasswd', help="username for database")
    group.add_argument("--db-default-pass", default=False, metavar='', help="password for default user [postgres]")
    group.add_argument("--db-name", metavar='', default='manpasswd', help="name to the database")
    group.add_argument("--db-table", metavar='', default='passman', help="name to the table")
    group.add_argument("--create-user", default=False, metavar='', help=argparse.SUPPRESS)
    group.add_argument("--delete-user", default=False, metavar='', help=argparse.SUPPRESS)
    group.add_argument("--create-database", default=False, metavar='', help="to create database")
    group.add_argument("--delete-database", default=False, metavar='', help="To delete database")
    group.add_argument("--create-table", metavar='', default=False, help=argparse.SUPPRESS)
    group.add_argument("--menu", default=False, action='store_true', help=argparse.SUPPRESS)
    parser.add_argument_group(group)
    options = parser.parse_args()
    if not options.new_masterkey and not options.store and not options.retrieve and not options.modify and not options.create_table and not options.create_database and not options.delete_database and not options.db_default_pass and not options.create_user and not options.delete_user:
        options.menu = True
    if options.store:
        options.store = {'Website': options.website, 'Website_Url': options.url, 'Username': options.username,
                         'Password': options.password, 'Email_Id': options.email}
    elif options.retrieve:
        options.retrieve = {'Website': options.website, 'Website_Url': options.url, 'Username': options.username,
                            'Password': options.password, 'Email_Id': options.email}
    if options.modify:
        if not options.website or not options.username or not options.url or not options.password or not options.email:
            exit('\n[-] You have to provide all the data [website, url, username, password, email]')
        options.modify = [list({'Website': (options.website + ",").split(',')[0].strip(),
                                'Website_Url': (options.url + ",").split(',')[0].strip(),
                                'Username': (options.username + ",").split(',')[0].strip(),
                                'Password': (options.password + ",").split(',')[0].strip(),
                                'Email_Id': (options.email + ",").split(',')[0].strip()}.values()),
                          {'Website': (options.website + ",").split(',')[1].strip(),
                           'Website_Url': (options.url + ",").split(',')[1].strip(),
                           'Username': (options.username + ",").split(',')[1].strip(),
                           'Password': (options.password + ",").split(',')[1].strip(),
                           'Email_Id': (options.email + ",").split(',')[1].strip()}]
    return options


def man_pass(master_key=False, new_master_key=False, store=False, retrieve=False, modify=False, db_username='manpasswd',
             db_name='manpasswd', db_table='passman', cre_table=False, cre_db=False, del_db=False,
             db_default_pass=False, cre_user=False, del_user=False, userdata=None):
    if cre_table:
        db_table = cre_table
    if store or retrieve or modify:
        if store:
            userdata = store
        elif retrieve:
            userdata = retrieve
        elif modify:
            userdata = modify
        man_passwd = manpasswd.Manpasswd(default_pass=db_default_pass, new_db=cre_db, old_user=del_user,
                                         new_user=cre_user, old_db=del_db, new_master_key=new_master_key,
                                         master_key=master_key, db_username=db_username, db_name=db_name,
                                         db_table=db_table, user_data=userdata)
    else:
        man_passwd = manpasswd.Manpasswd(default_pass=db_default_pass, new_db=cre_db, old_user=del_user,
                                         new_user=cre_user, old_db=del_db, new_master_key=new_master_key,
                                         master_key=master_key, db_username=db_username, db_name=db_name,
                                         db_table=db_table)
    if cre_user:
        result = man_passwd.create_user()
        if result:
            return "\n[+] User Created"
    elif new_master_key:
        result = man_passwd.set_master_key()
        if result:
            return "\n[+] Master Key is set"
    elif store:
        result = man_passwd.insert_data()
        if result:
            return "\n[+] Data is stored"
    elif retrieve:
        result = man_passwd.retrieve_data()
        return result
    elif modify:
        result = man_passwd.modify_data()
        if result:
            return "\n[+] Data is modified"
    elif cre_db:
        result = man_passwd.create_database()
        if result:
            return "\n[+] Database Created"
    elif del_db:
        result = man_passwd.delete_database()
        if result:
            return "\n[+] Database deleted "
    elif db_table:
        result = man_passwd.create_table()
        if result:
            return "\n[+] New Table Created"


def main():
    options = get_argument()
    if options.menu:
        result = manpasswd.Manpasswd(master_key=options.master_key, db_username=options.db_uname,
                                     db_name=options.db_name, db_table=options.db_table).menu()
        if not result:
            print(result)
    else:
        if not options.master_key:
            try:
                options.master_key = getpass.getpass('Please provide the master key to access manpasswd : ')
            except KeyboardInterrupt:
                exit('\n[-] You pressed CTRL-C, You have to provide MasterKey to access Manpasswd.')
        result = man_pass(options.master_key, options.new_masterkey, options.store, options.retrieve, options.modify,
                          options.db_uname, options.db_name, options.db_table, options.create_table,
                          options.create_database, options.delete_database, options.db_default_pass,
                          options.create_user, options.delete_user)
        if not result:
            print(result)


if __name__ == "__main__":
    main()
