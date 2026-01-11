import streamlit as st
import pandas as pd
import os
import numpy as np

# -----------------------------
# ATTACK LOGIC (INLINE)
# -----------------------------
def poison_data(df, poison_rate=0.3):
    poisoned = df.copy()
    n = int(len(df) * poison_rate)
    idx = poisoned.sample(n).index
    poisoned.loc[idx, "label"] = 1 - poisoned.loc[idx, "label"]
    return poisoned

def evade_text(text):
    return text.replace("e", "3").replace("o", "0").replace("a", "@")

# -----------------------------
# DEFENSE LOGIC (INLINE)
# -----------------------------
def sanitize_data(df):
    return df.drop_duplicates().reset_index(drop=True)

def confidence_filter(confidence):
    if confidence < 0.6:
        return "⚠️ Low confidence – Manual review recommended"
    return "✅ High confidence prediction"

# -----------------------------
# MODEL LOGIC (INLINE, NO SKLEARN)
# -----------------------------
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

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Adversarial ML Lab", layout="centered")
st.title("🛡️ Adversarial ML Attack & Defense Lab")

DATA_PATH = os.path.join("data", "dataset.csv")

# Load dataset
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error("Dataset not found. Make sure data/dataset.csv exists.")
    st.stop()

mode = st.selectbox("Training Mode", ["Clean", "Poisoned"])

if mode == "Poisoned":
    df = poison_data(df)

df = sanitize_data(df)

predict_proba = train_model(df["text"], df["label"])

user_text = st.text_input("Enter text to analyze", "free money now")
use_evasion = st.checkbox("Apply Evasion Attack")

if use_evasion:
    user_text = evade_text(user_text)

if st.button("Analyze"):
    probs = predict_proba(user_text)
    confidence = max(probs)
    prediction = 1 if probs[1] > 0.5 else 0

    if prediction:
        st.error("🚨 Malicious Content Detected")
    else:
        st.success("✅ Benign Content")

    st.write("Confidence:", round(confidence, 2))
    st.write(confidence_filter(confidence))
