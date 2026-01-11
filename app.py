# ---- PATH FIX (CRITICAL FOR STREAMLIT CLOUD) ----
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ---- STANDARD IMPORTS ----
import streamlit as st
import pandas as pd

# ---- LOCAL MODULE IMPORTS ----
from model.train import train_model
from model.attack import poison_data, evade_text
from model.defense import sanitize_data, confidence_filter

# ---- STREAMLIT CONFIG ----
st.set_page_config(
    page_title="Adversarial ML Attack & Defense Lab",
    layout="centered"
)

st.title("🛡️ Adversarial ML Attack & Defense Lab")
st.caption("Demonstrating adversarial attacks against ML-based security systems")

# ---- LOAD DATASET ----
DATA_PATH = os.path.join("data", "dataset.csv")

df = pd.read_csv(DATA_PATH)

# ---- TRAINING MODE ----
mode = st.selectbox(
    "Select Training Mode",
    ["Clean Training", "Poisoned Training"]
)

if mode == "Poisoned Training":
    df = poison_data(df)

# ---- DEFENSIVE SANITIZATION ----
df = sanitize_data(df)

# ---- TRAIN MODEL ----
model, vectorizer = train_model(df["text"], df["label"])

# ---- USER INPUT ----
user_text = st.text_input(
    "Enter text to analyze",
    value="free money now"
)

apply_evasion = st.checkbox("Apply Evasion Attack")

if apply_evasion:
    user_text = evade_text(user_text)

# ---- ANALYSIS ----
if st.button("Analyze"):
    X_test = vectorizer.transform([user_text])
    probabilities = model.predict_proba(X_test)[0]
    confidence = max(probabilities)
    prediction = model.predict(X_test)[0]

    st.subheader("Analysis Result")

    if prediction == 1:
        st.error("🚨 Malicious Content Detected")
    else:
        st.success("✅ Benign Content")

    st.write("**Confidence:**", round(confidence, 2))
    st.write(confidence_filter(confidence))
