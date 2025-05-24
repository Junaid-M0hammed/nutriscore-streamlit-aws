import pandas as pd
import argparse, joblib
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error

TARGET = 'nutrition_score_fr_100g'

def main(data, model_path):
    df = pd.read_csv(data)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2,
                                                      random_state=42)
    model = LGBMRegressor(n_estimators=300, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    rmse = mean_squared_error(y_val, preds, squared=False)
    print(f"RMSE: {rmse:.3f}")
    joblib.dump(model, model_path)
    print(f"Saved model → {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--model_path', required=True)
    args = parser.parse_args()
    main(args.data, args.model_path)