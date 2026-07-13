from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class EmbeddingEngine:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading Sentence Transformer...")

            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return cls._model

    @classmethod
    def encode(cls, texts):

        model = cls.get_model()

        return model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    @classmethod
    def similarity(
        cls,
        query_embedding,
        document_embeddings,
    ):

        return cosine_similarity(
            [query_embedding],
            document_embeddings,
        )[0]

    @classmethod
    def rank(
        cls,
        query,
        documents,
    ):

        query_embedding = cls.encode([query])[0]

        document_embeddings = cls.encode(documents)

        scores = cls.similarity(
            query_embedding,
            document_embeddings,
        )

        return scores
