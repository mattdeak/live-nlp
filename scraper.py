import praw
from praw.models import MoreComments, Submission
import json
import multiprocessing
import logging
import yaml

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


class SubmissionScraper:
    """SubmissionScraper

    Watches one submission and returns scraped data. Updates the database according to changes.
    """

    def __init__(self, submission_id, only_top_level_comments=True):
        self.__name__ = self.__class__.__name__
        self.only_top_level_comments = only_top_level_comments
        self.submission_id = submission_id
        self.reddit_client = get_reddit()
        self.initialized = False

        self.logger = logging.getLogger("app")

    def reset(self):
        self.submission = Submission(self.reddit_client, id=self.submission_id)
        self.data = {"created_utc": self.submission.created_utc}
        self.data["comments"] = {}
        self.logger.info("Scraper Initialized")
        self.refresh()

    def refresh(self):
        if not self.initialized:
            self.initialized = True
            self.reset()
        else:
            self.logger.info("Refreshing")
            self.submission = Submission(self.reddit_client, id=self.submission_id)

        self.data["score"] = self.submission.score
        self.data["upvote_ratio"] = self.submission.upvote_ratio
        self.data["url"] = self.submission.url
        self.process_comments()

    def process_comments(self):
        """get_comments

        Parameters
        ----------

        submission : praw.Reddit.Submission

        Returns: Top-level comments of subreddit
        -------
        """
        # Re-processing comments
        submission = self.submission
        submission_id = self.submission_id
        submission.comments.replace_more(limit=None)

        if self.only_top_level_comments:
            for top_level_comment in submission.comments:
                self.data["comments"][top_level_comment.id] = {
                    "text": top_level_comment.body,
                    "score": top_level_comment.score,
                }
        else:
            for comment in submission.comments.list():
                self.data["comments"][comment.id] = {
                    "text": comment.body,
                    "score": comment.score,
                }

        
        self.logger.info(f'Number of Comments Updated: {len(self.data["comments"])}')

    def run(self):
        self.refresh()
        return self.data


class RedditScraper:  # TODO
    """SubredditScraper"""

    def __init(self, reddit_query):
        pass
