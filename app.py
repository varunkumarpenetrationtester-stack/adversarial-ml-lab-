# -------- FORCE PATH FIX (DO NOT REMOVE) --------
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(ROOT_DIR, "model")

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)
# -----------------------------------------------

import streamlit as st
import pandas as pd

# DIRECT IMPORTS (PATH-SAFE)
from attack import poison_data, evade_text
from defense import sanitize_data, confidence_filter
from train import train_model
