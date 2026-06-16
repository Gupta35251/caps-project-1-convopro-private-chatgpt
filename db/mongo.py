from config.settings import settings
from pymongo import MongoClient

settings = settings()

_client = MongoClient(settings.MONGO_DB_URL,tz_aware = True)  # tz_aware - time zone prints
_db = _client[settings.MONGO_DB_NAME]

def get_collection(name:str):
    return _db[name]

