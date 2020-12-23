import re
import gensim
import spacy

RE_REMOVE_SPECIAL_CHARACTERS = r"[^A-Za-z0-9 \(\)]+"
RE_FIND_MARKDOWN_LINK = r'\[(.+)\]\(([^ ]+?)( "(.+)")?\)'


def extract_markdown_link(text):
    return re.sub(RE_FIND_MARKDOWN_LINK, "\g<1>", text)

class DummyPreprocessor:
    def run(self, data):
        return data

class SimplePreprocessor:
    """SimplePreprocessor

    Simple preprocessing for a topic modelling algorithm.
    Performs:
        1. Removal of special characters
        2. Stopword Removal
        3. Markdown Link Suppression
        4. Lowercasing, removal of non-word tokens

    Discards all data about score, upvote ratio, etc.
    """

    def __init__(self, lang='en'):
        if lang != 'en':
            raise NotImplementedError('Languages aside from en are not supported')

        self.nlp = spacy.load('en_core_web_sm')

    def preprocess(self, data):
        """preprocess

        Parameters
        ----------

        data : Output of SubmissionScraper.run()

        Returns processed comments
        -------
        """
        raw_comments = data["comments"]
        raw_comments = [comment["text"] for comment in raw_comments.values()]
        # Remove Stopwords
        processed_comments = [
            extract_markdown_link(comment) for comment in raw_comments
        ]
        processed_comments = [
            list(gensim.utils.simple_preprocess(comment, deacc=True))
            for comment in processed_comments
        ]

        final_comments = []
        for comment in processed_comments:
            # Extract links

            doc = self.nlp(" ".join(comment))
            processed_tokens = []
            for token in doc:
                if not token.is_stop:
                    processed_tokens.append(token.lemma_)

            final_comments.append(processed_tokens)

        return final_comments


class CommentBodyExtractor:
    """Listifier

    Does nothing but convert comments into a list of documents"""


    def run(self, data):
        comments = [comment.body for comment in data]

        assert type(comments[0]) == str, "Comments should be a list of strings"
        return comments
