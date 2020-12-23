import logging
from scraper import SubmissionScraper
from streamer import RedditStreamer
from preprocessors import SimplePreprocessor, Listifier, DummyPreprocessor
from analyzers import SimpleTopicModel, KerasModel, DummyAnalyzer
from livebot import LiveBot
import sys
import asyncio
import tensorflow as tf
import tensorflow_text as text

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(  
           '%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    # scraper = SubmissionScraper('khwq8w', only_top_level_comments=False)
    preprocessor = DummyPreprocessor()
    analyzer = DummyAnalyzer()
    # preprocessor = SimplePreprocessor()
    # analyzer = SimpleTopicModel()

    # bert_sentiment_model = tf.keras.models.load_model('models/test_model_BERT')
    # analyzer = KerasModel(bert_sentiment_model, return_comments=True)
    # simple_livebot = LiveBot(scraper, preprocessor, analyzer, refresh_rate=1)

    bot = RedditStreamer('news', preprocessor, analyzer, None)
    bot.run()





