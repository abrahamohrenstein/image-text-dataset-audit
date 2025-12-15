# Image-Text Dataset Audit: Copyright and IP Indicators

**Empirical analysis of copyright indicators and franchise IP mentions across 4.3 billion image-text pairs**

[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Paper:** "Copyright Indicators and Franchise IP in Billion-Scale Image-Text Datasets: An Empirical Analysis"  
> **Author:** Abraham Ohrenstein (Zero Oversight Project)  
> **Date:** December 2025

---

## 📊 Overview

This repository contains the complete code and data for a reproducible empirical audit of three major AI training datasets:

- **COYO-700M** (746M records)
- **ReLAION-2B** (2.2B records) 
- **DataComp-1B** (1.4B records)

### Key Findings

- **10.16 million** copyright symbols (©) detected across datasets
- **Batman** most frequently mentioned character (2.45M mentions = 81,738× typical LoRA training requirement)
- **Warner Bros/DC** characters averaged 66% higher mention frequency than Disney/Marvel
- **Dataset variance** ranged from 1.14× (Mickey Mouse) to 10.81× (Woody)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11+
pip install duckdb pandas tqdm
```

### Running the Analysis

```bash
# Clone repository
git clone https://github.com/abrahamohrenstein/image-text-dataset-audit.git
cd image-text-dataset-audit

# Run full audit (requires dataset access)
python scripts/master_dataset_audit.py all

# Run specific audits
python scripts/master_dataset_audit.py copyright
python scripts/master_dataset_audit.py franchise
```

### Dataset Access

You'll need to download the original datasets:
- **COYO-700M:** https://github.com/kakaobrain/coyo-dataset
- **ReLAION-2B:** https://github.com/LAION-AI/laion-datasets
- **DataComp-1B:** https://github.com/mlfoundations/datacomp

⚠️ **Note:** Datasets are large (multi-TB). Analysis requires ~64GB RAM and ~48 hours on consumer hardware.

---

## 📁 Repository Structure

```
image-text-dataset-audit/
├── README.md
├── LICENSE
├── paper/
│   ├── main.pdf                    # Published paper
│   ├── main.tex                    # LaTeX source
│   └── references.bib              # Bibliography
├── scripts/
│   ├── master_dataset_audit.py     # Main analysis script
│   └── generate_figures.py         # Visualization code
├── data/
│   ├── results/
│   │   ├── copyright_indicators/   # Stock agency mentions
│   │   ├── franchise_characters/   # Character mention counts
│   │   └── comparison/             # Cross-dataset comparisons
│   └── queries/
│       └── sql_queries.md          # Complete SQL specifications
├── figures/
│   ├── fig1_top_characters.pdf
│   ├── fig2_rights_holders.pdf
│   ├── fig3_variance.pdf
│   └── fig4_copyright_indicators.pdf
└── docs/
    ├── METHODOLOGY.md              # Detailed methodology
    ├── LIMITATIONS.md              # Known limitations
    └── REPRODUCTION.md             # Step-by-step reproduction guide
```

---

## 📈 Results Summary

### Copyright Indicators

| Indicator | Total Mentions | Avg % |
|-----------|----------------|-------|
| Copyright © | 10,156,542 | 0.238% |
| Getty Images | 4,283,269 | 0.100% |
| Associated Press | 5,570,707 | 0.130% |
| Shutterstock | 3,614,326 | 0.084% |

### Top 10 Characters

| Rank | Character | Rights Holder | Total Mentions |
|------|-----------|---------------|----------------|
| 1 | Batman | Warner Bros/DC | 2,452,135 |
| 2 | Spider-Man | Marvel/Disney | 2,152,113 |
| 3 | Pokemon | Nintendo | 1,702,179 |
| 4 | Mickey Mouse | Disney | 1,524,475 |
| 5 | Superman | Warner Bros/DC | 1,344,962 |
| 6 | Minnie Mouse | Disney | 1,019,747 |
| 7 | Minions | Universal | 904,739 |
| 8 | Iron Man | Marvel/Disney | 848,029 |
| 9 | Captain America | Marvel/Disney | 799,625 |
| 10 | Mario | Nintendo | 745,584 |

### Rights Holder Comparison

| Rights Holder | Characters | Avg % per Character |
|---------------|------------|---------------------|
| Warner Bros/DC | 7 | 0.01552% |
| Nintendo | 8 | 0.01059% |
| Disney/Marvel/Lucasfilm/Pixar | 21 | 0.00933% |
| Universal/DreamWorks | 5 | 0.00615% |
| Nickelodeon | 4 | 0.00434% |
| Sega | 3 | 0.00229% |

---

## 🔬 Methodology

### Data Processing Pipeline

1. **Query Execution:** DuckDB SQL queries on Parquet files
2. **Keyword Matching:** Case-insensitive LIKE pattern matching
3. **Context Filters:** Disambiguation for ambiguous character names
4. **Aggregation:** Cross-dataset comparison and variance analysis

### Character Selection Criteria

- Multi-billion dollar franchises
- High cultural prevalence
- Balanced across 6 major rights holders
- 48 total characters measured

### Critical Limitations

⚠️ **This analysis examines ONLY textual caption metadata**

- **Does NOT analyze:** Image content, visual depictions, licensing status
- **Cannot determine:** Copyright status, fair use, infringement
- **False negatives:** Most copyrighted content has no textual markers
- **False positives:** Keyword matching includes unrelated contexts

See [LIMITATIONS.md](docs/LIMITATIONS.md) for complete discussion.

---

## 📊 Data Files

All result CSVs are in `data/results/`:

```
comparison_copyright_indicators.csv    # Cross-dataset copyright markers
comparison_franchise_characters.csv    # Cross-dataset character mentions
COYO700M_copyright_indicators.csv      # COYO-specific copyright data
ReLAION2B_copyright_indicators.csv     # ReLAION-specific copyright data
DataComp1B_copyright_indicators.csv    # DataComp-specific copyright data
# ... (similar files for franchise characters)
```

---

## 🔄 Reproducibility

### Hardware Requirements

- **CPU:** Modern multi-core (tested on i9-13900K)
- **RAM:** 64GB minimum
- **Storage:** 50GB for results, multi-TB for original datasets
- **Runtime:** ~48 hours for complete audit

### Software Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step-by-Step Guide

See [REPRODUCTION.md](docs/REPRODUCTION.md) for detailed instructions.

---

## 📝 Citation

If you use this code or data in your research, please cite:

```bibtex
@article{ohrenstein2025copyright,
  title={Copyright Indicators and Franchise IP in Billion-Scale Image-Text Datasets: An Empirical Analysis},
  author={Ohrenstein, Abraham},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Paper:** CC BY 4.0 (Creative Commons Attribution)

---

## 🤝 Contributing

This is a research artifact repository. For questions, corrections, or suggestions:

- **Open an issue:** For bugs or methodology questions
- **Pull requests:** For corrections to data or code
- **Email:** zero.oversight.project@proton.me

---

## ⚠️ Disclaimer

This research provides empirical documentation of textual patterns in public datasets. It does not:

- Make legal claims about copyright status
- Determine licensing compliance
- Establish infringement
- Provide legal advice

Interpretation requires domain expertise in law, ML, and policy.

---

## 🙏 Acknowledgments

- **DuckDB team** for enabling efficient billion-scale analysis on consumer hardware
- Dataset creators for making data accessible for research
- Community reviewers and endorsers

---

## 📧 Contact

**Abraham Ohrenstein**  
Zero Oversight Project  
Independent Researcher  
📧 zero.oversight.project@proton.me  
🐦 [@ZeroOversight](https://twitter.com/ZeroOversight) *(if applicable)*

---

**Last Updated:** December 2025
