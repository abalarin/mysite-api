import os
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
with open(APP_ROOT + '/config.json') as config_file:
    config = json.load(config_file)

# Object Storage
from myapi.objectstorage.configer import getConfig
from myapi.objectstorage.authBoto import botoClient, botoResource

configParser = getConfig(APP_ROOT + '/objectstorage/config.ini')
client = botoClient(config.get('BOTO_KEY'), config.get('BOTO_SECRET'), configParser['object_api']['base_url'], configParser['object_api']['user'])
resource = botoResource(config.get('BOTO_KEY'), config.get('BOTO_SECRET'), configParser['object_api']['base_url'], configParser['object_api']['user'])

# DB init
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

engine = create_engine(config.get('DB_URI'), echo=False, pool_pre_ping=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Blueprint
from myapi import endpoints
