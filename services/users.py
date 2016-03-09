import pymongo
import os
from datetime import datetime


class Users():
  def __init__(self):
    url = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
    self._client = pymongo.MongoClient(url)
    self._db = self._client.get_default_database()
    self._collection = self._db['users']
    self._collection.update_one({'_id': -1}, # bootstrap if needed
      {'$set': {'lastModified': datetime.utcnow()}},upsert=True)

  def get_user(self, user_id):
    self._collection.update_one({'_id': user_id},
      {'$set': {'lastModified': datetime.utcnow()}},
      upsert=True)

    return self._collection.find_one({'_id': user_id})

  def update_user(self, user):
    user['lastModified'] = datetime.utcnow()
    user_id = user.pop('_id')
    self._collection.update_one({'_id': user_id},
      {'$set': user})#, '$currentDate': {'lastModified': True}})
