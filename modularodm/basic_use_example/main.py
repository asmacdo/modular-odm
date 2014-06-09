from modularodm.basic_use_example.model import User, Comment
from pymongo import MongoClient
from modularodm import storage
import couchdb
from modularodm.query.querydialect import DefaultQueryDialect as Q

# Switch from couch to mongo
USE_COUCH = True




# Set model storage
if USE_COUCH:
    #Remove old db and start a fresh instance
    couch = couchdb.Server()
    couch.delete('odm')

    server = couchdb.Server()
    db = server.create('odm')  # new db
    User.set_storage(storage.CouchStorage(db, collection="user"))
    Comment.set_storage(storage.CouchStorage(db, collection="comment"))


else:
    client = MongoClient()
    client.drop_database('testdb')
    db = client['testdb']
    User.set_storage(storage.MongoStorage(db, collection="user"))
    Comment.set_storage(storage.MongoStorage(db, collection="comment"))

# Initialize users
u = User(username="austing", password="notpassword")
u.save()
u2 = User(username="notAustin", password="password")
u2.save()
u3 = User(username="austin", password="sixchars")
u3.save()
u4 = User(username="austin", password="different")
u4.save()

# Initialize comments
comment = Comment(text="And blah", user=u)
comment2 = Comment(text="It's just", user=u)
comment3 = Comment(text="Uh oh", user=u2)
comment.save()
comment2.save()
comment3.save()

# you can now search for all docs with username
# db.save(create_basic_query("text"))

# make a query from a Q
q = Q('username', 'eq', 'austing')

#query database
results = User.find(q)
print "\n\n\n\n"

if USE_COUCH:
    print "results ", results.data.rows[0].value
else:
    print results.data[0]

print "\n\n\n\n"
one_results = User.find(q)#, "before update"
print "before update", one_results

print User.update(q, {'username': "newAustin"})
new_q = Q('username', 'eq', 'newAustin')
find2 = User.find(new_q)

User.remove(new_q)

results = User.find(new_q)
print "\n\n\n\n"

if USE_COUCH:
    try:
        print "results ", results.data.rows[0].value
    except IndexError:
        print "no data"
else:
    try:
        results.data[0]
        print "data"
    except IndexError:
        print "no data"