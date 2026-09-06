"""
Unit tests për Module 1: Profiling.
Ekzekuto me: pytest tests/test_module1_profiling.py -v
"""

import sys
import os
import pandas as pd
import pytest

# Shto path-in e module1_profiling që të mund të importojmë profiler.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module1_profiling"))

from profiler import (
    infer_column_types,
    missing_value_report,
    cardinality_report,
    detect_suspicious_columns,
    detect_semantic_meaning,
    detect_mixed_type_columns,
    build_profiling_report,
)


@pytest.fixture
def sample_df():
    """Dataset i vogël testues me probleme të njohura."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "amount": [10.5, 20.0, None, 15.75],
        "email": ["a@test.com", "b@test.com", None, "d@test.com"],
        "category": ["A", "B", "A", "B"],
        "mixed_col": ["10", "twenty", "30", "40"],
    })


def test_infer_column_types(sample_df):
    types = infer_column_types(sample_df)
    assert types["id"] == "numeric"
    assert types["amount"] == "numeric"
    assert types["category"] == "categorical"


def test_missing_value_report(sample_df):
    report = missing_value_report(sample_df)
    assert report["amount"]["missing_count"] == 1
    assert report["email"]["missing_count"] == 1
    assert report["id"]["missing_count"] == 0
    assert report["amount"]["missing_pct"] == 25.0


def test_cardinality_report(sample_df):
    report = cardinality_report(sample_df)
    assert report["id"] == 4
    assert report["category"] == 2


def test_detect_suspicious_columns(sample_df):
    suspicious = detect_suspicious_columns(sample_df)
    assert "email" in suspicious
    assert "category" not in suspicious


def test_detect_semantic_meaning(sample_df):
    semantic = detect_semantic_meaning(sample_df)
    assert semantic["email"] == "email"
    assert semantic["id"] == "identifier"


def test_detect_mixed_type_columns(sample_df):
    mixed = detect_mixed_type_columns(sample_df)
    assert "mixed_col" in mixed


def test_build_profiling_report(sample_df):
    report = build_profiling_report(sample_df)
    assert report["n_rows"] == 4
    assert report["n_columns"] == 5
    assert "column_types" in report
    assert "missing_values" in report
    assert "semantic_meaning" in report
    assert "mixed_type_columns" in report


def test_no_missing_values_when_clean():
    """Test me dataset pa asnjë vlerë të munguar."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    report = missing_value_report(df)
    assert report["a"]["missing_count"] == 0
    assert report["b"]["missing_count"] == 0