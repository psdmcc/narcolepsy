import os
import json
from collections import Counter

def analyze_biomedical_corpus(data_dir="data_payloads", file_name="pubmed_narcolepsy_immune_corpus.json"):
    """
    Parses the extracted PubMed JSON payload to measure cross-thematic key term density
    and isolate prominent publishing patterns.
    """
    file_path = os.path.join(data_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: Target data payload file missing at: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    print(f"Analyzing {len(corpus)} records inside database matrix...\n")

    # Define core tracking metrics buckets
    journals = []
    keyword_counts = Counter()
    co_occurrences = Counter()
    
    target_keywords = ["narcolepsy", "hypothalamus", "auto-immune", "inflammation", "parkinsons", "pneumonia"]

    for article in corpus:
        title = article.get("title", "").lower()
        journals.append(article.get("journal_source", "Unknown Venue"))
        
        # Isolate which discrete keywords hit inside this specific title string
        active_hits = []
        for kw in target_keywords:
            if kw in title or (kw == "auto-immune" and "autoimmune" in title):
                keyword_counts[kw] += 1
                active_hits.append(kw)
        
        # If multiple targets intersect inside the same title, increment pairing metrics
        if len(active_hits) > 1:
            active_hits.sort()
            for i in range(len(active_hits)):
                for j in range(i + 1, len(active_hits)):
                    pair_string = f"{active_hits[i]} <---> {active_hits[j]}"
                    co_occurrences[pair_string] += 1

    # Print structural summary layout to terminal profile
    print("=== TOP KEYWORDS IN TITLES ===")
    for kw, count in keyword_counts.most_common():
        print(f"* {kw.capitalize()}: {count} matches")
        
    print("\n=== HIGH-DENSITY KEYWORD CO-OCCURRENCES (PAIRED TITLES) ===")
    if not co_occurrences:
        print("No exact string pairings identified inside localized title profiles.")
    for pair, count in co_occurrences.most_common(10):
        print(f"* {pair}: {count} articles")

    print("\n=== PRIMARY VENUES (TOP 5 JOURNALS) ===")
    for journal, count in Counter(journals).most_common(5):
        print(f"* {journal}: {count} papers")

if __name__ == "__main__":
    analyze_biomedical_corpus()
