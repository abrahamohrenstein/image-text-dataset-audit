# Reproduction Guide

**Step-by-step guide to reproduce the analysis from scratch**

---

## Overview

This guide will walk you through reproducing the complete analysis in approximately **72 hours** (48 hours compute + 24 hours setup).

**Prerequisites:**
- Consumer-grade workstation (64GB RAM, modern CPU)
- 2TB+ storage
- Python 3.11+
- Basic command line familiarity

---

## Part 1: Environment Setup (2-4 hours)

### Step 1.1: Install Python Dependencies

```bash
# Clone repository
git clone https://github.com/abrahamohrenstein/image-text-dataset-audit.git
cd image-text-dataset-audit

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import duckdb; print(duckdb.__version__)"
# Should output: 1.0.0 or higher
```

---

### Step 1.2: Directory Setup

Create directory structure for datasets:

```bash
# Linux/Mac
mkdir -p /datasets/{coyo-700m/data,relaion2b,datacomp1b}
mkdir -p data/results/{copyright_indicators,franchise_characters,comparison}

# Windows
mkdir C:\datasets\coyo-700m\data
mkdir C:\datasets\relaion2b
mkdir C:\datasets\datacomp1b
mkdir data\results\copyright_indicators
mkdir data\results\franchise_characters
mkdir data\results\comparison
```

---

## Part 2: Dataset Acquisition (varies, 1-7 days)

### Step 2.1: COYO-700M

**Source:** https://github.com/kakaobrain/coyo-dataset

**Download method:**
```bash
# Using wget (Linux/Mac)
wget -r -np -nH --cut-dirs=3 -R "index.html*" \
  https://storage.googleapis.com/...

# Or use provided download scripts from COYO repo
git clone https://github.com/kakaobrain/coyo-dataset.git
cd coyo-dataset
# Follow their download instructions
```

**Expected:**
- ~746 million records
- ~800 parquet files
- ~500GB total

**Verify:**
```python
import duckdb
con = duckdb.connect()
count = con.execute("""
    SELECT COUNT(*) 
    FROM read_parquet('/datasets/coyo-700m/data/*.parquet')
""").fetchone()[0]
print(f"COYO records: {count:,}")
# Should be: 746,361,237
```

---

### Step 2.2: ReLAION-2B

**Source:** Filtered LAION subset  
**Access:** Contact LAION for download instructions

**Alternative:** Use LAION-5B and filter yourself (not recommended, very large)

**Expected:**
- ~2.2 billion records
- Multiple parquet files
- ~1.5TB total

**Verify:**
```python
count = con.execute("""
    SELECT COUNT(*) 
    FROM read_parquet('/datasets/relaion2b/*.parquet')
""").fetchone()[0]
print(f"ReLAION records: {count:,}")
# Should be: 2,168,163,050
```

---

### Step 2.3: DataComp-1B

**Source:** https://github.com/mlfoundations/datacomp

**Download:**
```bash
# Follow DataComp instructions
git clone https://github.com/mlfoundations/datacomp.git
cd datacomp
# Use their download scripts
```

**Expected:**
- ~1.4 billion records
- Multiple parquet files
- ~800GB total

**Verify:**
```python
count = con.execute("""
    SELECT COUNT(*) 
    FROM read_parquet('/datasets/datacomp1b/*.parquet')
""").fetchone()[0]
print(f"DataComp records: {count:,}")
# Should be: 1,387,173,656
```

---

## Part 3: Configuration (30 minutes)

### Step 3.1: Edit Dataset Paths

Edit `scripts/master_dataset_audit.py`:

```python
DATASETS = {
    "COYO-700M": {
        "name": "COYO-700M",
        "path": r"/datasets/coyo-700m/data/*.parquet",  # ← Update this
        "caption_column": "text",
        "total_records": 746_361_237
    },
    "ReLAION-2B": {
        "name": "ReLAION-2B",
        "path": r"/datasets/relaion2b/*.parquet",  # ← Update this
        "caption_column": "caption",
        "total_records": 2_168_163_050
    },
    "DataComp-1B": {
        "name": "DataComp-1B",
        "path": r"/datasets/datacomp1b/*.parquet",  # ← Update this
        "caption_column": "text",
        "total_records": 1_387_173_656
    }
}
```

---

### Step 3.2: Configure DuckDB Settings

Based on your system:

```python
# In master_dataset_audit.py, adjust if needed:
con.execute("SET memory_limit='40GB'")  # Adjust based on your RAM
con.execute("SET temp_directory='/path/to/fast/storage'")  # SSD recommended
con.execute("SET threads=16")  # Adjust based on CPU cores
```

**Recommendations:**
- 64GB RAM → memory_limit='40GB'
- 128GB RAM → memory_limit='96GB'
- Leave ~20-30GB for OS

---

## Part 4: Running the Analysis (48 hours)

### Step 4.1: Test Run (Quick Validation)

Before full audit, test on small subset:

```python
# Create test query
import duckdb
con = duckdb.connect()

# Test COYO
result = con.execute("""
    SELECT COUNT(*) 
    FROM read_parquet('/datasets/coyo-700m/data/*.parquet')
    WHERE LOWER(text) LIKE '%batman%'
    LIMIT 1000000
""").fetchone()[0]

print(f"Batman mentions in first 1M COYO records: {result}")
```

Expected runtime: 2-5 minutes

---

### Step 4.2: Run Copyright Indicators Audit

```bash
python scripts/master_dataset_audit.py copyright
```

**Expected runtime:** ~12 hours  
**Output files:**
```
data/results/copyright_indicators/
├── COYO700M_copyright_indicators.csv
├── ReLAION2B_copyright_indicators.csv
├── DataComp1B_copyright_indicators.csv
└── comparison_copyright_indicators.csv
```

**Progress tracking:**
- Script shows progress bar with `tqdm`
- Estimated time remaining displayed
- Can safely interrupt (Ctrl+C) and restart

---

### Step 4.3: Run Franchise Character Audit

```bash
python scripts/master_dataset_audit.py franchise
```

**Expected runtime:** ~24 hours  
**Output files:**
```
data/results/franchise_characters/
├── COYO700M_franchise_characters.csv
├── ReLAION2B_franchise_characters.csv
├── DataComp1B_franchise_characters.csv
└── comparison_franchise_characters.csv
```

---

### Step 4.4: Run Complete Audit (All Analyses)

```bash
python scripts/master_dataset_audit.py all
```

**Expected runtime:** ~48 hours total  
**Includes:**
- Copyright indicators
- Franchise characters
- Cross-dataset comparisons
- Variance calculations

---

## Part 5: Generate Figures (1-2 hours)

### Step 5.1: Run Figure Generation Script

```bash
python scripts/generate_figures.py
```

**Outputs:**
```
figures/
├── fig1_top_characters.pdf
├── fig2_rights_holders.pdf
├── fig3_variance.pdf
└── fig4_copyright_indicators.pdf
```

**Dependencies:**
- matplotlib
- seaborn
- pandas

---

### Step 5.2: Verify Figures

Open PDFs and check:
- ✅ Batman shows 2.45M mentions in Fig 1
- ✅ Warner Bros/DC highest in Fig 2
- ✅ Woody shows 10.81x variance in Fig 3
- ✅ Copyright symbol highest in Fig 4

---

## Part 6: Validation (2-4 hours)

### Step 6.1: Verify Key Numbers

**Check against published paper:**

| Metric | Expected Value | Your Result | ✓ |
|--------|----------------|-------------|---|
| Total corpus | 4,301,697,943 | ? | |
| Batman mentions | 2,452,135 | ? | |
| Copyright © | 10,156,542 | ? | |
| Getty Images | 4,283,269 | ? | |
| Warner/DC avg | 0.01552% | ? | |
| Disney/Marvel avg | 0.00933% | ? | |

**Verification script:**

```python
import pandas as pd

# Load comparison data
df = pd.read_csv('data/results/comparison/comparison_franchise_characters.csv')

# Check Batman
batman = df[df['metric'] == 'DC - Batman'].iloc[0]
batman_total = (batman['COYO-700M_count'] + 
                batman['ReLAION-2B_count'] + 
                batman['DataComp-1B_count'])

print(f"Batman total: {batman_total:,}")
print(f"Expected: 2,452,135")
print(f"Match: {batman_total == 2452135}")
```

---

### Step 6.2: Spot Check Random Samples

Manually verify some results make sense:

```python
# Load COYO results
coyo_chars = pd.read_csv('data/results/franchise_characters/COYO700M_franchise_characters.csv')

# Sort by frequency
print(coyo_chars.sort_values('count', ascending=False).head(10))
```

**Sanity checks:**
- ✅ Batman, Spider-Man, Pokemon in top 5?
- ✅ Percentages < 1% for all characters?
- ✅ No negative counts?
- ✅ Counts sum correctly across datasets?

---

## Part 7: Troubleshooting

### Issue 1: Out of Memory

**Symptoms:** Script crashes with "Out of memory" error

**Solutions:**
```python
# Reduce memory limit
con.execute("SET memory_limit='30GB'")

# Increase temp directory space
con.execute("SET temp_directory='/path/to/larger/disk'")

# Process datasets one at a time instead of all together
```

---

### Issue 2: File Not Found

**Symptoms:** "No files found matching pattern"

**Solutions:**
1. Verify parquet files exist:
   ```bash
   ls /datasets/coyo-700m/data/*.parquet | head
   ```

2. Check path format:
   - Linux/Mac: `/datasets/...`
   - Windows: `C:/datasets/...` or `C:\\datasets\\...`

3. Verify glob pattern works:
   ```python
   import glob
   files = glob.glob('/datasets/coyo-700m/data/*.parquet')
   print(f"Found {len(files)} files")
   ```

---

### Issue 3: Slow Performance

**Symptoms:** Queries taking much longer than expected

**Solutions:**
1. Check you're using SSD not HDD
2. Verify temp directory on fast storage
3. Increase thread count if CPU underutilized
4. Close other applications

**Benchmark:**
```python
import time
start = time.time()
con.execute("SELECT COUNT(*) FROM read_parquet('/datasets/coyo-700m/data/*.parquet')").fetchone()
elapsed = time.time() - start
print(f"Full table scan: {elapsed:.1f} seconds")
# Should be: 60-180 seconds on SSD
```

---

### Issue 4: Encoding Errors

**Symptoms:** "Cannot decode" or special characters display wrong

**Solutions:**
```python
# Ensure UTF-8 handling
import sys
print(sys.getdefaultencoding())  # Should be 'utf-8'

# For CSV export, specify encoding
df.to_csv('output.csv', encoding='utf-8', index=False)
```

---

## Part 8: Comparison with Published Results

### Step 8.1: Download Published Results

Published CSV files available at:
```
https://github.com/abrahamohrenstein/image-text-dataset-audit/tree/main/data/results
```

### Step 8.2: Compare Your Results

```python
import pandas as pd

# Load published results
published = pd.read_csv('published_comparison_franchise_characters.csv')

# Load your results
yours = pd.read_csv('data/results/comparison/comparison_franchise_characters.csv')

# Compare
comparison = published.merge(yours, on='metric', suffixes=('_pub', '_yours'))
comparison['diff'] = comparison['COYO-700M_count_pub'] - comparison['COYO-700M_count_yours']
print(comparison[comparison['diff'] != 0])

# Should be empty or very small differences (rounding)
```

---

## Part 9: Documentation

### Generate Your Own Report

```python
# Summary statistics
print(f"""
Reproduction Summary
====================
Date: {datetime.now()}
Total records processed: {total_records:,}
Runtime: {runtime_hours:.1f} hours
Hardware: [Your specs]
DuckDB version: {duckdb.__version__}

Key Results:
- Batman mentions: {batman_total:,}
- Copyright symbols: {copyright_total:,}
- Variance range: {variance_min:.2f}x to {variance_max:.2f}x

Validation:
- Match published results: {matches}/{total_checks}
- Discrepancies: {discrepancies}
""")
```

---

## Part 10: Extending the Analysis

### Add New Characters

1. Edit `FRANCHISE_CHARACTERS` dict in `master_dataset_audit.py`
2. Add query pattern:
```python
"New Character": "LOWER({caption}) LIKE '%character name%'"
```
3. Re-run analysis

### Add New Datasets

1. Add to `DATASETS` configuration
2. Ensure parquet format with caption column
3. Update total record counts
4. Re-run analysis

### Modify Queries

All queries in `data/queries/sql_queries.md`  
Edit and re-run specific analyses

---

## Estimated Time Budget

| Task | Time |
|------|------|
| Environment setup | 2-4 hours |
| Dataset download | 1-7 days (depends on connection) |
| Configuration | 30 min |
| Test run | 30 min |
| Full audit | 48 hours |
| Figure generation | 1-2 hours |
| Validation | 2-4 hours |
| **Total (excluding download)** | **~56-60 hours** |

---

## Hardware Recommendations

### Minimum Specs
- CPU: 8 cores / 16 threads
- RAM: 64GB
- Storage: 2TB SSD
- Network: 100 Mbps for downloads

### Recommended Specs
- CPU: 12+ cores / 24+ threads
- RAM: 128GB
- Storage: 4TB NVMe SSD
- Network: 1 Gbps

### Budget Option
- Use cloud compute (AWS, GCP, Azure)
- Rent high-memory instance for ~48 hours
- Download datasets to cloud storage
- Cost: ~$50-200 depending on provider

---

## Getting Help

**Issues with reproduction:**
1. Check GitHub Issues: https://github.com/abrahamohrenstein/image-text-dataset-audit/issues
2. Email: zero_oversight_project@proton.me
3. Include:
   - Error message
   - System specs
   - DuckDB version
   - Dataset being processed

**Expected response time:** 1-3 business days

---

## Success Criteria

You have successfully reproduced the analysis if:

✅ All CSV files generated  
✅ Key numbers match within 0.01%  
✅ Figures render correctly  
✅ No errors in validation script  
✅ Runtime within 2x of published estimate  

---

## Next Steps

After successful reproduction:
1. **Cite the original paper** if using in your research
2. **Extend the analysis** with new characters/datasets
3. **Contribute improvements** via pull request
4. **Share your experience** to help others

---

**Happy reproducing!** 🚀
