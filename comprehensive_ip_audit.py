#!/usr/bin/env python3
"""
Comprehensive IP and Copyright Indicator Audit
Analyzes COYO-700M, ReLAION-2B, and DataComp-1B for:
- Copyright indicators (stock agencies, symbols, text)
- Major franchise characters (Disney, Warner/DC, Nickelodeon, Nintendo, Sega, Universal)
- NSFW distribution
- Watermark detection

Author: Abraham Ohrenstein, Zero Oversight Project
Date: December 2024
"""

import duckdb
import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import time
import sys

# ═══════════════════════════════════════════════════════════════════════════════
# DATASET CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DATASETS = {
    "COYO-700M": {
        "name": "COYO-700M",
        "path": r"C:\datasets\coyo-700m\data\*.parquet",
        "caption_column": "text",
        "url_column": "url",
        "nsfw_column": "nsfw_score_opennsfw2",
        "watermark_column": "watermark_score",
        "total_records": 746_361_237
    },
    "ReLAION-2B": {
        "name": "ReLAION-2B",
        "path": r"G:\relaion2b\*.parquet",
        "caption_column": "caption",
        "url_column": "url",
        "nsfw_column": "punsafe",
        "watermark_column": "pwatermark",
        "total_records": 2_168_163_050
    },
    "DataComp-1B": {
        "name": "DataComp-1B",
        "path": r"G:\datacomp1b\*.parquet",
        "caption_column": "text",
        "url_column": "url",
        "nsfw_column": None,
        "watermark_column": None,
        "total_records": 1_387_173_656
    }
}

# Output directory
OUTPUT_DIR = Path("audit_results")
OUTPUT_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COPYRIGHT INDICATORS
# ═══════════════════════════════════════════════════════════════════════════════

COPYRIGHT_INDICATORS = {
    "Getty Images": "LOWER({caption}) LIKE '%getty images%'",
    "Shutterstock": "LOWER({caption}) LIKE '%shutterstock%'",
    "Reuters": "LOWER({caption}) LIKE '%reuters%'",
    "Associated Press": "LOWER({caption}) LIKE '%associated press%' OR LOWER({caption}) LIKE '%ap photo%'",
    "AFP": "LOWER({caption}) LIKE '%afp%' AND LOWER({caption}) LIKE '%getty%'",
    "Alamy": "LOWER({caption}) LIKE '%alamy%'",
    "iStock": "LOWER({caption}) LIKE '%istock%' OR LOWER({caption}) LIKE '%istockphoto%'",
    "Adobe Stock": "LOWER({caption}) LIKE '%adobe stock%'",
    "123RF": "LOWER({caption}) LIKE '%123rf%'",
    "Dreamstime": "LOWER({caption}) LIKE '%dreamstime%'",
    "Copyright Symbol ©": "{caption} LIKE '%©%'",
    "Copyright Text": "LOWER({caption}) LIKE '%copyright%'",
    "All Rights Reserved": "LOWER({caption}) LIKE '%all rights reserved%'",
}

# ═══════════════════════════════════════════════════════════════════════════════
# FRANCHISE CHARACTER INDICATORS
# Organized by rights holder for transparency in methodology
# ═══════════════════════════════════════════════════════════════════════════════

FRANCHISE_CHARACTERS = {
    # Disney/Marvel/Lucasfilm/Pixar
    "Disney - Mickey Mouse": "LOWER({caption}) LIKE '%mickey mouse%'",
    "Disney - Minnie Mouse": "LOWER({caption}) LIKE '%minnie mouse%'",
    "Disney - Donald Duck": "LOWER({caption}) LIKE '%donald duck%'",
    "Disney - Goofy": "LOWER({caption}) LIKE '%goofy%' AND (LOWER({caption}) LIKE '%disney%' OR LOWER({caption}) LIKE '%mickey%')",
    "Disney - Elsa": "LOWER({caption}) LIKE '%elsa%' AND LOWER({caption}) LIKE '%frozen%'",
    "Disney - Anna": "LOWER({caption}) LIKE '%anna%' AND LOWER({caption}) LIKE '%frozen%'",
    "Disney - Simba": "LOWER({caption}) LIKE '%simba%'",
    "Disney - Ariel": "LOWER({caption}) LIKE '%ariel%' AND LOWER({caption}) LIKE '%mermaid%'",
    
    "Marvel - Spider-Man": "LOWER({caption}) LIKE '%spider-man%' OR LOWER({caption}) LIKE '%spiderman%'",
    "Marvel - Iron Man": "LOWER({caption}) LIKE '%iron man%'",
    "Marvel - Captain America": "LOWER({caption}) LIKE '%captain america%'",
    "Marvel - Hulk": "LOWER({caption}) LIKE '%hulk%' AND (LOWER({caption}) LIKE '%marvel%' OR LOWER({caption}) LIKE '%avenger%')",
    "Marvel - Thor": "LOWER({caption}) LIKE '%thor%' AND (LOWER({caption}) LIKE '%marvel%' OR LOWER({caption}) LIKE '%avenger%' OR LOWER({caption}) LIKE '%asgard%')",
    "Marvel - Black Widow": "LOWER({caption}) LIKE '%black widow%' AND (LOWER({caption}) LIKE '%marvel%' OR LOWER({caption}) LIKE '%avenger%')",
    
    "Star Wars - Darth Vader": "LOWER({caption}) LIKE '%darth vader%'",
    "Star Wars - Luke Skywalker": "LOWER({caption}) LIKE '%luke skywalker%'",
    "Star Wars - Yoda": "LOWER({caption}) LIKE '%yoda%' AND LOWER({caption}) LIKE '%star wars%'",
    "Star Wars - R2-D2": "LOWER({caption}) LIKE '%r2-d2%' OR LOWER({caption}) LIKE '%r2d2%'",
    
    "Pixar - Buzz Lightyear": "LOWER({caption}) LIKE '%buzz lightyear%'",
    "Pixar - Woody": "LOWER({caption}) LIKE '%woody%' AND (LOWER({caption}) LIKE '%toy story%' OR LOWER({caption}) LIKE '%pixar%')",
    "Pixar - Lightning McQueen": "LOWER({caption}) LIKE '%lightning mcqueen%'",
    
    # Warner Bros/DC
    "DC - Superman": "LOWER({caption}) LIKE '%superman%'",
    "DC - Batman": "LOWER({caption}) LIKE '%batman%'",
    "DC - Wonder Woman": "LOWER({caption}) LIKE '%wonder woman%'",
    "DC - Joker": "LOWER({caption}) LIKE '%joker%' AND (LOWER({caption}) LIKE '%batman%' OR LOWER({caption}) LIKE '%gotham%' OR LOWER({caption}) LIKE '%dc%')",
    "DC - Harley Quinn": "LOWER({caption}) LIKE '%harley quinn%'",
    
    "Warner - Bugs Bunny": "LOWER({caption}) LIKE '%bugs bunny%'",
    "Warner - Scooby-Doo": "LOWER({caption}) LIKE '%scooby-doo%' OR LOWER({caption}) LIKE '%scooby doo%'",
    
    # Nickelodeon/Viacom
    "Nickelodeon - SpongeBob": "LOWER({caption}) LIKE '%spongebob%'",
    "Nickelodeon - Patrick Star": "LOWER({caption}) LIKE '%patrick star%' OR (LOWER({caption}) LIKE '%patrick%' AND LOWER({caption}) LIKE '%spongebob%')",
    "Nickelodeon - Teenage Mutant Ninja Turtles": "LOWER({caption}) LIKE '%teenage mutant ninja turtle%' OR LOWER({caption}) LIKE '%tmnt%'",
    "Nickelodeon - Dora": "LOWER({caption}) LIKE '%dora%' AND LOWER({caption}) LIKE '%explorer%'",
    
    # Nintendo
    "Nintendo - Mario": "LOWER({caption}) LIKE '%mario%' AND (LOWER({caption}) LIKE '%super%' OR LOWER({caption}) LIKE '%nintendo%' OR LOWER({caption}) LIKE '%luigi%')",
    "Nintendo - Luigi": "LOWER({caption}) LIKE '%luigi%'",
    "Nintendo - Princess Peach": "LOWER({caption}) LIKE '%princess peach%' OR (LOWER({caption}) LIKE '%peach%' AND LOWER({caption}) LIKE '%mario%')",
    "Nintendo - Bowser": "LOWER({caption}) LIKE '%bowser%' AND LOWER({caption}) LIKE '%mario%'",
    "Nintendo - Pikachu": "LOWER({caption}) LIKE '%pikachu%'",
    "Nintendo - Pokemon": "LOWER({caption}) LIKE '%pokemon%' OR LOWER({caption}) LIKE '%pokémon%'",
    "Nintendo - Link": "LOWER({caption}) LIKE '%link%' AND (LOWER({caption}) LIKE '%zelda%' OR LOWER({caption}) LIKE '%hyrule%')",
    "Nintendo - Zelda": "LOWER({caption}) LIKE '%zelda%'",
    
    # Sega
    "Sega - Sonic": "LOWER({caption}) LIKE '%sonic%' AND LOWER({caption}) LIKE '%hedgehog%'",
    "Sega - Tails": "LOWER({caption}) LIKE '%tails%' AND LOWER({caption}) LIKE '%sonic%'",
    "Sega - Knuckles": "LOWER({caption}) LIKE '%knuckles%' AND LOWER({caption}) LIKE '%sonic%'",
    
    # Universal/Illumination/DreamWorks
    "Universal - Minions": "LOWER({caption}) LIKE '%minion%'",
    "Universal - Gru": "LOWER({caption}) LIKE '%gru%' AND (LOWER({caption}) LIKE '%despicable%' OR LOWER({caption}) LIKE '%minion%')",
    "DreamWorks - Shrek": "LOWER({caption}) LIKE '%shrek%'",
    "DreamWorks - Donkey": "LOWER({caption}) LIKE '%donkey%' AND LOWER({caption}) LIKE '%shrek%'",
    "DreamWorks - Kung Fu Panda": "LOWER({caption}) LIKE '%kung fu panda%' OR (LOWER({caption}) LIKE '%po%' AND LOWER({caption}) LIKE '%panda%')",
}

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def print_header(text, char="═"):
    """Print professional header"""
    width = 80
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")

def print_subheader(text):
    """Print section header"""
    print(f"\n{text}")
    print("─" * 80)

def format_number(n):
    """Format number with commas"""
    return f"{n:,}"

def format_percentage(n, total):
    """Format as percentage with 6 decimals"""
    return f"{(n / total * 100):.6f}%"

def save_results(data, filename):
    """Save results to CSV"""
    filepath = OUTPUT_DIR / filename
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    return filepath

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def audit_copyright_indicators(dataset_name, config):
    """Audit copyright indicators in captions"""
    print_subheader(f"[{dataset_name}] COPYRIGHT INDICATORS")
    print(f"Path: {config['path']}")
    print(f"Records: {format_number(config['total_records'])}")
    
    con = duckdb.connect()
    caption_col = config['caption_column']
    results = {}
    
    start_time = time.time()
    
    for indicator_name, condition in tqdm(COPYRIGHT_INDICATORS.items(), 
                                          desc="Processing", 
                                          ncols=80,
                                          leave=False):
        query = f"""
        SELECT COUNT(*) FROM read_parquet('{config['path']}')
        WHERE {condition.format(caption=caption_col)}
        """
        count = con.execute(query).fetchone()[0]
        results[indicator_name] = {
            "count": count,
            "percentage": format_percentage(count, config['total_records'])
        }
    
    con.close()
    elapsed = time.time() - start_time
    
    # Print results
    print("\nResults:")
    for indicator, data in results.items():
        print(f"  {indicator:<30} {format_number(data['count']):>15} ({data['percentage']})")
    
    print(f"\nRuntime: {elapsed/60:.1f}m")
    
    # Save to CSV
    csv_data = [
        {"indicator": k, "count": v["count"], "percentage": v["percentage"]}
        for k, v in results.items()
    ]
    filename = f"{dataset_name.replace('-', '')}_copyright_indicators.csv"
    filepath = save_results(csv_data, filename)
    print(f"Saved: {filepath}")
    
    return results

def audit_franchise_characters(dataset_name, config):
    """Audit franchise character mentions across major IP holders"""
    print_subheader(f"[{dataset_name}] FRANCHISE CHARACTER MENTIONS")
    print(f"Path: {config['path']}")
    print(f"Records: {format_number(config['total_records'])}")
    
    con = duckdb.connect()
    caption_col = config['caption_column']
    results = {}
    
    start_time = time.time()
    
    for char_name, condition in tqdm(FRANCHISE_CHARACTERS.items(), 
                                     desc="Processing", 
                                     ncols=80,
                                     leave=False):
        query = f"""
        SELECT COUNT(*) FROM read_parquet('{config['path']}')
        WHERE {condition.format(caption=caption_col)}
        """
        count = con.execute(query).fetchone()[0]
        results[char_name] = {
            "count": count,
            "percentage": format_percentage(count, config['total_records'])
        }
    
    con.close()
    elapsed = time.time() - start_time
    
    # Print results grouped by company
    print("\nResults by Rights Holder:")
    current_company = None
    for char_name, data in results.items():
        company = char_name.split(" - ")[0]
        if company != current_company:
            print(f"\n{company}:")
            current_company = company
        char_display = char_name.split(" - ")[1]
        print(f"  {char_display:<35} {format_number(data['count']):>15} ({data['percentage']})")
    
    print(f"\nTotal Runtime: {elapsed/60:.1f}m")
    
    # Save to CSV
    csv_data = [
        {"character": k, "count": v["count"], "percentage": v["percentage"]}
        for k, v in results.items()
    ]
    filename = f"{dataset_name.replace('-', '')}_franchise_characters.csv"
    filepath = save_results(csv_data, filename)
    print(f"Saved: {filepath}")
    
    return results

def audit_nsfw_distribution(dataset_name, config):
    """Audit NSFW content distribution"""
    print_subheader(f"[{dataset_name}] NSFW DISTRIBUTION")
    print(f"Path: {config['path']}")
    print(f"Records: {format_number(config['total_records'])}")
    
    if config['nsfw_column'] is None:
        print("\nNo NSFW column available - skipping")
        return None
    
    con = duckdb.connect()
    nsfw_col = config['nsfw_column']
    
    start_time = time.time()
    
    # Count records >= 0.7 threshold
    query = f"""
    SELECT COUNT(*) FROM read_parquet('{config['path']}')
    WHERE {nsfw_col} >= 0.7
    """
    high_nsfw = con.execute(query).fetchone()[0]
    
    con.close()
    elapsed = time.time() - start_time
    
    results = {
        "NSFW Score ≥0.7": {
            "count": high_nsfw,
            "percentage": format_percentage(high_nsfw, config['total_records'])
        }
    }
    
    # Print results
    print("\nResults:")
    print(f"  NSFW Score ≥0.7: {format_number(high_nsfw)} ({results['NSFW Score ≥0.7']['percentage']})")
    print(f"\nRuntime: {elapsed/60:.1f}m")
    
    # Save to CSV
    csv_data = [
        {"category": "NSFW Score ≥0.7", "count": high_nsfw, 
         "percentage": results['NSFW Score ≥0.7']['percentage']}
    ]
    filename = f"{dataset_name.replace('-', '')}_nsfw_distribution.csv"
    filepath = save_results(csv_data, filename)
    print(f"Saved: {filepath}")
    
    return results

def audit_watermark_distribution(dataset_name, config):
    """Audit watermark detection distribution"""
    print_subheader(f"[{dataset_name}] WATERMARK DISTRIBUTION")
    print(f"Path: {config['path']}")
    print(f"Records: {format_number(config['total_records'])}")
    
    if config['watermark_column'] is None:
        print("\nNo watermark column available - skipping")
        return None
    
    con = duckdb.connect()
    watermark_col = config['watermark_column']
    
    start_time = time.time()
    
    # Count records >= 0.7 threshold
    query = f"""
    SELECT COUNT(*) FROM read_parquet('{config['path']}')
    WHERE {watermark_col} >= 0.7
    """
    high_watermark = con.execute(query).fetchone()[0]
    
    con.close()
    elapsed = time.time() - start_time
    
    results = {
        "Watermark Score ≥0.7": {
            "count": high_watermark,
            "percentage": format_percentage(high_watermark, config['total_records'])
        }
    }
    
    # Print results
    print("\nResults:")
    print(f"  Watermark Score ≥0.7: {format_number(high_watermark)} ({results['Watermark Score ≥0.7']['percentage']})")
    print(f"\nRuntime: {elapsed/60:.1f}m")
    
    # Save to CSV
    csv_data = [
        {"category": "Watermark Score ≥0.7", "count": high_watermark, 
         "percentage": results['Watermark Score ≥0.7']['percentage']}
    ]
    filename = f"{dataset_name.replace('-', '')}_watermark_distribution.csv"
    filepath = save_results(csv_data, filename)
    print(f"Saved: {filepath}")
    
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISON FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_comparison_table(all_results, audit_type):
    """Generate comparison table across all datasets"""
    print_header(f"COMPARISON SUMMARY: {audit_type.upper()}")
    
    # Prepare comparison data
    comparison_data = []
    
    # Get all keys from first dataset
    first_dataset = list(all_results.keys())[0]
    if all_results[first_dataset] is None:
        print(f"No data available for {audit_type}")
        return
    
    keys = list(all_results[first_dataset].keys())
    
    for key in keys:
        row = {"metric": key}
        for dataset_name, results in all_results.items():
            if results is not None and key in results:
                row[f"{dataset_name}_count"] = results[key]["count"]
                row[f"{dataset_name}_pct"] = results[key]["percentage"]
            else:
                row[f"{dataset_name}_count"] = "N/A"
                row[f"{dataset_name}_pct"] = "N/A"
        comparison_data.append(row)
    
    # Print comparison
    for item in comparison_data:
        print(f"\n{item['metric']}:")
        for dataset_name in all_results.keys():
            count_key = f"{dataset_name}_count"
            pct_key = f"{dataset_name}_pct"
            if count_key in item and item[count_key] != "N/A":
                print(f"  {dataset_name:<15} {format_number(item[count_key]):>15} ({item[pct_key]})")
            else:
                print(f"  {dataset_name:<15} {'N/A':>15}")
    
    # Save comparison
    filename = f"comparison_{audit_type.replace(' ', '_').lower()}.csv"
    filepath = save_results(comparison_data, filename)
    print(f"\nComparison saved: {filepath}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main execution function"""
    
    print_header("COMPREHENSIVE IP AND COPYRIGHT AUDIT")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Datasets: {', '.join(DATASETS.keys())}")
    print(f"Output Directory: {OUTPUT_DIR.absolute()}")
    
    if len(sys.argv) < 2:
        print("\nUsage: python comprehensive_ip_audit.py <audit_type>")
        print("\nAvailable audit types:")
        print("  copyright    - Copyright indicators (Getty, Shutterstock, ©, etc.)")
        print("  characters   - Franchise character mentions (Disney, Warner, Nintendo, etc.)")
        print("  nsfw         - NSFW distribution (requires score columns)")
        print("  watermark    - Watermark detection (requires score columns)")
        print("  all          - Run all audits sequentially")
        sys.exit(1)
    
    audit_type = sys.argv[1].lower()
    
    # Run selected audit
    if audit_type == "copyright" or audit_type == "all":
        all_results = {}
        for dataset_name, config in DATASETS.items():
            all_results[dataset_name] = audit_copyright_indicators(dataset_name, config)
        generate_comparison_table(all_results, "Copyright Indicators")
    
    if audit_type == "characters" or audit_type == "all":
        all_results = {}
        for dataset_name, config in DATASETS.items():
            all_results[dataset_name] = audit_franchise_characters(dataset_name, config)
        generate_comparison_table(all_results, "Franchise Characters")
    
    if audit_type == "nsfw" or audit_type == "all":
        all_results = {}
        for dataset_name, config in DATASETS.items():
            all_results[dataset_name] = audit_nsfw_distribution(dataset_name, config)
        generate_comparison_table(all_results, "NSFW Distribution")
    
    if audit_type == "watermark" or audit_type == "all":
        all_results = {}
        for dataset_name, config in DATASETS.items():
            all_results[dataset_name] = audit_watermark_distribution(dataset_name, config)
        generate_comparison_table(all_results, "Watermark Distribution")
    
    print_header("AUDIT COMPLETE")

if __name__ == "__main__":
    main()
