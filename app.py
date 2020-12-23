import asyncio
import logging
import sys

import tensorflow as tf
import tensorflow_text as text

from analyzers import (DummyAnalyzer, KerasModel, SimpleTopicModel,
                       TFModelClient)
from bots import RedditStreamer
from reddit.preprocessors import CommentBodyExtractor, SimplePreprocessor

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(  
           '%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    preprocessor = CommentBodyExtractor()
    analyzer = TFModelClient(8501, 'BERT_test1')

    bot = RedditStreamer('news', preprocessor, analyzer, None)
    bot.run()
