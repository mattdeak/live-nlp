import json
import logging
import multiprocessing
import queue
import threading
import time
from abc import ABC, abstractmethod

import praw
import yaml
from praw.models import MoreComments, Submission

# -------------------------------------------------------------- #

# Utility function for generating a reddit client
def get_reddit(credentials_filepath="credentials.json"):
    with open(credentials_filepath, "r") as credentials_file:
        credentials = json.load(credentials_file)

    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["secret"],
        password=credentials["password"],
        user_agent=credentials["user_agent"],
        username=credentials["username"],
    )

    return reddit


def get_subreddits(reddit, subreddit_list):
    subreddits = reddit.subreddit("+".join(subreddit_list))
    return subreddits


class RedditStreamer:
    """RedditStreamer

    Collects and analyzes streamed data from a subreddit
    """

    def __init__(
        self, subreddit_name, preprocessor, analyzer, result_handler, min_refresh_rate=3
    ):
        self.__name__ = self.__class__.__name__
        self.subreddit_name = subreddit_name
        # Preprocessor manipulates streamed comments and reformats
        # Analyzer performs some analysis on processed comments
        # Result handler decides what to do with result of analysis
        self.preprocessor = preprocessor
        self.analyzer = analyzer
        self.result_handler = result_handler

        self.reddit_client = get_reddit()
        self.initialized = False
        self.min_refresh_rate = min_refresh_rate

        self.logger = logging.getLogger("app")
        self.reset()

    def reset(self):
        self.logger.debug("Initializing Subreddit Instance")
        self.subreddit = self.reddit_client.subreddit(self.subreddit_name)
        self.data = {"created_utc": self.subreddit.created_utc}
        self.data["comments"] = {}
        self.logger.info("Scraper Initialized")

    def run(self):
        """run
        
        Streams comments from a subreddit.
        """
        new_comment_queue = queue.Queue()
        analyzed_comment_queue = queue.Queue()

        scraping_thread = threading.Thread(
            target=self._streaming_thread, args=(new_comment_queue,)
        )
        analysis_thread = threading.Thread(
            target=self._analysis_thread,
            args=(new_comment_queue, analyzed_comment_queue),
        )
        result_handler_thread = threading.Thread(
            target=self._result_handler_thread, args=(analyzed_comment_queue,)
        )

        scraping_thread.start()
        analysis_thread.start()
        result_handler_thread.start()

    def _streaming_thread(self, q):
        self.logger.info("Starting Streaming Thread")
        for comment in self.subreddit.stream.comments():

            q.put(comment)

    def _analysis_thread(self, new_q, analyzed_q):
        """_analysis_thread

        Parameters
        ----------

        new_q : New Comments Queue (queue.Queue)
        analyzed_q : Analyzed Comments Queue (queue.Queue)
        -------
        """
        # Either wait for batch size or timeout
        analysis_batch = []
        timedout = False
        num_items_stored = 0

        start_time = time.time()
        while True:
            time_remaining_before_auto_refresh = (
                start_time + self.min_refresh_rate - time.time()
            )

            if time_remaining_before_auto_refresh <= 0:
                self.logger.debug("Analysis Thread Timeout")
                timedout = True

            else:
                try:
                    self.logger.debug("Retrieving comment from Queue")
                    comment = new_q.get(timeout=time_remaining_before_auto_refresh)
                    analysis_batch.append(comment)
                    num_items_stored += 1

                except queue.Empty:
                    self.logger.debug("Timeout on Analysis Queue")
                    timedout = True

            if num_items_stored >= 32 or timedout:  # TODO 32 should be a param
                if timedout:
                    timedout = False

                if num_items_stored != 0:
                    self.logger.info(f"Running Analysis on {num_items_stored} Comments")
                    analyzed = self.analyzer.run(analysis_batch)
                    num_items_stored = 0
                    analysis_batch = []

                    for item in analyzed:
                        analyzed_q.put(item)
                

                start_time = time.time()

    def _result_handler_thread(self, analyzed_q):
        # TODO: Implement this whole thing.
        # ---- DUMMY for TESTING
        while True:
            data = analyzed_q.get(block=True)
            self.logger.info(data.body)
