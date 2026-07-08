import os
import json
from collections import Counter
import csv

def generate_network_matrices(data_dir="data_payloads", output_dir="data_payloads"):
    """
    Parses the 600 biomedical articles to construct standard node and edge CSV files
    suitable for topological network visualization mapping.
    """
    json_path = os.path.join(data_dir, "pubmed_narcolepsy_immune_corpus.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Target data payload file missing at: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    target_keywords = ["narcolepsy", "hypothalamus", "auto-immune", "inflammation", "parkinsons", "pneumonia"]
    
    # 1. Define nodes and populate metadata properties metrics
    node_list = []
    for idx, kw in enumerate(target_keywords):
        node_list.append({
            "Id": kw,
            "Label": kw.capitalize(),
            "Type": "Keyword"
        })

    # 2. Compute co-occurrence edge weights across entire dataset titles
    edge_weights = Counter()
    for article in corpus:
        title = article.get("title", "").lower()
        
        # Identify active keyword metrics trace handles
        active_nodes = []
        for kw in target_keywords:
            if kw in title or (kw == "auto-immune" and "autoimmune" in title):
                active_nodes.append(kw)
                
        # Build relational weight markers for all intersecting items
        if len(active_nodes) > 1:
            active_nodes.sort()
            for i in range(len(active_nodes)):
                for j in range(i + 1, len(active_nodes)):
                    pair = (active_nodes[i], active_nodes[j])
                    edge_weights[pair] += 1

    # 3. Write nodes map to disk harddrive files allocation layout
    nodes_csv_path = os.path.join(output_dir, "network_nodes.csv")
    with open(nodes_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Id", "Label", "Type"])
        writer.writeheader()
        writer.writerows(node_list)

    # 4. Write structural connection edges map to disk lines
    edges_csv_path = os.path.join(output_dir, "network_edges.csv")
    with open(edges_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight", "Type"])
        for (source, target), weight in edge_weights.items():
            writer.writerow([source, target, weight, "Undirected"])

    print(f"Topological data structure built successfully!")
    print(f"* Nodes spreadsheet exported to: {nodes_csv_path}")
    print(f"* Edges spreadsheet exported to: {edges_csv_path}")

if __name__ == "__main__":
    generate_network_matrices()
