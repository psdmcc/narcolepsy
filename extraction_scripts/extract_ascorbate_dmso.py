import os
import json
import re

def analyze_ascorbate_and_dmso(data_dir="data_payloads"):
    """
    Precision scans extracted biomedical json arrays to map out 
    all structural references to Vitamin C variants and DMSO.
    """
    # Scan across both our primary collected JSON files to ensure absolute coverage
    files_to_scan = [
        "pubmed_narcolepsy_deep_corpus.json",
        "expanded_compounds_discovered.json",
        "targeted_parkinsons_hypothalamus_bridge.json"
    ]
    
    # Compile strict regex variations for comprehensive extraction
    vit_c_regex = re.compile(r"(vitamin[ -]c|ascorb|sodium[ -]ascorbate)")
    dmso_regex = re.compile(r"(\bdmso\b|dimethyl[ -]?sulfoxide)")

    discovered_mentions = []

    print("Initializing precision text scanning for Vitamin C and DMSO variants...\n")

    for file_name in files_to_scan:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            corpus = json.load(f)
            
        for article in corpus:
            # Check both titles and full abstract bodies combined
            title = article.get("title", "")
            abstract = article.get("abstract", article.get("abstract_snippet", ""))
            full_text = f"{title} {abstract}".lower()
            
            has_vit_c = bool(vit_c_regex.search(full_text))
            has_dmso = bool(dmso_regex.search(full_text))
            
            if has_vit_c or has_dmso:
                detected = []
                if has_vit_c: detected.append("VITAMIN C / ASCORBATE")
                if has_dmso: detected.append("DMSO")
                
                # Isolate the exact matching sentence out of the abstract text block
                matched_sentences = []
                sentences = re.split(r'(?<=[.!?])\s+', abstract)
                for sentence in sentences:
                    if vit_c_regex.search(sentence.lower()) or dmso_regex.search(sentence.lower()):
                        matched_sentences.append(sentence.strip())
                
                discovered_mentions.append({
                    "pmid": article.get("pmid", "N/A"),
                    "title": title,
                    "journal": article.get("journal_source", article.get("journal", "Unknown Venue")),
                    "detected_agents": detected,
                    "context_snippet": " | ".join(matched_sentences)[:300] + "..."
                })

    # Deduplicate entries using their unique PubMed ID (PMID)
    seen_pmids = set()
    unique_mentions = []
    for m in discovered_mentions:
        if m["pmid"] not in seen_pmids and m["pmid"] != "N/A":
            seen_pmids.add(m["pmid"])
            unique_mentions.append(m)

    print(f"=== EXTRACTION COMPLETE ===")
    print(f"Total unique articles discovered containing these specific variant tags: {len(unique_mentions)}\n")

    for idx, match in enumerate(unique_mentions, start=1):
        print(f"[{idx}] PMID: {match['pmid']} | Detected: {', '.join(match['detected_agents'])}")
        print(f"    Title: {match['title']}")
        print(f"    Journal: {match['journal']}")
        print(f"    Key Context: {match['context_snippet']}\n")

if __name__ == "__main__":
    analyze_ascorbate_and_dmso()
