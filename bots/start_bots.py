import logging
import sys

from analyzers import DummyAnalyzer, KerasModel, SimpleTopicModel, TFModelClient
from bots import RedditStreamer
from reddit.preprocessors import CommentBodyExtractor, SimplePreprocessor
from reddit.writers import JSONWriter, MongoWriter
import os

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

DB_NAME = os.environ["DB_NAME"]
DB_COL = os.environ["DB_COL"]

# TODO: This will have to be a published service eventually. A simply websocket should be fine.
if __name__ == "__main__":
    preprocessor = CommentBodyExtractor()
    # analyzer = TFModelClient(8501, "BERT_test1")
    analyzer = DummyAnalyzer()
    writer = MongoWriter(DB_NAME, DB_COL)

    bot = RedditStreamer("news", preprocessor, analyzer, writer)
    bot.run()
