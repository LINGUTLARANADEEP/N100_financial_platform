# N100 Financial Platform – ETL Pipeline Project

## Project Overview

The N100 Financial Platform project is a mini ETL (Extract, Transform, Load) pipeline developed using Python, Pandas, and SQLite.

The project processes Nifty 100 company financial datasets, performs data validation and transformation, stores the cleaned data in a SQLite database, and generates analytical reports.

### Objectives

* Load raw financial datasets from Excel files.
* Validate data quality.
* Handle missing and invalid values.
* Transform and clean data.
* Store processed data in SQLite.
* Generate financial reports using SQL queries.

---

## Folder Structure

```text
N100_FINANCIAL_PLATFORM
│
├── data
│   ├── raw
│   │   ├── companies.xlsx
│   │   ├── balancesheet.xlsx
│   │   ├── cashflow.xlsx
│   │   ├── financial_ratios.xlsx
│   │   ├── market_cap.xlsx
│   │   ├── profitandloss.xlsx
│   │   ├── sectors.xlsx
│   │   └── stock_prices.xlsx
│   │
│   └── processed
│       └── companies_clean.csv
│
├── db
│   ├── schema.sql
│   └── nifty100.db
│
├── output
│   ├── validation_failures.csv
│   ├── top10_roce_companies.csv
│   └── top10_roe_companies.csv
│
├── src
│   └── etl
│       ├── loader.py
│       ├── validator.py
│       ├── normaliser.py
│       ├── transformer.py
│       ├── check_db.py
│       └── report.py
│
├── requirements.txt
└── README.md
```

---

## ETL Workflow

### 1. Data Loading

Loads Excel files from the raw data folder using Pandas.

**Script:** `loader.py`

### 2. Data Validation

Checks:

* Missing values
* Duplicate records
* Negative values

**Script:** `validator.py`

### 3. Data Normalization

Standardizes data formats and cleans text fields.

**Script:** `normaliser.py`

### 4. Data Transformation

* Selects required columns
* Handles missing values
* Generates cleaned datasets

**Script:** `transformer.py`

### 5. Database Loading

Loads transformed data into SQLite database.

**Script:** `loader.py`

### 6. Reporting

Generates:

* Top 10 Companies by ROCE
* Top 10 Companies by ROE

**Script:** `report.py`

---

## How to Run

### Install Dependencies

```bash
py -m pip install pandas openpyxl
```

### Run Validation

```bash
python src/etl/validator.py
```

### Run Transformation

```bash
python src/etl/transformer.py
```

### Load Data into SQLite

```bash
python src/etl/loader.py
```

### Verify Database

```bash
python src/etl/check_db.py
```

### Generate Reports

```bash
python src/etl/report.py
```

---

## Technologies Used

* Python 3.14
* Pandas
* SQLite3
* OpenPyXL
* VS Code

---

## Output Reports

### Top 10 ROCE Companies

Generated file:

```text
output/top10_roce_companies.csv
```

### Top 10 ROE Companies

Generated file:

```text
output/top10_roe_companies.csv
```

### Validation Report

Generated file:

```text
output/validation_failures.csv
```

---

## Project Outcome

Successfully built an end-to-end ETL pipeline for processing Nifty 100 financial datasets. The pipeline validates, transforms, stores, and analyzes company financial data while generating automated business reports.
