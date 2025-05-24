import pandas as pd
import argparse, joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

TARGET = 'nutrition_score_fr_100g'

def main(model_path, data_path):
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    preds = model.predict(X)
    print("Full‑data metrics")
    print("RMSE", mean_squared_error(y, preds, squared=False))
    print("MAE", mean_absolute_error(y, preds))
    print("R² ", r2_score(y, preds))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True)
    parser.add_argument('--data_path', required=True)
    args = parser.parse_args()
    main(args.model_path, args.data_path)