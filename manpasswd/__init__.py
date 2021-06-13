"""Password Manager using PostgreSQL"""

__version__ = '1.0.0'

from .manpasswd import Manpasswd
from .Menu import Data, Menu, Key
from .Psql import Psql, tabulate_retrieved
from .Key import MasterKey
