import json


class JSONWriter:
    def __init__(self, outfile_path, comment_attributes=['body','created_utc','id','score']):
        self.outfile = open(outfile_path, "a")
        self.comment_attributes = comment_attributes

    def run(self, data):
        data['comment'] = {key: getattr(data['comment'], key) for key in self.comment_attributes}
        assert type(data) == dict, "JSONWriter requires DICT input"
        json.dump(data, self.outfile)
