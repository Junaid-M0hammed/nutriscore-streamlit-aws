import pandas as pd
import argparse
from pathlib import Path

NUMERIC_COLS = [
    'energy_100g','fat_100g','saturated-fat_100g','carbohydrates_100g',
    'sugars_100g','proteins_100g','salt_100g','fiber_100g'
]
TARGET = 'nutrition_score_fr_100g'

def clean_df(df):
    df = df[NUMERIC_COLS + [TARGET]].dropna()
    return df

def main(raw_path, out_path):
    df = pd.read_csv(raw_path, sep='\t', low_memory=False)
    df = clean_df(df)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved processed: {out_path} rows={len(df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_path', required=True)
    parser.add_argument('--out_path', required=True)
    args = parser.parse_args()
    main(args.raw_path, args.out_path)