import os
import json
import re

def analyze_edta_contexts(data_dir="data_payloads"):
    """
    Scans extracted biomedical JSON arrays to find any explicit references
    to EDTA or chelation-driven neuroprotective frameworks.
    """
    files_to_scan = [
        "pubmed_narcolepsy_deep_corpus.json",
        "expanded_compounds_discovered.json",
        "targeted_parkinsons_hypothalamus_bridge.json",
        "expanded_compounds_discovered.json"
    ]
    
    # Target EDTA naming variations and its clinical method (chelation)
    edta_regex = re.compile(r"(\bedta\b|ethylenediaminetetra|chelat)")
    discovered_mentions = []

    print("Initializing precision scanning for EDTA and chelation markers...\n")

    for file_name in files_to_scan:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            corpus = json.load(f)
            
        for article in corpus:
            title = article.get("title", "")
            abstract = article.get("abstract", article.get("abstract_snippet", ""))
            full_text = f"{title} {abstract}".lower()
            
            if edta_regex.search(full_text):
                # Isolate the exact matching sentences out of the text block
                matched_sentences = []
                sentences = re.split(r'(?<=[.!?])\s+', abstract)
                for sentence in sentences:
                    if edta_regex.search(sentence.lower()):
                        matched_sentences.append(sentence.strip())
                
                discovered_mentions.append({
                    "pmid": article.get("pmid", "N/A"),
                    "title": title,
                    "journal": article.get("journal_source", article.get("journal", "Unknown Venue")),
                    "context_snippet": " | ".join(matched_sentences)[:300] + "..." if matched_sentences else "Mentioned in title."
                })

    # Deduplicate entries using their unique PubMed ID (PMID)
    seen_pmids = set()
    unique_mentions = []
    for m in discovered_mentions:
        if m["pmid"] not in seen_pmids and m["pmid"] != "N/A":
            seen_pmids.add(m["pmid"])
            unique_mentions.append(m)

    print(f"=== EXTRACTION COMPLETE ===")
    print(f"Total unique articles discovered containing EDTA/Chelation markers: {len(unique_mentions)}\n")

    for idx, match in enumerate(unique_mentions, start=1):
        print(f"[{idx}] PMID: {match['pmid']}")
        print(f"    Title: {match['title']}")
        print(f"    Journal: {match['journal']}")
        print(f"    Key Context: {match['context_snippet']}\n")

if __name__ == "__main__":
    analyze_edta_contexts()
