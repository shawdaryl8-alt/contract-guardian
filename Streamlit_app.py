# ========================================
# Contract Guardian – Red Flag Detector
# By YOU – 2025
# ========================================

import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import re

st.set_page_config(page_title="Contract Guardian", layout="wide", page_icon="🔍")

st.title("🔍 Contract Guardian")
st.markdown("**Upload a contract PDF/photo or paste text → instantly see every hidden trap in plain English.**")

# ----- Red Flags Database -----
RED_FLAGS = {
    "One-Sided Control": {
        "patterns": [r"\bsole discretion\b", r"\bat (our|their) sole discretion\b", r"\breserves? the right\b", r"\bmay (modify|change|amend|terminate)\b", r"\bwithout (prior )?notice\b", r"\bat any time\b"],
        "explanation": "They can change the deal anytime — even after you sign.",
        "risk": "high"
    },
    "Auto-Renewal Trap": {
        "patterns": [r"\bauto[-\s]?renew\b", r"\bautomatic renewal\b", r"\bnon[-\s]?cancellable\b", r"\bearly termination fee\b"],
        "explanation": "You’re locked in and it’s hard or expensive to get out.",
        "risk": "high"
    },
    "No Liability": {
        "patterns": [r"\bhold harmless\b", r"\bindemnify\b", r"\bno liability\b", r"\blimitation of liability\b", r"\bwaive.*claims?\b"],
        "explanation": "If they mess up, you can’t sue — even if it’s their fault.",
        "risk": "critical"
    },
    "Forced Arbitration": {
        "patterns": [r"\bbinding arbitration\b", r"\bclass action waiver\b", r"\bwaive.*jury\b"],
        "explanation": "No real court, no class action. You fight alone.",
        "risk": "critical"
    },
    "Hidden Fees": {
        "patterns": [r"\badditional fees?\b", r"\bvariable.*rate\b", r"\bprice.*increase\b"],
        "explanation": "They can raise prices or add surprise charges later.",
        "risk": "high"
    },
    "No Warranty": {
        "patterns": [r"\bas[- ]?is\b", r"\bwithout warranty\b", r"\bno guarantee\b"],
        "explanation": "If it breaks or doesn’t work — you’re on your own.",
        "risk": "medium"
    },
    "Vague = They Win": {
        "patterns": [r"\breasonable\b", r"\bas (we|they) (deem|determine)\b", r"\bin (our|their) judgment\b"],
        "explanation": "They decide what “reasonable” means. Guess who wins?",
        "risk": "medium"
    }
}

tab1, tab2 = st.tabs(["Upload PDF/Image", "Paste Text"])
extracted_text = ""

with tab1:
    uploaded = st.file_uploader("PDF, PNG, JPG", type=["pdf","png","jpg","jpeg"])
    if uploaded:
        with st.spinner("Reading with OCR…"):
            bytes_data = uploaded.read()
            if uploaded.type == "application/pdf":
                images = convert_from_bytes(bytes_data, dpi=200)
                for img in images:
                    extracted_text +=
