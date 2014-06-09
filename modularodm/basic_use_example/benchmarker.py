from modularodm.basic_use_example.model import User, Comment, User2, Comment2
from pymongo import MongoClient
from modularodm import storage
import couchdb
import random
import string
from modularodm.query.querydialect import DefaultQueryDialect as Q
import benchmark

num_tests = 1000


def create_rand_string():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(8))

i = 1
def create_seq_string():
    global i
    i += 1
    return str(i)


def create_rand_doc():
    s1 = create_rand_string()
    s2 = create_rand_string()
    s3 = create_rand_string()
    doc = {s1: {s2: s3}}
    return doc

class Benchmark_Couch(benchmark.Benchmark):

    each = num_tests

    def setUp(self):
        self.size = 1
        self.couch = couchdb.Server()  # localhost:5984
        self.db = self.couch.create('test')
        User2.set_storage(storage.CouchStorage(self.db, collection="user"))
        Comment2.set_storage(storage.CouchStorage(self.db, collection="comment"))

    def test_add_doc(self):
        u = User2(_id= create_rand_string(), username=create_rand_string(), password=create_rand_string())
        u.save()

    # def test_add_doc_seq(self):
    #     u = User2(_id=create_seq_string(), username=create_rand_string(), password=create_rand_string())
    #     u.save()

    def tearDown(self):
        self.couch.delete('test')

class Benchmark_Mongo(benchmark.Benchmark):

    each = num_tests

    def setUp(self):
        self.size = 1
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['testdb']
        self.collection = self.db.test_collection
        User.set_storage(storage.MongoStorage(self.db, collection="user"))
        Comment.set_storage(storage.MongoStorage(self.db, collection="comment"))


    def test_add_doc(self):
        u = User(_id=create_rand_string(), username=create_rand_string(), password=create_rand_string())
        u.save()

    # def test_add_doc_seq(self):
    #     u = User(_id=create_rand_string(), username=create_rand_string(), password=create_rand_string())
    #     u.save()


    def tearDown(self):
        self.db.drop_collection('test_collection')

# class Benchmark_Modular_Mongo(benchmark.Benchmark):
#
#     each = num_tests
#
#     def setUp(self):
#         client = MongoClient()
#         client.drop_database('testdbMongo')
#         self.db = client['testdbMongo']
#         User.set_storage(storage.MongoStorage(self.db, collection="user"))
#         Comment.set_storage(storage.MongoStorage(self.db, collection="comment"))
#
#     def add_one(self):
#         u = User(username=create_rand_string(), password=create_rand_doc())
#         u.save()
#         comment = Comment(text="And now for something completely different.", user=u)
#         comment2 = Comment(text="It's just a flesh wound.", user=u)
#         comment.save()
#         comment2.save()
#
#     def tearDown(self):
#         self.db.drop_collection('user')
#         self.db.drop_collection('comment')
#
#     # def all_comments_byvne(Q("username", "eq", "unladenswallow"))
#     #     #u.comment__comments


if __name__ == '__main__':
    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.

