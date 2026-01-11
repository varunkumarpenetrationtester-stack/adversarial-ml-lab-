import streamlit as st
import pandas as pd
import os

from train import train_model
from attack import poison_data, evade_text
from defense import sanitize_data, confidence_filter

st.set_page_config(page_title="Adversarial ML Lab", layout="centered")

st.title("🛡️ Adversarial ML Attack & Defense Lab")

DATA_PATH = os.path.join("data", "dataset.csv")

df = pd.read_csv(DATA_PATH)

mode = st.selectbox("Training Mode", ["Clean", "Poisoned"])

if mode == "Poisoned":
    df = poison_data(df)

df = sanitize_data(df)

predict_proba = train_model(df["text"], df["label"])

text = st.text_input("Enter text", "free money now")

if st.button("Analyze"):
    probs = predict_proba(text)
    confidence = max(probs)
    prediction = 1 if probs[1] > 0.5 else 0

    if prediction:
        st.error("🚨 Malicious")
    else:
        st.success("✅ Benign")

    st.write("Confidence:", round(confidence, 2))
    st.write(confidence_filter(confidence))
