from couchdb.mapping import Mapping
from .base import Storage
from ..query.queryset import BaseQuerySet
from ..query.query import RawQuery

class CouchQuerySet(BaseQuerySet):
    def __init__(self, schema, cursor):

        super(CouchQuerySet, self).__init__(schema)
        self.data = cursor

    def __iter__(self, raw=False):
        keys = [obj[self.primary] for obj in self.data]
        if raw:
            return keys
        return (self.schema.load(key) for key in keys)

class CouchStorage(Storage):

    QuerySet = CouchQuerySet

    def __init__(self, db, collection):

        """ Get the collection or initialize it.
        :param db: database within th couchDB client
        :param collection:
        :return:
        """
        self.db = db
        self.collection = collection

    def insert(self, primary_name, key, value):


        if 'primary_name' not in value:
            value['primary_name'] = primary_name

        if 'type' not in value:
            value['type'] = self.collection

        self.db.save(value)

    def find(self, query=None, **kwargs):
        """

        :param query: a Q object containing attribute, operator, argument
        :param kwargs:
        :return: results of the query
        """
        mapfun, argument = self._translate_query(query)
        return self.db.query(mapfun, key=argument)


    def update(self, query, data):
        pass

    def _translate_query(self, query=None, couch_query=None):
        """
        Convert a Q object to appropriate javascript for a couchdb map function
        :param query: a Q object
        :param couch_query: string of javascript that is passed to couch as a mapfunction
        :return: couch_query
        """

        ########
        # Create a query document for permanent use
        # couch_query = {
        #     "_id": "_design/{field}".format(field=query.attribute),
        #     "language": "javascript",
        #     "views": {
        #         "basic_query": {
        #             "map": "function(doc) {{\n  if ('{field}' in doc) {{\n    emit(doc.username, null)\n  }}\n}}".format(field=query.attribute)
        #         }
        #     }
        # }
        argument = None
        if isinstance(query, RawQuery):
            attribute, operator, argument = \
                query.attribute, query.operator, query.argument

            if operator == 'eq':
                #couch_query = "function(doc) {{\n  if ('{attribute}' in doc) {{\n    if(doc.{attribute} === '{argument}') {{\n    	emit(doc.{attribute}, null)\n    }}\n  }}\n}}".format(attribute=attribute, argument=argument)
                couch_query = "function(doc) {{\n  if ('{field}' in doc) {{\n    emit(doc.username, null)\n  }}\n}}".format(field=attribute)

        return couch_query, argument


###################
    #AHHHHHHHHHHHHHHHHHHHHHHHh
    # def find(self, query=None, **kwargs):
    #     couch_query = self._translate_query(query)
    #     return self.db.find(couch_query)
    #
    # def _translate_query(self, query=None, couch_query=None):
    #
    #     couch_query = couch_query or {}




#
# User.find(Q('firstname', 'eq', 'brian')
#
#
# {1, 2, 3}
#
#
# def translate_to_js(query):
#
#     translate_map = {
#         'eq': lambda q: '{query.attribute} === {query.argument}'.format(query=query)
#     }
#
#     return translate_map[query.operator]
#
# '''
# function(doc, emit) \{
#     if doc.type == {collection} and {query.loperand} {operator}
# \}
# '''.format(collection=collection, query=query, operator=operator)