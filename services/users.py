import pymongo
import os


class Users():
  def __init__(self):
    url = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
    self._client = pymongo.MongoClient(url)
    self._db = self._client.get_default_database()
    self._collection = self._db['users']
    self._collection.insert({'id':-1})

  def get_user(self, user_id):
    self._collection.update_one({'_id': user_id},
      {'$set': {'_id': user_id}}, upsert=True)

    return self._collection.find_one({'_id': user_id})

  def update_user(self, user):
    user.pop('lastModified')
    self._collection.update_one({'_id': user['_id']},
      {'$set': user,
       '$currentDate': {'lastModified': True}})
