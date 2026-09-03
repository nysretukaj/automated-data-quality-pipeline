"""
Module 1: Advanced Data Profiling & Metadata Intelligence
Output: profiling_report.json

Fillestar/skeleton — plotësohet gjatë Javëve 1-3.
"""

import json
import pandas as pd
import numpy as np
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
        "missing_values": missing_value_report(df),
        "cardinality": cardinality_report(df),
        "suspicious_columns": detect_suspicious_columns(df),
    }
    return report


def save_report(report: dict, output_path: str):
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    df = load_dataset("../data/raw/creditcard.csv")
    print(f"Dataset i ngarkuar: {df.shape[0]} rreshta, {df.shape[1]} kolona")
    
    report = build_profiling_report(df)
    save_report(report, "../data/processed/profiling_report.json")
    
    print("Profiling report u ruajt te data/processed/profiling_report.json")
    print(f"Kolona të dyshimta (PII): {report['suspicious_columns']}")
