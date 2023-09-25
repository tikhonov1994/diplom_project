from core.config import app_config
from db.mongo_client import MongoClientDep


class MongoStorageBase:
    def __init__(self, mongo_client: MongoClientDep) -> None:
        self.client = mongo_client
        self.db = self.client[app_config.api.mongo_database]
