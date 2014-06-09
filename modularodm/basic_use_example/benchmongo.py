from modularodm.basic_use_example.model import User, Comment
from pymongo import MongoClient
import couchdb
from modularodm import storage
import random
import string
from modularodm.query.querydialect import DefaultQueryDialect as Q
import benchmark

USE_COUCH = False
num_tests = 10000

def create_rand_string():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(11))


def create_rand_doc():
    s1 = create_rand_string()
    s2 = create_rand_string()
    s3 = create_rand_string()
    doc = {s1: {s2: s3}}
    return doc

class Benchmark_DB(benchmark.Benchmark):

    each = num_tests

    def setUp(self):
        self.size = 1

        if USE_COUCH:
            print "Using Couch"
            self.client = couchdb.Server()  # localhost:5984
            self.db = self.client.create('test')

            User.set_storage(storage.CouchStorage(self.db, collection="user"))
            Comment.set_storage(storage.CouchStorage(self.db, collection="comment"))
        else:
            print "Using Mongo"
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['testdb']
            self.collection = self.db.test_collection
            User.set_storage(storage.MongoStorage(self.db, collection="user"))
            Comment.set_storage(storage.MongoStorage(self.db, collection="comment"))


    def test_add_doc(self):
        u = User(_id=create_rand_string(), username=create_rand_string(), password=create_rand_string())
        u.save()



if __name__ == '__main__':
    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.
