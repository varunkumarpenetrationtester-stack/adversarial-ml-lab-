import streamlit as st
import pandas as pd

from model.train import train_model
from model.attack import poison_data, evade_text
from model.defense import sanitize_data, confidence_filter

st.set_page_config(page_title="Adversarial ML Lab", layout="centered")

st.title("🛡️ Adversarial ML Attack & Defense Lab")

df = pd.read_csv("data/dataset.csv")

mode = st.selectbox("Training Mode", ["Clean", "Poisoned"])

if mode == "Poisoned":
    df = poison_data(df)

df = sanitize_data(df)

model, vectorizer = train_model(df["text"], df["label"])

text = st.text_input("Enter text", "free money now")
use_evasion = st.checkbox("Apply Evasion Attack")

if use_evasion:
    text = evade_text(text)

if st.button("Analyze"):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0].max()
    pred = model.predict(X)[0]

    st.write("Prediction:", "🚨 Malicious" if pred == 1 else "✅ Benign")
    st.write("Confidence:", round(prob, 2))
    st.write(confidence_filter(prob))
