import streamlit as st
import pandas as pd
import numpy as np
import joblib, re

MODEL_PATH = "models/lgbm.pkl"
NUMERIC_COLS = ['energy_100g','fat_100g','saturated-fat_100g','carbohydrates_100g',
                'sugars_100g','proteins_100g','salt_100g','fiber_100g']

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

def main():
    st.title("Nutri‑Score Predictor")
    st.write("Enter nutrient values per 100 g:")

    inputs = {}
    for col in NUMERIC_COLS:
        inputs[col] = st.number_input(col.replace('_',' ').title(), 0.0, 100.0, step=0.1)

    if st.button("Predict"):
        model = load_model()
        X = pd.DataFrame([inputs])
        score = float(model.predict(X)[0])
        st.success(f"Predicted nutrition score: **{score:.1f}**")
        label = np.select(
            [score <= -1, score <= 2, score <= 10, score <= 18],
            ['A','B','C','D'],
            default='E'
        )
        st.write(f"Corresponding Nutri‑Score label: **{label}**")

if __name__ == "__main__":
    main()