import numpy as np

def poison_data(df, poison_rate=0.3):
    poisoned = df.copy()
    n = int(len(df) * poison_rate)
    idx = np.random.choice(df.index, n, replace=False)
    poisoned.loc[idx, "label"] = 1 - poisoned.loc[idx, "label"]
    return poisoned

def evade_text(text):
    return (
        text.replace("e", "3")
            .replace("o", "0")
            .replace("a", "@")
    )
