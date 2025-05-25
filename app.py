import streamlit as st
import pandas as pd
import numpy as np
import joblib

MODEL_PATH = "models/lgbm.pkl"
NUMERIC_COLS = [
    'energy_100g','fat_100g','saturated-fat_100g','carbohydrates_100g',
    'sugars_100g','proteins_100g','salt_100g','fiber_100g'
]

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

def get_label(score):
    if score <= -1: return 'A', '🟩'
    elif score <= 2: return 'B', '🟨'
    elif score <= 10: return 'C', '🟧'
    elif score <= 18: return 'D', '🟥'
    else: return 'E', '⬛'

def main():
    st.set_page_config("Nutri‑Score Predictor", layout="wide")

    # Load and apply CSS
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("🥗 Nutri‑Score Predictor")
    st.markdown("### 🔍 Enter nutrient values per **100g** below:")
    st.divider()

    inputs = {}
    col1, col2 = st.columns(2)
    for i, col in enumerate(NUMERIC_COLS):
        with (col1 if i % 2 == 0 else col2):
            label = col.replace('_', ' ').title()
            inputs[col] = st.number_input(label, min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Predict"):
        model = load_model()
        X = pd.DataFrame([inputs])
        score = float(model.predict(X)[0])
        grade, emoji = get_label(score)

        st.success(f"✅ Predicted Nutri‑Score: **{score:.1f}**")

        st.markdown("## 🧾 Nutri-Score Details")
        st.markdown(f"<div class='badge'>{emoji} {grade}</div>", unsafe_allow_html=True)

        st.progress(min(max(score / 40, 0.0), 1.0))

        with st.expander("ℹ️ What does this grade mean?"):
            st.markdown("""
            - 🟩 **A**: Excellent nutritional quality  
            - 🟨 **B**: Good  
            - 🟧 **C**: Average  
            - 🟥 **D**: Poor  
            - ⬛ **E**: Very poor nutritional quality  
            """)

    # Footer
    st.markdown("""
    <hr style="margin-top: 3rem;">
    <div class="footer">
        Made with ❤️ by <strong>Junaid Mohammed</strong>  
        • <a href="https://github.com/Junaid-M0hammed" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
