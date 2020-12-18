import pickle
import datetime
import asyncio
import os

import logging

# ---- LOGGING INIT ---- #
logger = logging.getLogger('app')

# ---- Live Bot ---- #
class LiveBot:

    def __init__(self, scraper, preprocessor, analyzer, refresh_rate=5, log_dir='./'):
        """__init__

        Parameters
        ----------

        scraper : SubmissionScraper
        preprocessor : Preprocessor
        analyzer : Analyzer
        refresh_rate : Delay between refreshes (mins)
        log_dir : output directory of LDA

        -------
        """
        self.scraper = scraper
        self.preprocessor = preprocessor
        self.analyzer = analyzer
        self.refresh_rate = refresh_rate
        self.log_dir = log_dir


    async def run(self):
        timestamp = datetime.datetime.now().timestamp()

        logger.debug('Running Scraper')
        data = self.scraper.run()
        logger.debug('Running Preprocessor')
        processed = self.preprocessor.preprocess(data)
        logger.debug('Running Running Analyzer')
        lda_model = self.analyzer.analyze(processed)

        logger.debug('Saving LDA Model') 
        with open(os.path.join(self.log_dir, str(timestamp)), 'wb+') as outfile:
            pickle.dump(lda_model, outfile)

        logger.debug('Sleeping')
        await asyncio.sleep(self.refresh_rate*60)

