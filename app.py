import streamlit as st
import pandas as pd
import os

from model.train import train_model
from model.attack import poison_data, evade_text
from model.defense import sanitize_data, confidence_filter

st.set_page_config(page_title="Adversarial ML Lab", layout="centered")

st.title("🛡️ Adversarial ML Attack & Defense Lab")
st.caption("Cloud-safe adversarial ML demonstration")

# Load dataset
DATA_PATH = os.path.join("data", "dataset.csv")
df = pd.read_csv(DATA_PATH)

# Training mode
mode = st.selectbox(
    "Select Training Mode",
    ["Clean Training", "Poisoned Training"]
)

if mode == "Poisoned Training":
    df = poison_data(df)

# Defense: sanitize data
df = sanitize_data(df)

# Train model (returns prediction function)
predict_proba = train_model(df["text"], df["label"])

# User input
user_text = st.text_input(
    "Enter text to analyze",
    value="free money now"
)

apply_evasion = st.checkbox("Apply Evasion Attack")

if apply_evasion:
    user_text = evade_text(user_text)

# Analyze
if st.button("Analyze"):
    probs = predict_proba(user_text)
    confidence = max(probs)
    prediction = 1 if probs[1] > 0.5 else 0

    st.subheader("Result")

    if prediction == 1:
        st.error("🚨 Malicious Content Detected")
    else:
        st.success("✅ Benign Content")

    st.write("**Confidence:**", round(confidence, 2))
    st.write(confidence_filter(confidence))
