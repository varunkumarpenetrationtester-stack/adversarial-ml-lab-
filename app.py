import streamlit as st
import pandas as pd
import os

from train import train_model
from attack import poison_data, evade_text
from defense import sanitize_data, confidence_filter

st.set_page_config(page_title="Adversarial ML Lab", layout="centered")

st.title("🛡️ Adversarial ML Attack & Defense Lab")
st.write("App loaded successfully")

# Check files
st.write("Files in root:", os.listdir("."))

DATA_PATH = os.path.join("data", "dataset.csv")

# Load dataset safely
try:
    df = pd.read_csv(DATA_PATH)
    st.success("Dataset loaded")
except Exception as e:
    st.error("Dataset load failed")
    st.code(str(e))
    st.stop()

mode = st.selectbox("Training Mode", ["Clean", "Poisoned"])

if mode == "Poisoned":
    df = poison_data(df)

df = sanitize_data(df)

predict_proba = train_model(df["text"], df["label"])

user_text = st.text_input("Enter text", "free money now")
use_evasion = st.checkbox("Apply Evasion Attack")

if use_evasion:
    user_text = evade_text(user_text)

if st.button("Analyze"):
    probs = predict_proba(user_text)
    confidence = max(probs)
    prediction = 1 if probs[1] > 0.5 else 0

    if prediction == 1:
        st.error("🚨 Malicious Content")
    else:
        st.success("✅ Benign Content")

    st.write("Confidence:", round(confidence, 2))
    st.write(confidence_filter(confidence))
