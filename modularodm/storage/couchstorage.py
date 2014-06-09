from couchdb.mapping import Mapping
from .base import Storage
from ..query.queryset import BaseQuerySet
from ..query.query import RawQuery
from modularodm.exceptions import NoResultsFound, MultipleResultsFound

class CouchQuerySet(BaseQuerySet):
    def __init__(self, schema, view_results):

        """Initialize CouchQuerySet
        :param schema: ObjectMeta class defined by the use case's model, eg. User class
        :param view_results: result object returned by Couchdb
        """

        super(CouchQuerySet, self).__init__(schema)
        self.data = view_results

    def __iter__(self, raw=False):
        keys = [obj.value[self.primary] for obj in self.data.rows]
        if raw:
            return keys
        return (self.schema.load(key) for key in keys)

    def __getitem__(self, index, raw=False):
        super(CouchQuerySet, self).__getitem__(index)
        key = self.data[index][self.primary]
        if raw:
            return key
        return self.schema.load(key)

    def get_keys(self):
        return list(self.__iter__(raw=True))

    def __len__(self):
        self.data.total_rows

    count = __len__


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

        :param query: a RawQuery object containing attribute, operator, argument
        :param kwargs:
        :return: ViewResults, a CouchDB object that results of the query
        """
        mapfun, argument = self._translate_query(query)

        return self.db.query(mapfun, key=argument)

    def find_one(self, query=None, **kwargs):
        """
        :param query: query: a RawQuery object containing attribute, operator, argument
        :param kwargs:
        :return: an object of the class that called it.
        """

        mapfun, argument = self._translate_query(query)

        matches = self.db.query(mapfun, key=argument)

        if len(matches.rows) == 1:
            return matches.rows[0].value

        if len(matches.rows) == 0:
            raise NoResultsFound()

        raise MultipleResultsFound(
            'Query for find_one must return exactly one result; '
            'returned {0}'.format(matches.count())
        )


    def get(self, primary_name, key):
        return self.store.find_one({primary_name: key})

    def update(self, query, data):

        """ Update a record that matches a query with the provided data
        :param query: RawQuery object containing search terms
        :param data: dict object {'<fieldname>': <'newvalue'>}
        """

        # Create a ViewResult
        mapfun, argument = self._translate_query(query)
        couch_view_results = self.db.query(mapfun, key=argument)

        # Iterate through the rows of a result and change the appropriate rows
        # TODO(asmacdo) fewer calls
        docs_to_change = {}
        for row in couch_view_results.rows:
            for key in data:
                if row.value.get(key) is not None:
                    row.value[key] = data[key]
                    doc = row.value


        #TODO (asmacdo) add case for '_id'



    def _translate_query(self, query=None, couch_query=None):
        """
        Convert a RawQuery object to appropriate javascript for a couchdb map function and add appropriate args
        :param query: a RawQuery object
        :param couch_query: string of javascript that is passed to couch as a mapfunction
        :return: tuple containing a couchdb query and a search argument
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
                couch_query = "function(doc) {{\n  if ('{field}' in doc) {{\n    emit(doc.{field}, doc)\n  }}\n}}".format(field=attribute)

        return couch_query, argument