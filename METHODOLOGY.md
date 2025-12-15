# Methodology

**Detailed technical methodology for "Copyright Indicators and Franchise IP in Billion-Scale Image-Text Datasets"**

---

## Overview

This study uses **keyword-based pattern matching** on caption text from three billion-scale image-text datasets to quantify observable frequencies of:

1. Copyright-related textual markers (stock agencies, © symbols)
2. Entertainment franchise character mentions (48 characters across 6 rights holders)

**Total corpus analyzed:** 4,301,697,943 image-text pairs

---

## 1. Dataset Selection

### Datasets Analyzed

| Dataset | Records | Caption Column | Format | Source |
|---------|---------|----------------|--------|--------|
| COYO-700M | 746,361,237 | `text` | Parquet | Kakaobrain (2022) |
| ReLAION-2B | 2,168,163,050 | `caption` | Parquet | Filtered LAION subset |
| DataComp-1B | 1,387,173,656 | `text` | Parquet | Gadre et al. (2023) |

### Selection Rationale

- **Widely used:** Cited in major ML research
- **Publicly documented:** Schema and access available
- **Scale:** Representative of billion-scale web scraping
- **Parquet format:** Enables efficient SQL querying via DuckDB

---

## 2. Technical Infrastructure

### Hardware Configuration

```
CPU:     Intel Core i9-13900K (24 cores, 32 threads)
RAM:     64GB DDR5
Storage: NVMe SSD (2TB)
OS:      Windows 11 / Ubuntu 24 (dual boot)
```

### Software Stack

```python
Python:  3.11+
DuckDB:  1.0+
Pandas:  2.0+
```

### DuckDB Configuration

```python
import duckdb

con = duckdb.connect()
con.execute("SET memory_limit='40GB'")          # Leave 24GB for system
con.execute("SET temp_directory='C:/datasets/duckdb_temp'")  # SSD temp
con.execute("SET threads=16")                   # Parallel processing
```

**Runtime:** ~48 hours for complete audit across all three datasets

---

## 3. Copyright Indicator Methodology

### 3.1 Stock Photo Agencies

**Indicators measured:**
- Getty Images
- Shutterstock
- Reuters
- Associated Press (including "AP Photo")
- AFP (requires co-occurrence with "getty" to reduce false positives)
- Alamy
- iStock / iStockPhoto

**Query pattern (example for Getty Images):**

```sql
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE LOWER(caption_column) LIKE '%getty images%'
```

**Case handling:** All queries use `LOWER()` for case-insensitive matching

### 3.2 Copyright Textual Markers

**Markers measured:**
- Copyright symbol: `©`
- Text: "copyright"
- Text: "all rights reserved"

**Special handling for © symbol:**

```sql
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE caption_column LIKE '%©%'
```

Note: No `LOWER()` needed for symbol matching

### 3.3 Rationale for Selection

Stock agencies selected based on:
1. Frequent mention in dataset curation discussions
2. Major commercial stock photography providers
3. Publicly documented presence in web scraping contexts

**Important:** Selection does NOT imply these are the only relevant copyright holders. Thousands of photographers, artists, and agencies remain unmeasured.

---

## 4. Franchise Character Methodology

### 4.1 Character Selection Criteria

**48 characters selected across 6 major rights holders:**

1. **Multi-billion dollar franchises:** Publicly documented revenue
2. **High cultural prevalence:** Likely to appear in web content
3. **Multiple rights holders:** Balanced representation
4. **Distinctive names:** Reduces false positive risk

### 4.2 Rights Holder Distribution

| Rights Holder | Characters Measured |
|---------------|---------------------|
| Disney/Marvel/Lucasfilm/Pixar | 21 |
| Warner Bros/DC | 7 |
| Nintendo | 8 |
| Nickelodeon | 4 |
| Sega | 3 |
| Universal/DreamWorks | 5 |

**Design goal:** Examine IP across multiple companies, not focus on single rights holder

### 4.3 Query Construction

#### Simple Queries (Distinctive Names)

For characters with unique, unambiguous names:

```sql
-- Batman (distinctive, minimal context needed)
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE LOWER(caption_column) LIKE '%batman%'
```

#### Disambiguation Queries (Common Names)

For characters with ambiguous names requiring context:

```sql
-- Woody (common first name, requires franchise context)
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE LOWER(caption_column) LIKE '%woody%' 
  AND (LOWER(caption_column) LIKE '%toy story%' 
       OR LOWER(caption_column) LIKE '%pixar%')
```

```sql
-- Sonic (common word, requires franchise context)
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE LOWER(caption_column) LIKE '%sonic%' 
  AND LOWER(caption_column) LIKE '%hedgehog%'
```

#### Multi-Context Queries

Some queries check multiple variations:

```sql
-- Spider-Man (handles hyphen variations)
SELECT COUNT(*) 
FROM read_parquet('dataset/*.parquet')
WHERE LOWER(caption_column) LIKE '%spider-man%' 
   OR LOWER(caption_column) LIKE '%spiderman%'
```

### 4.4 Complete Query Specifications

All 48 character queries documented in: `/data/queries/sql_queries.md`

---

## 5. Data Processing Pipeline

### Step 1: Individual Dataset Queries

For each dataset, run all queries:

```python
for indicator_name, sql_pattern in COPYRIGHT_INDICATORS.items():
    query = f"""
        SELECT COUNT(*) 
        FROM read_parquet('{dataset_path}')
        WHERE {sql_pattern.format(caption=caption_column)}
    """
    count = con.execute(query).fetchone()[0]
    results[indicator_name] = {
        "count": count,
        "percentage": (count / total_records) * 100
    }
```

### Step 2: Cross-Dataset Aggregation

Sum counts across all three datasets:

```python
total_mentions = (
    coyo_count + 
    relaion_count + 
    datacomp_count
)
```

### Step 3: Variance Calculation

For each character/indicator:

```python
max_pct = max(coyo_pct, relaion_pct, datacomp_pct)
min_pct = min(coyo_pct, relaion_pct, datacomp_pct)
variance_ratio = max_pct / min_pct
```

### Step 4: Results Export

Export to CSV for transparency and reproducibility:

```python
df.to_csv('results/comparison_franchise_characters.csv', index=False)
```

---

## 6. Validation Procedures

### 6.1 Spot Checking

Manual validation of random samples:
- Examined 100 random "Batman" mentions → 97% true positives
- Examined 100 random "Getty Images" mentions → 99% true positives
- Examined 100 random "Mario" mentions → 89% true positives (11% personal name usage)

### 6.2 Cross-Validation

Verified counts against published dataset statistics where available

### 6.3 Reproducibility Testing

Complete analysis re-run on separate machine (Ubuntu) produced identical results

---

## 7. Analysis Decisions

### 7.1 Threshold Selection

**No minimum threshold applied** - all mentions counted, including rare characters

Rationale: Even low-frequency mentions relevant for understanding dataset composition

### 7.2 Percentage Precision

**6 decimal places** used in raw data (e.g., 0.000236%)

Rationale: Enables detection of rare but meaningful patterns

### 7.3 Dataset Version Control

Analysis conducted December 2024 on datasets as accessed via published links

**Snapshot approach:** Results represent point-in-time analysis

---

## 8. Quality Assurance

### Checks Performed

✅ **Total record counts verified** against published documentation  
✅ **No NULL caption handling** - records with NULL captions excluded  
✅ **Encoding validation** - UTF-8 handling for special characters (©)  
✅ **Duplicate detection** - No deduplication performed (mirrors dataset as-is)  
✅ **Query optimization** - All queries use indexed parquet columns  

### Known Issues

⚠️ **COYO-700M watermark column:** Some NULL values present  
⚠️ **DataComp-1B:** No NSFW/watermark columns available  
⚠️ **Character encoding:** Some non-English mentions may be missed  

---

## 9. Computational Efficiency

### DuckDB Performance

**Query execution times (approximate):**
- Simple pattern match: 2-5 minutes per dataset
- Complex multi-condition: 5-10 minutes per dataset
- Full audit (48 characters + 13 indicators): ~48 hours total

### Optimization Techniques

1. **Parquet columnar format:** Only reads caption column
2. **Parallel processing:** DuckDB auto-parallelizes queries
3. **Memory management:** 40GB limit prevents system crashes
4. **Temp directory on SSD:** Faster intermediate operations

### Scalability

**Consumer hardware sufficient** - no cloud computing or distributed systems required

---

## 10. Reproducibility Notes

### Dataset Access

Original datasets must be obtained from:
- COYO-700M: https://github.com/kakaobrain/coyo-dataset
- ReLAION-2B: Contact LAION for access
- DataComp-1B: https://github.com/mlfoundations/datacomp

### File Paths

Analysis assumes Parquet files organized as:
```
/datasets/
  ├── coyo-700m/data/*.parquet
  ├── relaion2b/*.parquet
  └── datacomp1b/*.parquet
```

Adjust paths in `master_dataset_audit.py` configuration section

### Complete Reproduction

Estimated time: **72 hours** (48 hours compute + 24 hours setup/verification)

See `REPRODUCTION.md` for step-by-step guide

---

## References

- Kakaobrain (2022). COYO-700M: Image-Text Pair Dataset
- Gadre et al. (2023). DataComp: In search of the next generation of multimodal datasets
- DuckDB Documentation: https://duckdb.org/docs/
