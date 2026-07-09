import os
import json
from collections import Counter

def analyze_expanded_markers(data_dir="data_payloads"):
    """
    Scans both the deep corpus and the targeted bridge dataset to evaluate
    the presence of newly requested alternative therapeutic markers.
    """
    deep_corpus_path = os.path.join(data_dir, "pubmed_narcolepsy_deep_corpus.json")
    bridge_path = os.path.join(data_dir, "targeted_parkinsons_hypothalamus_bridge.json")

    if not os.path.exists(deep_corpus_path) or not os.path.exists(bridge_path):
        print("Error: Missing required JSON data assets. Please ensure scraper scripts have run.")
        return

    # Load datasets
    with open(deep_corpus_path, "r", encoding="utf-8") as f:
        deep_corpus = json.load(f)
    with open(bridge_path, "r", encoding="utf-8") as f:
        bridge_data = json.load(f)
        
    # Isolate active inflammatory papers from the bridge subset (31 papers)
    active_bridge = [r for r in bridge_data if r.get("contains_inflammation_context") == True]

    # Map expanded target keywords and their common variations
    expanded_markers = {
        "methylene blue": ["methylene blue", "methylthioninium"],
        "vitamin c": ["vitamin c", "ascorbic acid", "ascorbate"],
        "dmso": ["dmso", "dimethyl sulfoxide", "dimethylsulfoxide"],
        "magnesium": ["magnesium"],
        "ginkgo biloba": ["ginkgo", "gingko", "biloba"],
        "bacopa monnieri": ["bacopa", "monnieri", "brahmi"]
    }

    # Tracking counters
    deep_counts = Counter()
    bridge_counts = Counter()

    # 1. Scan Base Deep Corpus (499 records)
    for article in deep_corpus:
        text_pool = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
        for marker, variants in expanded_markers.items():
            for v in variants:
                if v in text_pool:
                    deep_counts[marker] += 1
                    break

    # 2. Scan Targeted Parkinson's-Hypothalamus Bridge Subset (31 records)
    for article in active_bridge:
        text_pool = f"{article.get('title', '')} {article.get('abstract_snippet', '')}".lower()
        for marker, variants in expanded_markers.items():
            for v in variants:
                if v in text_pool:
                    bridge_counts[marker] += 1
                    break

    # Output Comparative Metrics to Console
    print("=================== EXPANDED MARKER CORRELATION REPORT ===================")
    print(f"Dataset Baselines: Base Corpus ({len(deep_corpus)} papers) | Bridge Subset ({len(active_records := active_bridge)} papers)\n")
    
    print(f"{'EXPANDED BIOCHEMICAL MARKER':<25} | {'BASE CORPUS HITS':<18} | {'BRIDGE SUBSET HITS':<18}")
    print("-" * 68)
    
    for marker in expanded_markers.keys():
        deep_hit = deep_counts[marker]
        bridge_hit = bridge_counts[marker]
        
        deep_pct = (deep_hit / len(deep_corpus)) * 100
        bridge_pct = (bridge_hit / len(active_bridge)) * 100 if active_bridge else 0.0
        
        deep_str = f"{deep_hit} ({deep_pct:.1f}%)"
        bridge_str = f"{bridge_hit} ({bridge_pct:.1f}%)"
        
        print(f"{marker.upper():<25} | {deep_str:<18} | {bridge_str:<18}")
    print("==========================================================================")

if __name__ == "__main__":
    analyze_expanded_markers()
