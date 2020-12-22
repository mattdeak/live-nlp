import gensim
from gensim import corpora

import tensorflow as tf
import tensorflow_hub as hub


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
