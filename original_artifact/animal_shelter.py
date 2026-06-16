from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host='localhost', port=27017, db='aac', col='animals'):
        """
        Initialize connection to MongoDB using credentials supplied by the Dash dashboard or test script.
        """

        # Build MongoDB connection URI
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin"

        # Initialize connection
        try:
            self.client = MongoClient(uri)
            self.database = self.client[db]
            self.collection = self.database[col]
        except Exception as e:
            raise Exception(f"Could not connect to MongoDB: {e}")

    # --------------------- CREATE ---------------------

    def create(self, data):
        """
        Inserts a document into the aac.animals collection.
        Returns True if the insert is acknowledged, else False.
        """
        if data is not None:
            result = self.collection.insert_one(data)
            return True if result.acknowledged else False
        else:
            return False

    # --------------------- READ ---------------------

    def read(self, query):
        """
        Queries for document(s) from a specified MongoDB collection.
        Returns a list of matching documents.
        """
        if query is not None:
            cursor = self.collection.find(query)
            return list(cursor)
        else:
            return []

    # --------------------- UPDATE ---------------------

    def update(self, query, new_values):
        """
        Updates document(s) that match the query.
        Returns the number of documents updated.
        """
        if query is not None and new_values is not None:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        else:
            return 0

    # --------------------- DELETE ---------------------

    def delete(self, query):
        """
        Deletes document(s) that match the query.
        Returns the number of documents deleted.
        """
        if query is not None:
            result = self.collection.delete_many(query)
            return result.deleted_count
        else:
            return 0
