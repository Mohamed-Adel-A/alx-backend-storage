#!/usr/bin/env python3
"""
Insert a new document in a collection based on kwargs
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection: pymongo collection object.
        **kwargs: key-value pairs to be inserted as document fields.

    Returns:
        New _id of the inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id

