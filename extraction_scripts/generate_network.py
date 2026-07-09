import os
import json
import csv
from collections import Counter

def generate_deep_abstract_network(data_dir="data_payloads", output_dir="data_payloads"):
    """
    Parses full article title and abstract strings to map deep topological paths.
    """
    json_path = os.path.join(data_dir, "pubmed_narcolepsy_deep_corpus.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Data file missing. Please execute scraper script first. Path: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    target_keywords = ["narcolepsy", "hypothalamus", "auto-immune", "inflammation", "parkinsons", "pneumonia"]
    edge_weights = Counter()
    
    # Specific targeted relationship tracker parameters counters
    parkinsons_hypothalamus_inflammation_count = 0

    print(f"Scanning deep text abstract frameworks across {len(corpus)} records...")

    for article in corpus:
        # Construct combined target text space out of title and abstract matrices
        search_text = (article.get("title", "") + " " + article.get("abstract", "")).lower()
        
        active_nodes = []
        for kw in target_keywords:
            if kw in search_text or (kw == "auto-immune" and "autoimmune" in search_text):
                active_nodes.append(kw)

        # Track the specific neurodegenerative-inflammatory link you requested
        if "parkinsons" in active_nodes and "hypothalamus" in active_nodes and "inflammation" in active_nodes:
            parkinsons_hypothalamus_inflammation_count += 1

        # Calculate general network pairing distributions weights
        if len(active_nodes) > 1:
            active_nodes.sort()
            for i in range(len(active_nodes)):
                for j in range(i + 1, len(active_nodes)):
                    pair = (active_nodes[i], active_nodes[j])
                    edge_weights[pair] += 1

    # Print targeted tracking observation directly to terminal
    print("\n================ TARGETED INSIGHT SUMMARY ================")
    print(f"* Articles detailing 'Parkinsons' + 'Hypothalamus' + 'Inflammation' links: {parkinsons_hypothalamus_inflammation_count}")
    print("==========================================================\n")

    # Save out updated data matrices spreadsheets to harddrive disk path spaces
    nodes_path = os.path.join(output_dir, "network_nodes.csv")
    with open(nodes_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Label", "Type"])
        for kw in target_keywords:
            writer.writerow([kw, kw.capitalize(), "Keyword"])

    edges_path = os.path.join(output_dir, "network_edges.csv")
    with open(edges_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight", "Type"])
        for (src, tgt), weight in edge_weights.items():
            writer.writerow([src, tgt, weight, "Undirected"])

    print(f"Deep network mapping matrix successfully exported!")
    print(f"* Updated Edges spreadsheet path: {edges_path}")

if __name__ == "__main__":
    generate_deep_abstract_network()
