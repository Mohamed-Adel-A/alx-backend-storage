#!/usr/bin/env python3
"""
Return the list of schools having a specific topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic: Topic searched.

    Returns:
        List of school documents with the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
