import os
import pymongo
from django.conf import settings

MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
mongo_settings = settings.DATABASES['default']['CLIENT']  # Get the MongoDB client settings from DATABASES

client = pymongo.MongoClient(
    mongo_settings['host'],
    username=mongo_settings['username'],
    password=mongo_settings['password'],
    authSource=mongo_settings['authSource'],
    authMechanism=mongo_settings['authMechanism']
)

db = client[settings.DATABASES['default']['NAME']]  # Database name
session_collection = db[MONGO_COLLECTION]  # Collection name