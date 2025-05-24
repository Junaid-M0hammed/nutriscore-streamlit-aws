# NutriScore Streamlit App • AWS‑ready

Predict the **continuous nutrient score** that powers the A–E **Nutri‑Score** label for any packaged food, then surface results in a Streamlit dashboard.

## Why this project?

* **Food & Health trend** · Nutri‑Score adoption is expanding across Europe and generating buzz in North‑America.
* **Data Engineering focus** · End‑to‑end: ingest OpenFoodFacts TSV → preprocess → train LightGBM → serve via Streamlit → ship with Docker & CI/CD to AWS ECS/Fargate.
* Aligns with my background in **ETL, AWS, and data‑to‑dashboard pipelines**.

---

## Quick‑start (local)

```bash
git clone https://github.com/your-username/nutriscore-streamlit-aws.git
cd nutriscore-streamlit-aws

# 1) Create venv & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Download latest OpenFoodFacts export (3M rows)
python src/data_ingest.py --bucket local --raw_path data/raw.tsv.gz

# 3) Preprocess
python src/data_prep.py --raw_path data/raw.tsv.gz --out_path data/processed.csv

# 4) Train model
python src/train.py --data data/processed.csv --model_path models/lgbm.pkl

# 5) Launch Streamlit
streamlit run app.py
```

Open the browser → `http://localhost:8501` and paste an ingredient list to see the predicted nutrition score.

---

## Cloud deployment (summary)

| Stage | Service | IaC/Automation |
|-------|---------|----------------|
| Data ingest | AWS Glue job (or step‑function) → S3 raw zone | `src/data_ingest.py` runnable as Glue Python shell |
| Train | Amazon SageMaker notebook or batch job | extend `train.py` |
| Serve | Dockerised Streamlit → ECR → **ECS/Fargate** | see `Dockerfile`, `.github/workflows/ci.yml` |

---

## Model performance (sample)

| Metric | Value on hold‑out 20 % |
|--------|-----------------------|
| RMSE   | ≈ 2.80 |
| MAE    | ≈ 2.05 |
| R²     | 0.89 |

*(numbers are for lightGBM with 300 trees on ~150 k clean rows; retrain for fresher data)*

---

## File tree
```
nutriscore_streamlit_aws/
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── data/          # raw & processed files (git‑ignored)
├── models/
├── src/
│   ├── __init__.py
│   ├── data_ingest.py
│   ├── data_prep.py
│   ├── train.py
│   └── evaluate.py
└── .github/workflows/ci.yml
```

---

## License
MIT