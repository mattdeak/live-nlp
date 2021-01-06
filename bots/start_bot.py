import logging
import sys
import multiprocessing
import argparse

from analyzers import DummyAnalyzer, KerasModel, SimpleTopicModel, TFModelClient
from bots import RedditStreamer
from reddit.preprocessors import CommentBodyExtractor, SimplePreprocessor
from reddit.writers import JSONWriter, MongoWriter
import os

from utils import initialize_preprocessor, initialize_analyzer, initialize_writer


logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


DB_NAME = os.environ.get('DB_NAME', 'test_db')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 27017)

def initialize_bot(bot_config):
    bot_type = bot_config["bot_type"]
    query = bot_config["query"]

    bot_kwargs = bot_config.get("bot_kwargs", {})

    preprocessor = bot_config.get("preprocessor", "CommentBodyExtractor")
    preprocessor_args = bot_config.get("preprocessor_args", [])
    preprocessor = initialize_preprocessor(preprocessor, *preprocessor_args)

    analyzer = bot_config["analyzer"]
    analyzer_args = bot_config.get("analyzer_args", [])
    analyzer = initialize_analyzer(analyzer, *analyzer_args)

    writer_name = bot_config["writer"]
    writer_kwargs = bot_config["writer_kwargs"]
    writer = initialize_writer(writer_name, **writer_kwargs)
    # Initialize and Start Bot
    if bot_type == "reddit_streamer":
        bot = RedditStreamer(query, preprocessor, analyzer, writer, **bot_kwargs)

    return bot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot_type", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--db_host", default=DB_HOST)
    parser.add_argument("--db_port", type=int, default=DB_PORT)
    parser.add_argument("--db_name", default=DB_NAME)
    parser.add_argument("--preprocessor", default="CommentBodyExtractor")
    parser.add_argument("--analyzer", default="DummyAnalyzer")
    parser.add_argument("--writer", default="MongoWriter")
    args = parser.parse_args()

    config = {
        "bot_type": args.bot_type,
        "query": args.query,
        "preprocessor": args.preprocessor,
        "analyzer": args.analyzer,
        "writer": args.writer,
        "writer_kwargs": {
            "host": args.db_host,
            "port": args.db_port,
            "database_name": args.db_name,
            "collection_name": args.query,
        },
    }

    bot = initialize_bot(config)
    bot.run()
