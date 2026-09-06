"""
Module 1: Advanced Data Profiling & Metadata Intelligence
Output: profiling_report.json

Fillestar/skeleton — plotësohet gjatë Javëve 1-3.
"""

import json
import pandas as pd
import numpy as np
import re
from datetime import datetime


def load_dataset(path: str) -> pd.DataFrame:
    """Ngarkon dataset-in nga CSV."""
    return pd.read_csv(path)


def infer_column_types(df: pd.DataFrame) -> dict:
    """
    Infero tipin e çdo kolone: numeric, categorical, datetime, id, mixed.
    TODO: shto detektim semantik (email, phone, IBAN, name) — Javë 1.
    """
    types = {}
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            types[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            types[col] = "datetime"
        else:
            types[col] = "categorical"
    return types



def detect_semantic_meaning(df: pd.DataFrame) -> dict:
    """
    Zbulon kuptimin semantik të kolonës bazuar në emër dhe mostër vlerash:
    email, date, id, name, ose 'unknown' nëse s'përputhet asnjë pattern.
    """
    semantic = {}
    for col in df.columns:
        col_lower = col.lower()
        sample = df[col].dropna().astype(str).head(20)

        if "email" in col_lower:
            semantic[col] = "email"
        elif "date" in col_lower or "time" in col_lower:
            semantic[col] = "date/time"
        elif col_lower.endswith("id") or col_lower == "id":
            semantic[col] = "identifier"
        elif "name" in col_lower:
            semantic[col] = "name"
        elif sample.str.match(r"^[\w\.-]+@[\w\.-]+\.\w+$").any():
            semantic[col] = "email"
        elif sample.str.match(r"^\d{4}-\d{2}-\d{2}").any():
            semantic[col] = "date/time"
        else:
            semantic[col] = "unknown"
    return semantic


def detect_mixed_type_columns(df: pd.DataFrame) -> list:
    """
    Zbulon kolona që kanë tipe të përziera vlerash brenda vetes
    (p.sh. disa rreshta numra, disa tekst brenda kolonës object).
    """
    mixed = []
    for col in df.columns:
        if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
            types_found = df[col].dropna().apply(lambda x: type(x).__name__).unique()
            if len(types_found) > 1:
                mixed.append(col)
                continue
            sample = df[col].dropna().astype(str)
            is_numeric_like = sample.str.match(r"^-?\d+\.?\d*$")
            if is_numeric_like.any() and not is_numeric_like.all():
                mixed.append(col)
    return mixed

def missing_value_report(df: pd.DataFrame) -> dict:
    """Raporti i vlerave që mungojnë për çdo kolonë."""
    missing = df.isnull().sum()
    total = len(df)
    return {
        col: {
            "missing_count": int(missing[col]),
            "missing_pct": round(float(missing[col]) / total * 100, 2)
        }
        for col in df.columns
    }


def cardinality_report(df: pd.DataFrame) -> dict:
    """Numri i vlerave unike për çdo kolonë (ndihmon me identifiku ID kolona)."""
    return {col: int(df[col].nunique()) for col in df.columns}


def detect_suspicious_columns(df: pd.DataFrame) -> list:
    """
    Zbulon kolona potencialisht PII ose me probleme.
    TODO: shto regex për email, phone, IBAN — Javë 2-3.
    """
    suspicious = []
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in ["name", "email", "phone", "iban", "ssn", "address"]):
            suspicious.append(col)
    return suspicious


def build_profiling_report(df: pd.DataFrame) -> dict:
    """Ndërton profiling_report.json të plotë."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "column_types": infer_column_types(df),
        "semantic_meaning": detect_semantic_meaning(df),
        "mixed_type_columns": detect_mixed_type_columns(df),
        "missing_values": missing_value_report(df),
        "cardinality": cardinality_report(df),
        "suspicious_columns": detect_suspicious_columns(df),
    }
    return report


def save_report(report: dict, output_path: str):
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

import matplotlib
matplotlib.use("Agg")  # backend pa GUI, ruan direkt në file
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_missing_heatmap(df: pd.DataFrame, output_path: str):
    """Heatmap i vlerave që mungojnë (bosh nëse s'ka missing values)."""
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Values Heatmap")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str):
    """Heatmap i korrelacionit ndërmjet kolonave numerike."""
    numeric_df = df.select_dtypes(include=[np.number])
    plt.figure(figsize=(14, 10))
    corr = numeric_df.corr()
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_outlier_distribution(df: pd.DataFrame, column: str, output_path: str):
    """Boxplot për me identifiku outliers në një kolonë specifike."""
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df[column])
    plt.title(f"Outlier Distribution: {column}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_class_distribution(df: pd.DataFrame, output_path: str):
    """Distribucioni i target kolonës (Class: fraud vs jo-fraud)."""
    plt.figure(figsize=(6, 5))
    sns.countplot(x="Class", data=df)
    plt.title("Class Distribution (0 = Normal, 1 = Fraud)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    df = load_dataset("../data/raw/creditcard.csv")
    print(f"Dataset i ngarkuar: {df.shape[0]} rreshta, {df.shape[1]} kolona")

    report = build_profiling_report(df)
    save_report(report, "../data/processed/profiling_report.json")
    print("Profiling report u ruajt te data/processed/profiling_report.json")

    os.makedirs("../data/processed/visuals", exist_ok=True)

    plot_missing_heatmap(df, "../data/processed/visuals/missing_heatmap.png")
    print("Missing heatmap u ruajt.")

    plot_correlation_heatmap(df, "../data/processed/visuals/correlation_heatmap.png")
    print("Correlation heatmap u ruajt.")

    plot_outlier_distribution(df, "Amount", "../data/processed/visuals/amount_outliers.png")
    print("Amount outlier distribution u ruajt.")

    plot_class_distribution(df, "../data/processed/visuals/class_distribution.png")
    print("Class distribution u ruajt.")

    print("\nGjithçka u kompletua! Kontrollo data/processed/visuals/")