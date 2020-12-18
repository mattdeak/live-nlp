import logging
from scraper import SubmissionScraper
from preprocessors import SimplePreprocessor
from analyzers import SimpleTopicModel
from livebot import LiveBot
import sys
import asyncio

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(  
           '%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    scraper = SubmissionScraper('kfqvif', only_top_level_comments=False)
    preprocessor = SimplePreprocessor()
    analyzer = SimpleTopicModel()
    simple_livebot = LiveBot(scraper, preprocessor, analyzer, refresh_rate=1)

    asyncio.run(simple_livebot.run())




