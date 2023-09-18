from db.storage import MongoStrageDep


class MongoServiceBase:
    def __init__(self, mongo_storage: MongoStrageDep):
        self.mongo_storage = mongo_storage


__all__ = ['MongoServiceBase']
