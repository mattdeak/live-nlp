import pickle
import datetime
import asyncio
import os

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
        data = self.scraper.run()
        processed = self.preprocessor.preprocess(data)
        lda_model = self.analyzer.analyze(processed)

        with open(os.path.join(self.log_dir, str(timestamp)), 'wb+') as outfile:
            pickle.dump(lda_model, outfile)

        await asyncio.sleep(self.refresh_rate*60)


