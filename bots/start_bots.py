import logging
import sys

import tensorflow as tf
import tensorflow_text as text

from analyzers import DummyAnalyzer, KerasModel, SimpleTopicModel, TFModelClient
from bots import RedditStreamer
from reddit.preprocessors import CommentBodyExtractor, SimplePreprocessor
from reddit.writers import JSONWriter

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# TODO: This will have to be a published service eventually. A simply websocket should be fine.
if __name__ == "__main__":
    preprocessor = CommentBodyExtractor()
    analyzer = TFModelClient(8501, "BERT_test1")
    writer = JSONWriter("data/newstest2")

    bot = RedditStreamer("news", preprocessor, analyzer, writer)
    bot.run()
