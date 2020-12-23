import json
import safer


class JSONWriter:
    def __init__(self, outfile_path, comment_attributes=['body','created_utc','id','score']):
        self.outfile_path = outfile_path
        self.comment_attributes = comment_attributes

    def run(self, data):
        data['comment'] = {key: getattr(data['comment'], key) for key in self.comment_attributes}
        assert type(data) == dict, "JSONWriter requires DICT input"
        # Assures atomic write operation.
        with safer.open(self.outfile_path, 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

