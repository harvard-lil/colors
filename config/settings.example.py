import os
from config.settings_base import *

SQLALCHEMY_DATABASE_URI = 'postgresql://%s/colors' % 'postgres:example@db' if os.environ.get('DOCKERIZED') else 'localhost'
