import motor
from tornado import gen
import os
from datetime import datetime


class Users():
    def __init__(self):
        url = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
        self._client = motor.motor_tornado.MotorClient(url)
        self._db = self._client.get_default_database()
        self._collection = self._db['users']

    def drop(self):
        self._db.drop_collection('users')

    @gen.coroutine
    def get_user(self, user_id):
        user = yield self._collection.find_one({'_id': user_id})
        if user:
            return user

        yield self._collection.update({'_id': user_id},
            {'$set': {'last_modified': datetime(1989, 8, 24)}},
            upsert=True)

        return (yield self._collection.find_one({'_id': user_id}))

    @gen.coroutine
    def update_user(self, user):
        user['last_modified'] = datetime.utcnow()
        user_id = user.pop('_id')
        yield self._collection.update({'_id': user_id}, {'$set': user})
