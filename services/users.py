import pymongo
import os
from datetime import datetime


class Users():
    def __init__(self):
        url = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
        self._client = pymongo.MongoClient(url)
        self._db = self._client.get_default_database()
        self._collection = self._db['users']

    def drop(self):
        self._db.drop_collection('users')

    def get_user(self, user_id):
        user = self._collection.find_one({'_id': user_id})
        if user:
            return user

        self._collection.update_one({'_id': user_id},
            {'$set': {'last_modified': datetime(1989, 8, 24)}},
            upsert=True)

        return self._collection.find_one({'_id': user_id})

    def update_user(self, user):
        user['last_modified'] = datetime.utcnow()
        user_id = user.pop('_id')
        self._collection.update_one({'_id': user_id}, {'$set': user})
