from pymongo import MongoClient
from modularodm import storage
from model import User, Comment
import couchdb

USE_COUCH = True

if not USE_COUCH:

    print ("using mongo")
    client = MongoClient()
    db = client['testdb']
    User.set_storage(storage.MongoStorage(db, collection="user"))
    Comment.set_storage(storage.MongoStorage(db, collection="comment"))

else:

    print ("using couch")
    server = couchdb.Server()
    db = server.create('test')  # new db
    User.set_storage(storage.CouchStorage(db, collection="user"))
    Comment.set_storage(storage.CouchStorage(db, collection="comment"))