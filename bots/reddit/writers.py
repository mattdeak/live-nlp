import json
import safer

from pymongo import MongoClient


class JSONWriter:
    def __init__(
        self, outfile_path, comment_attributes=["body", "created_utc", "id", "score"]
    ):
        self.outfile_path = outfile_path
        self.comment_attributes = comment_attributes

    def run(self, data):
        data["comment"] = {
            key: getattr(data["comment"], key) for key in self.comment_attributes
        }
        assert type(data) == dict, "JSONWriter requires DICT input"
        # Assures atomic write operation.
        with safer.open(self.outfile_path, "a") as outfile:
            json.dump(data, outfile)
            outfile.write("\n")


class MongoWriter:
    def __init__(
        self,
        database_name,
        collection_name,
        host="db",
        port=27017,
        comment_attributes=["body", "created_utc", "id", "score"],
    ):
        self.comment_attributes = comment_attributes
        self.client = MongoClient(host, port)
        self.collection = self.client[database_name][collection_name]

    def run(self, data):
        # TODO: Implement bulk update capability.
        if type(data) == list:
            raise NotImplementedError("Bulk Updates not yet supported")

        data["comment"] = {
            key: getattr(data["comment"], key) for key in self.comment_attributes
        }

        assert type(data) == dict, "MongoWriter requires DICT input"

        self.collection.insert_one(data)


