import gensim
from gensim import corpora

import requests
import json


class DummyAnalyzer:
    """DummyAnalyzer

    A dummy class that does essentially nothing. Used for testing"""

    def run(self, data):
        return data


class TFModelClient:
    """TFModelClient

    Communicates with a TF Model Server using a REST API"""

    def __init__(self, port, model_name):
        self.port = port
        self.model_name = model_name

    def run(self, data):
        headers = {"content-type": "application/json"}

        json_data = json.dumps({"signature_name": "serving_default", "instances": data})
        json_response = requests.post(
            f"http://localhost:{self.port}/v1/models/{self.model_name}:predict",
            data=json_data,
            headers=headers,
        )

        predictions = json.loads(json_response.text)["predictions"]
        return predictions


class SimpleTopicModel:
    """SimpleTopicModel

    Uses simple bigram LDA to generate topics. Uses gensim."""

    def __init__(self, num_topics=5):
        self.num_topics = num_topics

    def analyze(self, documents):
        bigram = gensim.models.Phrases(documents, min_count=5, threshold=100)
        bigram_model = gensim.models.phrases.Phraser(bigram)
        texts = [bigram_model[doc] for doc in documents]

        # Topic Models
        id2word = corpora.Dictionary(texts)

        # TDF
        corpus = [id2word.doc2bow(text) for text in texts]

        # LDA
        lda_model = gensim.models.ldamodel.LdaModel(
            corpus=corpus,
            id2word=id2word,
            num_topics=self.num_topics,
            update_every=1,
            chunksize=100,
            passes=10,
            per_word_topics=True,
        )

        return lda_model


class KerasModel:
    def __init__(self, model, return_comments=False):
        self.model = model
        self.return_comments = return_comments

    def analyze(self, documents):
        preds = self.model.predict(documents)
        if self.return_comments:
            return (documents, preds)
        else:
            return preds
