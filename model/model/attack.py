import numpy as np
import pandas as pd

def poison_data(df, poison_rate=0.3):
    """
    Simulates data poisoning by flipping labels.
    """
    poisoned = df.copy()
    n_poison = int(len(df) * poison_rate)
    idx = np.random.choice(df.index, n_poison, replace=False)
    poisoned.loc[idx, "label"] = 1 - poisoned.loc[idx, "label"]
    return poisoned

def evade_text(text):
    """
    Simple evasion attack by modifying characters.
    """
    return text.replace("e", "3").replace("o", "0").replace("a", "@")

