import numpy as np

def train_model(texts, labels):
    """
    Simple probabilistic classifier without sklearn.
    """
    keywords = ["free", "win", "offer", "cash", "urgent", "click", "money"]

    def predict_proba(text):
        score = 0
        for k in keywords:
            if k in text.lower():
                score += 1
        prob = min(score / len(keywords), 1.0)
        return [1 - prob, prob]

    return predict_proba
