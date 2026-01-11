import streamlit as st
import pandas as pd

from model.train import train_model
from model.attack import poison_data, evade_text
from model.defense import sanitize_data, confidence_filter

st.set_page_config(page_title="Adversarial ML Lab", layout="centered")

st.title("🛡️ Adversarial ML Attack & Defense Lab")
st.caption("Demonstrating how ML security systems fail — and how to defend them")

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Select training mode
mode = st.selectbox(
    "Select Training Scenario",
    ["Clean Training", "Poisoned Training"]
)

# Apply poisoning if selected
if mode == "Poisoned Training":
    df = poison_data(df)

# Apply basic defense
df = sanitize_data(df)

# Train model
model, vectorizer = train_model(df["text"], df["label"])

# User input
user_input = st.text_input(
    "Enter text to analyze",
    "free money now"
)

# Optional evasion attack
attack_toggle = st.checkbox("Apply Evasion Attack")

if attack_toggle:
    user_input = evade_text(user_input)

# Analyze button
if st.button("Analyze"):
    X_test = vectorizer.transform([user_input])
    probabilities = model.predict_proba(X_test)[0]
    confidence = max(probabilities)
    prediction = model.predict(X_test)[0]

    st.subheader("Result")
    st.write("Prediction:", "🚨 Malicious" if prediction == 1 else "✅ Benign")
    st.write("Confidence:", round(confidence, 2))
    st.write(confidence_filter(confidence))
