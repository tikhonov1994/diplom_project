from db.storage import MongoStrageDep

class ReviewService():
    def __init__(self, mongo_storage: MongoStrageDep) -> None:
        self.mongo_storage = mongo_storage
