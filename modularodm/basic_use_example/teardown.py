import couchdb
from pymongo import MongoClient

couch = couchdb.Server()
couch.delete('test')

mongo = MongoClient('localhost', 27017)
db = mongo.test_database
db.drop_collection('test_collection')