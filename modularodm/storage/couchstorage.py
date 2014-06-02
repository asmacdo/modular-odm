from couchdb.mapping import Mapping
from .base import Storage
from ..query.query import RawQuery

class CouchStorage(Storage):

    #TODO Queryset

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

        print value
        self.db.save(value)

    def update(self, query, data):
        pass
        #couch_query = self._translate_query(query)

    def _translate_query(self, query=None, couch_query=None):

        couch_query = couch_query or {}

        if isinstance(query, RawQuery):
            attribute, operator, argument = \
                query.attribute, query.operator, query.argument

            if operator == 'eq':
                query.operator = "=="

            couch_query = '''
                function(doc, emit) {
                    return '{query.attribute}' === '{query.argument}'
                }
                '''.format(query=query)
        return couch_query



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