# Automated Data Cleaning & Validation System

Backend "data gatekeeper" — një pipeline i automatizuar që profilon, pastron dhe validon
çdo dataset para se të përdoret. Projekt individual (solo) për CadetX Virtual Work Experience,
domain: **Financa / Fintech**.

## Pipeline Flow

```
Raw Data → [Module 1: Profile] → profiling_report.json
        → [Module 2: Clean]   → cleaned_data.csv + cleaning_log.json
        → [Module 3: Validate]→ validation_report.json
        → [Module 4: Automate]→ end-to-end pipeline (CLI + Docker)
```

## Struktura e Repos

```
data-quality-pipeline/
├── data/
│   ├── raw/              # dataset origjinal (raw)
│   └── processed/        # output-et e pastruara
├── module1_profiling/    # metadata + profiling engine
├── module2_cleaning/     # imputation, dedup, normalization
├── module3_validation/   # rule-based + AI anomaly detection
├── module4_pipeline/     # orchestrator, CLI, Docker
├── docs/                 # dokumentim & prezantime per modul
├── tests/                # pytest unit & integration tests
├── requirements.txt
└── README.md
```

## Domain & Dataset

**Domain:** Financa (transaksione bankare / kredi)
**Dataset:** _[Për t'u plotësuar — p.sh. Kaggle "Credit Card Fraud Detection" ose "Loan Default Dataset"]_
**Arsyeja:** Dataset-et financiare kanë probleme reale të cilësisë (missing values,
duplicate transaksione, kolona PII si emra/IBAN, dhe rast natyror përdorimi për
anomaly detection — fraud).

## Progres Javor (12 javë)

| Javë | Modul | Fokusi |
|---|---|---|
| 0 | Setup | Domain, dataset, repo, struktura |
| 1-3 | Modul 1 | Profiling & Metadata Intelligence |
| 4-6 | Modul 2 | Cleaning & Transformation |
| 7-9 | Modul 3 | AI Validation & Anomaly Detection |
| 10-12 | Modul 4 | Integration, Orchestration, Production |

## Si të runohet (do plotësohet gjatë projektit)

```bash
pip install -r requirements.txt
python module4_pipeline/pipeline.py --input data/raw/dataset.csv --output data/processed/
```

## Autor

Projekt solo — CadetX Virtual Work Experience Programme.
