# Module 1: Advanced Data Profiling & Metadata Intelligence

## Purpose
Understand the structure and quality of the dataset before any cleaning or modeling
takes place — by identifying column types, missing values, correlations, and
potentially sensitive (PII) columns.

## Dataset
**Source:** Credit Card Fraud Detection ([Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud))
**Size:** 284,807 rows, 31 columns
**Domain:** Finance — credit card transactions, target column: `Class` (0 = normal, 1 = fraud)

## What was built

### 1. Metadata Extraction Engine
`infer_column_types()` classifies each column as `numeric`, `datetime`, or
`categorical` based on its pandas dtype.

### 2. Profiling Engine
- `missing_value_report()` — count and percentage of missing values per column
- `cardinality_report()` — number of unique values per column (helps identify IDs/categories)
- `detect_suspicious_columns()` — scans column names for PII-related keywords
  (name, email, phone, iban, ssn, address)

### 3. Visualizations
Automatically generated in `data/processed/visuals/`:
- `missing_heatmap.png` — visual map of missing values
- `correlation_heatmap.png` — correlation between all 31 numeric columns
- `amount_outliers.png` — boxplot of the `Amount` column to spot outliers
- `class_distribution.png` — distribution of the target column `Class`

### 4. Output
`profiling_report.json` — a structured JSON report containing all findings above,
ready to be consumed by Module 2 (Cleaning).

## Key findings
- The dataset has no explicitly named PII columns (columns V1-V28 are PCA-transformed
  and already anonymized by the original source)
- The dataset is highly imbalanced (see `class_distribution.png`) — fraud (Class = 1)
  represents only a small fraction of the data, which will directly shape the strategy
  for Module 3 (anomaly detection)

## How to run
```bash
cd module1_profiling
python profiler.py
```

## Next steps
The output (`profiling_report.json`) will be used as input for Module 2
(Cleaning & Transformation).