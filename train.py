def train_model(texts, labels):
    keywords = [
        "free", "win", "offer", "cash",
        "urgent", "click", "money", "prize"
    ]

    def predict_proba(text):
        score = 0
        t = text.lower()
        for k in keywords:
            if k in t:
                score += 1
        p = min(score / len(keywords), 1.0)
        return [1 - p, p]  # [benign, malicious]

    return predict_proba
