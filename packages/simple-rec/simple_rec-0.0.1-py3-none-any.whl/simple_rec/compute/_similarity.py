import numpy as np


class _SimilaritySearchMixin:
    """Mixin for similarity search between vectors.

    """

    def _cosine_similarity(self,
                           query: np.ndarray,
                           keys: np.ndarray,
                           eps: float = 1e-8):
        """Computes similarities between query and keys.

        """
        # normalize to unit length
        query = query / (eps + np.linalg.norm(query))
        keys = keys / (eps + np.linalg.norm(keys, axis=1)[:, None])

        # compute cosine similarity and sort in descending order
        similarities = np.dot(keys, query)
        permutation = np.argsort(similarities)[::-1]
        similarities = similarities[permutation]

        return permutation, similarities
