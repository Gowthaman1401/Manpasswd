# [Manpasswd](https://test.pypi.org/project/manpasswd)

<!-- [![PyPI](https://img.shields.io/pypi/v/manpasswd)](https://pypi.python.org/pypi/manpasswd)
[![PyPI - License](https://img.shields.io/pypi/l/manpasswd)](https://github.com/Gowthaman1401/ManPasswd/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/manpasswd?color=red)](https://pypi.python.org/pypi/manpasswd) -->

Password manager to store passwords using postgreSQL.

## Installation

`pip install -U manpasswd`

## Usage

```
usage: manpasswd [options]

optional arguments:
  -h, --help          show this help message and exit
  -v, --version       show version number and exit

to access manpasswd:
  --master-key        masterKey to access manpasswd
  --new-masterkey     to set new masterkey

to store and retrieve user data:
  --store             to store data
  --retrieve          to retrieve data
  --modify            to modify data
  -w , --website      name of the website
  -u , --url          url for the website
  -n , --username     username for the website
  -p , --password     password for the user
  -e , --email        email of the user

to modify database:
  --db-uname          username for database
  --db-default-pass   password for default user [postgres]
  --db-name           name to the database
  --db-table          name to the table
  --create-database   to create database
  --delete-database   To delete database
```
## Issues:

If you encounter any problems, please file an [issue](https://github.com/Gowthaman1401/ManPasswd/) along with a detailed description.
