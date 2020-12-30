import json
from pymongo import MongoClient
import pandas as pd


class MongoReader:
    def __init__(
        self,
        database_name,
        collection_name,
        host="localhost",
        port=27017,
        comment_attributes=["body", "created_utc", "id", "score"],
    ):
        self.client = MongoClient(host, port)
        self.collection = self.client[database_name][collection_name]

    def run(self, last_datetime, comment_return_fields=["body", "created_utc"]):
        # TODO: Optimize. This feels really inefficient.
        cursor = self.collection.find({"comment.created_utc": {"$gt": last_datetime}})
        search_results = list(cursor)
        pruned_comments = []
        for result in search_results:

            pruned_comment = {
                field: result["comment"][field] for field in comment_return_fields
            }
            pruned_comment['analysis'] = result['analysis'][0]
            pruned_comments.append(pruned_comment)

        return pruned_comments
