#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
"""

def log_stats(mongo_collection):
    """
    Provide some stats about Nginx logs stored in MongoDB
    """
    count = mongo_collection.count_documents({})
    print(f"{count} logs")
    
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = mongo_collection.count_documents({ "method": method })
        print(f"    method {method}: {method_count}")
    
    status_check_count = mongo_collection.count_documents({ "method": "GET", "path": "/status" })
    print(f"{status_check_count} status check")
