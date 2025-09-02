# services/data/eda_preprocess.py
import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


# ---------- utils ----------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def is_binary_like(s: pd.Series) -> bool:
    vals = s.dropna().unique()
    if len(vals) == 2:
        return True
    lowered = pd.Series(vals).astype(str).str.lower().unique()
    return set(lowered).issubset({"yes","no","true","false","positive","negative","pos","neg","y","n","1","0"})


def guess_target(df: pd.DataFrame):
    common = [
        "Outcome","outcome","target","Target","label","Label","class","Class",
        "diabetes","Diabetes","has_diabetes","diabetic","Diabetic"
    ]
    for c in common:
        if c in df.columns:
            return c
    return None


# ---------- EDA ----------
def run_eda(df: pd.DataFrame, reports_dir: str, target_col: str = None):
    ensure_dir(reports_dir)

    # shape + dtypes
    dtypes = df.dtypes.astype(str).rename("dtype").reset_index().rename(columns={"index":"column"})
    dtypes.to_csv(os.path.join(reports_dir, "01_dtypes.csv"), index=False)

    # missing values
    miss = df.isna().sum().rename("missing_count").reset_index().rename(columns={"index":"column"})
    miss["missing_pct"] = (miss["missing_count"] / len(df) * 100).round(2)
    miss.to_csv(os.path.join(reports_dir, "02_missing_values.csv"), index=False)

    # numeric describe
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if num_cols:
        desc = df[num_cols].describe().T.reset_index().rename(columns={"index":"column"})
        desc.to_csv(os.path.join(reports_dir, "03_numeric_describe.csv"), index=False)

    # target distribution
    if target_col and target_col in df.columns:
        tgt = df[target_col].value_counts(dropna=False).rename_axis(target_col).reset_index(name="count")
        tgt["percent"] = (tgt["count"] / len(df) * 100).round(2)
        tgt.to_csv(os.path.join(reports_dir, "04_target_distribution.csv"), index=False)

    # simple histogram plots
    num_cols = num_cols[:6]  # limit
    for c in num_cols:
        plt.figure()
        df[c].hist(bins=30)
        plt.title(f"Histogram - {c}")
        plt.savefig(os.path.join(reports_dir, f"hist_{c}.png"))
        plt.close()


# ---------- preprocessing ----------
def preprocess(df: pd.DataFrame, outdir: str, target_col: str = None):
    ensure_dir(outdir)

    df_clean = df.copy()

    # drop duplicates
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)

    # numeric + categorical
    num_cols = [c for c in df_clean.columns if pd.api.types.is_numeric_dtype(df_clean[c]) and c != target_col]
    obj_cols = [c for c in df_clean.columns if df_clean[c].dtype == "object" and c != target_col]

    # impute missing
    for c in num_cols:
        df_clean[c] = df_clean[c].fillna(df_clean[c].median())
    for c in obj_cols:
        df_clean[c] = df_clean[c].fillna(df_clean[c].mode()[0] if not df_clean[c].mode().empty else "Unknown")

    # --- human-readable version
    readable_path = os.path.join(outdir, "diabetes_preprocessed_readable.csv")
    df_clean.to_csv(readable_path, index=False)

    # --- numeric ML-ready version
    df_encoded = pd.get_dummies(df_clean, columns=obj_cols, drop_first=False)
    if num_cols:
        scaler = StandardScaler()
        df_encoded[num_cols] = scaler.fit_transform(df_encoded[num_cols])
    numeric_path = os.path.join(outdir, "diabetes_preprocessed_numeric.csv")
    df_encoded.to_csv(numeric_path, index=False)

    return readable_path, numeric_path


# ---------- main ----------
def main():
    parser = argparse.ArgumentParser(description="EDA + Preprocess diabetes dataset")
    parser.add_argument("--input", required=True, help="Path to raw CSV")
    parser.add_argument("--outdir", default="services/data/processed", help="Where to save processed CSVs")
    parser.add_argument("--reports", default="services/data/reports", help="Where to save EDA reports")
    parser.add_argument("--target", default=None, help="Target column name (optional)")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    target_col = args.target or guess_target(df)
    print(f"[i] Target column: {target_col}")

    run_eda(df, reports_dir=args.reports, target_col=target_col)
    readable_path, numeric_path = preprocess(df, outdir=args.outdir, target_col=target_col)

    print(f"[✓] Human-readable CSV: {readable_path}")
    print(f"[✓] Numeric ML-ready CSV: {numeric_path}")


if __name__ == "__main__":
    main()
