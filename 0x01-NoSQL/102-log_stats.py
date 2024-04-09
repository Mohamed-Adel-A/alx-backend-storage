#!/usr/bin/env python3
"""
Provides improved stats about Nginx logs stored in MongoDB, including top 10 IPs.
"""

from pymongo import MongoClient

def log_stats_new(mongo_collection):
    """
    Provides improved stats about Nginx logs stored in MongoDB, including top 10 IPs.

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

    # Top 10 IPs
    top_ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip_data in top_ips:
        print(f"    {ip_data['_id']}: {ip_data['count']}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    log_stats_new(logs_collection)
