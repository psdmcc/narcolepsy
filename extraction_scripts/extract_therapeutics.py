import os
import json
from collections import Counter

def extract_bridge_therapeutics(data_dir="data_payloads", file_name="targeted_parkinsons_hypothalamus_bridge.json"):
    """
    Parses the 31 target bridge articles to identify and rank mentioned
    therapeutic compounds, treatments, and biochemical markers.
    """
    file_path = os.path.join(data_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: Missing targeted json database at: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Filter down strictly to the 31 articles containing inflammatory data contexts
    active_records = [r for r in records if r.get("contains_inflammation_context") == True]
    print(f"Parsing abstract text fields across the {len(active_records)} identified bridge papers...\n")

    # Target compounds and biomarkers to track in the text fields
    target_compounds = {
        "orexin / hypocretin": ["orexin", "hypocretin"],
        "melatonin": ["melatonin"],
        "vitamin d": ["vitamin d", "calcitriol"],
        "oxytocin": ["oxytocin"],
        "probiotics / gut-axis": ["probiotic", "microbiota", "gut-brain", "fermented"],
        "cortisol / steroids": ["cortisol", "steroid"],
        "sirt1": ["sirt1"],
        "cytokines (il-6, tnf)": ["cytokine", "tnf", "interleukin", "il-6"]
    }

    compound_counts = Counter()

    for paper in active_records:
        # Scan both title and abstract snippet fields combined
        text_pool = f"{paper.get('title', '')} {paper.get('abstract_snippet', '')}".lower()
        
        for generic_name, variants in target_compounds.items():
            for variant in variants:
                if variant in text_pool:
                    compound_counts[generic_name] += 1
                    break # Count once per paper profile block

    print("=== RANKED BIOCHEMICAL & THERAPEUTIC MARKERS ===")
    for compound, count in compound_counts.most_common():
        percentage = (count / len(active_records)) * 100
        print(f"* {compound.upper()}: found in {count} papers ({percentage:.1f}%)")

if __name__ == "__main__":
    extract_bridge_therapeutics()
