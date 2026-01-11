from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def train_model(texts, labels):
    """
    Trains a simple ML classifier for security text detection.
    """
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=200)
    model.fit(X, labels)

    return model, vectorizer
