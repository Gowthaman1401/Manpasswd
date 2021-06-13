"""Password Manager using PostgreSQL"""

__version__ = '2.4.4'

from .manpasswd import Manpasswd
from .Menu import Data, Menu, Key
from .Psql import Psql, tabulate_retrieved
from .Key import MasterKey
