"""File for vectorize the sencente for the english model."""
import numpy as np
from sklearn.base import TransformerMixin


def sentence_to_vec(sentence, model):
    """Transform the sentence in vector.

    Args:
        sentence (str): phrase to vectorize
        model (model): The model for vectorize.

    Returns: float: phrase vectorized
    """
    words = sentence.lower().split()
    vectors = [model[w] for w in words if w in model]
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)


class GloVeVectorizer(TransformerMixin):
    """This class is used to convert a list of sentences into their respective vector representations using the pretrained glove word embeddings.

    Args:
        TransformerMixin (TransformerMixin): The transformer for the model
    """

    def __init__(self, model):
        """Init the model and the size of vector.

        Args:
            model (_type_): _description_
        """
        self.model = model
        self.size = model.vector_size

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return np.array([sentence_to_vec(sentence, self.model) for sentence in x])
