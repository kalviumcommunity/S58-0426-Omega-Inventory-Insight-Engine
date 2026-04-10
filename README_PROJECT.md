# Retail Inventory Analysis - Project Setup & Testing Guide

## Project Overview

This project analyzes retail inventory and sales data to identify slow-moving items, fast-selling products, and demand variability across stores and time periods. The analysis helps retail chains optimize inventory management and reduce stockouts and overstocking.

## Project Structure

```
S58-0426-Omega-Inventory-Insight-Engine/
├── data/
│   ├── raw/                              # Raw, unprocessed data
│   │   └── sample_inventory_data.csv     # Sample inventory data
│   └── processed/                        # Cleaned and processed data
├── notebooks/
│   └── 01_exploratory_analysis.ipynb     # Exploratory data analysis notebook
├── scripts/
│   ├── load_and_clean_data.py            # Data loading and cleaning script
│   └── analyze_inventory.py              # Analysis and reporting script
├── outputs/                              # Generated reports and results
├── requirements.txt                      # Python dependencies
└── README_PROJECT.md                     # This file
```

## Prerequisites

Before running this project, ensure you have the following installed on your system:

- **Python 3.7+** (verify with `python --version`)
- **Conda** or **pip** (for package management)
- **Jupyter Notebook** (for interactive analysis)

### Installation Check

Run these commands in your terminal to verify installations:

```bash
python --version
conda --version
jupyter --version
```

## Setup Instructions

### Step 1: Create a Conda Environment (Recommended)

A virtual environment isolates project dependencies and prevents conflicts.

```bash
# Create a new conda environment named 'inventory-analysis'
conda create -n inventory-analysis python=3.9

# Activate the environment
conda activate inventory-analysis
```

### Step 2: Install Dependencies

Install all required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Verify Installation

After installation, verify all packages are available:

```bash
python -c "import pandas as pd; import numpy as np; import matplotlib.pyplot as plt; import seaborn as sns; print('✓ All dependencies installed successfully')"
```

## Running the Project

The workflow consists of three main steps:

### Step 1: Data Processing

Run the data cleaning and preprocessing script to prepare raw data:

```bash
python scripts/load_and_clean_data.py
```

**What it does:**
- Loads raw CSV data from `data/raw/sample_inventory_data.csv`
- Cleans and validates the data
- Creates engineered features (revenue, day of week, etc.)
- Saves processed data to `data/processed/processed_inventory_data.csv`

**Expected Output:**
```
Loading data from ../data/raw/sample_inventory_data.csv...
Loaded 100 rows and 8 columns
Cleaning data...
... (cleaning messages)
Data saved to ../data/processed/processed_inventory_data.csv
✓ Data processing completed successfully!
```

### Step 2: Run Analysis

Execute the analysis script to generate insights and reports:

```bash
python scripts/analyze_inventory.py
```

**What it does:**
- Analyzes slow-moving items (low sales volume)
- Identifies fast-selling products (high sales volume)
- Calculates demand variability across stores and time
- Generates summary statistics
- Saves results to `outputs/` folder

**Expected Output:**
```
============================================================
ANALYSIS 1: SLOW-MOVING ITEMS
============================================================
... (product rankings)

============================================================
ANALYSIS 2: FAST-SELLING ITEMS
============================================================
... (product rankings)

... (more analyses)

✓ Analysis completed successfully!
```

**Generated Files in `outputs/`:**
- `slow_moving_items.csv` - Products with low sales
- `fast_selling_items.csv` - Products with high sales
- `demand_variability_by_store.csv` - Store-level variability metrics
- `demand_variability_by_product.csv` - Product-level variability metrics
- `summary_statistics.txt` - Overall project summary

### Step 3: Exploratory Data Analysis Notebook

Launch Jupyter Notebook to explore data interactively:

```bash
# Navigate to the project directory
cd path/to/S58-0426-Omega-Inventory-Insight-Engine

# Launch Jupyter Notebook
jupyter notebook
```

**In Jupyter:**
1. The browser will open; navigate to `notebooks/` folder
2. Open `01_exploratory_analysis.ipynb`
3. Run cells sequentially (Shift + Enter) to see analysis and visualizations
4. Follow the narrative sections to understand the data

## Testing Guide

### Test 1: Data Loading

Verify that raw data loads correctly:

```bash
python -c "import pandas as pd; data = pd.read_csv('data/raw/sample_inventory_data.csv'); print(f'Loaded {len(data)} rows'); print(data.head())"
```

**Expected Result:** Displays 100 rows with columns: product_id, store_id, product_name, date, units_sold, units_in_stock, category, price

---

### Test 2: Data Processing Script

Run the processing script and verify output:

```bash
python scripts/load_and_clean_data.py
```

**Verify Success:**
- ✓ Script completes without errors
- ✓ Output message shows "✓ Data processing completed successfully!"
- ✓ File `data/processed/processed_inventory_data.csv` is created
- ✓ Processed file has more columns than raw file (includes engineered features)

**Check Processed Data:**
```bash
python -c "import pandas as pd; data = pd.read_csv('data/processed/processed_inventory_data.csv'); print(f'Columns: {list(data.columns)}')"
```

---

### Test 3: Analysis Script

Run the analysis script and verify reports:

```bash
python scripts/analyze_inventory.py
```

**Verify Success:**
- ✓ Script completes without errors
- ✓ All analysis sections execute (SLOW-MOVING, FAST-SELLING, DEMAND VARIABILITY, SUMMARY)
- ✓ Output message shows "✓ Analysis completed successfully!"
- ✓ Five CSV/text files created in `outputs/` folder:
  - `slow_moving_items.csv`
  - `fast_selling_items.csv`
  - `demand_variability_by_store.csv`
  - `demand_variability_by_product.csv`
  - `summary_statistics.txt`

**Inspect Results:**
```bash
# View first few lines of slow-moving items report
head outputs/slow_moving_items.csv

# View summary statistics
type outputs/summary_statistics.txt
```

---

### Test 4: Jupyter Notebook

Launch and test the notebook interactively:

```bash
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

**Steps:**
1. In the notebook, run **Section 1 (Import Libraries)** - should print "✓ Libraries imported successfully"
2. Run **Section 2 (Load Data)** - should load and display dataset info
3. Run **Section 3 (Data Quality)** - should report on missing values and data validation
4. Continue running sections sequentially
5. **Section 8 (Visualizations)** should generate 4 plots:
   - Daily sales trend
   - Average daily sales by product
   - Total sales by store
   - Inventory levels over time

---

### Test 5: Quick Integration Test

Run this complete workflow test:

```bash
# 1. Process data
echo "Step 1: Processing data..."
python scripts/load_and_clean_data.py

# 2. Run analysis
echo "Step 2: Running analysis..."
python scripts/analyze_inventory.py

# 3. Verify outputs exist
echo "Step 3: Checking output files..."
if [ -f "outputs/summary_statistics.txt" ]; then
    echo "✓ All outputs generated successfully!"
    echo "Results:"
    cat outputs/summary_statistics.txt
else
    echo "✗ Error: Output files not found"
fi
```

---

## Expected Results

### Data Overview
- **Total Records:** 100
- **Date Range:** 5 days (January 1-5, 2024)
- **Stores:** 3 (S01, S02, S03)
- **Products:** 5 (Laptop Stand, USB-C Cable, Desk Lamp, Mouse Pad, Keyboard)
- **Total Revenue:** Varies based on sales and pricing

### Key Insights from Sample Data

**Slow-Moving Items:** Products with average daily sales < 33rd percentile
- Expected: Some products show consistent low demand

**Fast-Selling Items:** Products with average daily sales >= 67th percentile
- Expected: Some products show high and consistent demand

**Demand Variability:** Stores and products with high sales volatility
- Expected: Coefficient of variation identifies stores/products with unpredictable demand

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
# Ensure your conda environment is activated
conda activate inventory-analysis

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "File not found" when loading data

**Solution:**
- Ensure you're running scripts from the project root directory
- Verify file paths are correct: `data/raw/sample_inventory_data.csv`
- Use absolute paths as alternative

### Issue: Jupyter Notebook not launching

**Solution:**
```bash
# Ensure Jupyter is installed in your environment
pip install jupyter

# Launch notebook with explicit port
jupyter notebook --port=8888
```

### Issue: Processed data file not created

**Solution:**
- Run `scripts/load_and_clean_data.py` again and check for error messages
- Verify `data/processed/` directory exists
- Check file write permissions

---

## Next Steps for Extension

This is a basic project setup. To extend it:

1. **Add More Data:** Replace sample data with real inventory data
2. **Advanced Analysis:** Add forecasting models, clustering, or anomaly detection
3. **Visualization Dashboard:** Create interactive dashboards with Dash or Streamlit
4. **Automated Reporting:** Schedule regular analysis runs and email reports
5. **Data Pipeline:** Integrate with databases and automate data ingestion

---

## Project Files Reference

| File | Purpose |
|------|---------|
| `data/raw/sample_inventory_data.csv` | Raw inventory data (read-only) |
| `data/processed/processed_inventory_data.csv` | Cleaned data with engineered features |
| `scripts/load_and_clean_data.py` | Data validation and feature engineering |
| `scripts/analyze_inventory.py` | Inventory analysis and reporting |
| `notebooks/01_exploratory_analysis.ipynb` | Interactive exploration and visualization |
| `outputs/*.csv` | Analysis result files |
| `requirements.txt` | Python package dependencies |

---

## Support & Questions

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure you're using the correct paths (relative to project root)
4. Check that the conda environment is activated
5. Review script output for specific error messages

---

**Project Status:** ✓ Ready to Use

This project is ready for immediate testing and analysis. All components are functional and follow data science best practices for reproducibility and clarity.
