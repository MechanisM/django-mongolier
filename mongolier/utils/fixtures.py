"""
fixtures.py

A module for creating json fixtures that can be imported into MongoDB and 
exporting fixtures from MongoDB

"""
import sys

from bson import json_utils
from bson.objectid import ObjectId

class FixtureBase(object):
    """
    FixtureBase

    Currently only holds the connection object
    """

    def __init__(self, connection, respect_objectid=False):
        
        self.connection = connection

        if respect_objectid:
            self.respect_objectid = True

class CreateFixture(FixtureBase):
    """
    Creates a fixture (json file) that is a representation of a 
    MongoDB collection

    Uses a standard style to store objects.

    {'objectid_3344545aa4453445': ['foo','bar']}

    If respect_objectid is set to true, it will store the key prefaced 
    (like above) so that when it restores objects, it retains their id.

    """

    def create(self):

        fixture_dict = {}

        for document in connection.find():
            
            if isinstance(key, ObjectId) and self.respect_objectid:
                key = 'objectid_%s' % document['_id']
            else:
                key = document['_id']                

            document.pop('_id')

            fixture_dict[key] = document

        
        sys.stdout.write(json.dumps(fixture_dict, default=json_utils.default))
        

class LoadFixture(FixtureBase):
    """
    Loads a fixture (json file) into MongoDB.

    """

    def load(self, fixture):
       
        with open(fixture, 'rb') as fixtures_file_obj:
            fixture_dict = json.load(fixtures_file_obj, object_hook=json_utils.object_hook)

        for key, document in fixture_dict.items():
            if 'objectid_' in key and self.respect_objectid:
                document['_id'] = ObjectId(key.split('objectid_')[1])
                 
            document['_id'] = key
            connection.insert(document)