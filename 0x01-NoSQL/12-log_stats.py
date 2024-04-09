#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        None
    """
    # Total number of logs
    total_logs = mongo_collection.count_documents({})

    # Number of logs by method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents({"method": method}) for method in methods}

    # Number of logs with method=GET and path=/status
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")
