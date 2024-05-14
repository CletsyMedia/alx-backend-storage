#!/usr/bin/env python3
"""
Script that provides advanced stats about Nginx logs stored in MongoDB,
including top 10 most present IP addresses.
"""
import pymongo

def log_stats():
    """
    Display advanced stats about Nginx logs stored in MongoDB.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count status check
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Count IPs
    ip_counts = {}
    for log in collection.find({}, {"ip": 1}):
        ip = log["ip"]
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    print("IPs:")
    for ip, count in sorted_ips:
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    log_stats()

