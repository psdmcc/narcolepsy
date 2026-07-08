import os
import json
import re
from collections import Counter

def run_fuzzy_semantic_analysis(data_dir="data_payloads", file_name="pubmed_narcolepsy_deep_corpus.json"):
    """
    Parses deep abstract matrices using fuzzy keyword normalization to capture
    morphological variants (e.g., hypothalamic, neuroinflammation, Parkinson's).
    """
    file_path = os.path.join(data_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: Target data payload file missing at: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    print(f"Executing Fuzzy Semantic Analysis across {len(corpus)} records...")

    # Define normalized regex matching rules for semantic flexibility
    rules = {
        "parkinsons": re.compile(r"parkinson"), 
        "hypothalamus": re.compile(r"hypothalam"),
        "inflammation": re.compile(r"inflam"),
        "narcolepsy": re.compile(r"narcolep"),
        "auto-immune": re.compile(r"auto[ -]?immun"),
        "pneumonia": re.compile(r"pneumon")
    }

    matched_articles = []
    global_co_occurrences = Counter()

    for article in corpus:
        title = article.get("title", "")
        abstract = article.get("abstract", "")
        combined_text = f"{title} {abstract}".lower()
        
        # Strip out punctuation markers to ensure clean text scans
        clean_text = re.sub(r"[^\w\s-]", "", combined_text)
        
        # Track hits per article based on root forms
        active_hits = []
        for key, regex in rules.items():
            if regex.search(clean_text):
                active_hits.append(key)
                
        # Isolate the specific Parkinson's hypothalamic inflammatory links
        if "parkinsons" in active_hits and "hypothalamus" in active_hits and "inflammation" in active_hits:
            matched_articles.append({
                "pmid": article.get("pmid", "N/A"),
                "title": title,
                "journal": article.get("journal_source", "Unknown Venue")
            })

        # Track global node overlaps
        if len(active_hits) > 1:
            active_hits.sort()
            for i in range(len(active_hits)):
                for j in range(i + 1, len(active_hits)):
                    pair = f"{active_hits[i]} <---> {active_hits[j]}"
                    global_co_occurrences[pair] += 1

    # Print summary of discoveries straight to your terminal
    print("\n================ UPGRADED SEMANTIC METRICS SUMMARY ================")
    print(f"Articles capturing 'Parkinson' + 'Hypothalamus' + 'Inflammation' connections: {len(matched_articles)}")
    print("====================================================================\n")

    if matched_articles:
        print("=== IDENTIFIED LINK PAPERS ===")
        for idx, paper in enumerate(matched_articles, start=1):
            print(f"[{idx}] PMID: {paper['pmid']}")
            print(f"    Title: {paper['title']}")
            print(f"    Journal: {paper['journal']}\n")
    else:
        print("No nested papers hit the strict three-way intersection constraint layout.\n")

    print("=== TOP LINGUISTIC NODE PAIRINGS OVERLAPS (ABSTRACT-WIDE) ===")
    for pair, count in global_co_occurrences.most_common(8):
        print(f"* {pair}: {count} papers")

if __name__ == "__main__":
    run_fuzzy_semantic_analysis()
