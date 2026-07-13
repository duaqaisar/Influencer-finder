from services.embedding_engine import EmbeddingEngine
from services.embedding_cache import EmbeddingCache

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RelevanceEngine:

    TOPIC_KEYWORDS = {

        "fitness": [
            "fitness",
            "gym",
            "workout",
            "training",
            "bodybuilding",
            "exercise",
            "muscle",
            "strength",
            "cardio",
            "yoga"
        ],

        "beauty": [
            "beauty",
            "makeup",
            "skincare",
            "cosmetics",
            "hair"
        ],

        "fashion": [
            "fashion",
            "style",
            "clothing",
            "outfit",
            "designer"
        ],

        "sports": [
            "sports",
            "football",
            "cricket",
            "basketball",
            "athlete"
        ],

        "technology": [
            "technology",
            "coding",
            "software",
            "developer",
            "ai",
            "machine learning"
        ]

    }

    @classmethod
    def get_keywords(
        cls,
        topic
    ):

        topic = topic.lower().strip()

        if topic in cls.TOPIC_KEYWORDS:
            return cls.TOPIC_KEYWORDS[topic]

        return topic.split()

    @classmethod
    def keyword_score(
        cls,
        texts,
        keywords
    ):

        scores = []

        for text in texts.fillna("").astype(str):

            text = text.lower()

            hits = sum(
                1
                for word in keywords
                if word in text
            )

            scores.append(
                min(
                    hits / len(keywords),
                    1
                )
            )

        return pd.Series(
            scores,
            index=texts.index
        )

    @classmethod
    def semantic_score(
        cls,
        texts,
        topic
    ):
        """
        Uses cached document embeddings.
        Only the query is encoded.
        """

        EmbeddingCache.ensure_ready()

        query_embedding = EmbeddingEngine.encode(
            [topic]
        )[0]

        scores = EmbeddingEngine.similarity(
            query_embedding,
            EmbeddingCache.embeddings
        )

        return pd.Series(
            scores,
            index=texts.index
        )

    @classmethod
    def tfidf_score(
        cls,
        texts,
        topic
    ):

        corpus = list(
            texts.astype(str)
        )

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            corpus + [topic]
        )

        query_vector = matrix[-1]

        scores = cosine_similarity(
            query_vector,
            matrix[:-1]
        )[0]

        return pd.Series(
            scores,
            index=texts.index
        )

    @classmethod
    def hybrid_relevance(
        cls,
        text_series,
        topic
    ):

        keywords = cls.get_keywords(
            topic
        )

        keyword = cls.keyword_score(
            text_series,
            keywords
        )

        semantic = cls.semantic_score(
            text_series,
            topic
        )

        tfidf = cls.tfidf_score(
            text_series,
            topic
        )

        relevance = (

            semantic * 0.65

            +

            keyword * 0.20

            +

            tfidf * 0.15

        )

        return (
            relevance.clip(0, 1),
            keywords
        )

    @classmethod
    def keyword_relevance(
        cls,
        text_series,
        topic
    ):

        keywords = cls.get_keywords(
            topic
        )

        scores = cls.keyword_score(
            text_series,
            keywords
        )

        return (
            scores,
            keywords
        )
