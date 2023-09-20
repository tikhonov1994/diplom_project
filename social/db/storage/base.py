from db.mongo_client import MongoClientDep
from core.config import app_config


class MongoStorageBase:
    def __init__(self, mongo_client: MongoClientDep) -> None:
        self.client = mongo_client
        self.db = self.client[app_config.mongo.social_database]
