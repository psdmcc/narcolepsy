import os
import json
import csv
from collections import Counter

def generate_expanded_compound_network(data_dir="data_payloads", output_dir="data_payloads"):
    """
    Parses the 50 newly discovered compound papers to map connections between alternative
    agents and the structural/inflammatory frameworks of the brain.
    """
    json_path = os.path.join(data_dir, "expanded_compounds_discovered.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Target data payload file missing at: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Establish the specialized node definitions
    alternative_agents = ["methylene blue", "vitamin c", "dmso", "magnesium", "ginkgo biloba", "bacopa monnieri"]
    contexts = ["neuroinflammation", "hypothalamus"]
    
    node_list = []
    for agent in alternative_agents:
        node_list.append({"Id": agent, "Label": agent.upper(), "Type": "Alternative Agent"})
    for ctx in contexts:
        node_list.append({"Id": ctx, "Label": ctx.capitalize(), "Type": "Biological Context"})

    # Specific mapping rules for text matching
    mapping = {
        "methylene blue": ["methylene blue", "methylthioninium"],
        "vitamin c": ["vitamin c", "ascorbic acid", "ascorbate"],
        "dmso": ["dmso", "dimethyl sulfoxide", "dimethylsulfoxide"],
        "magnesium": ["magnesium"],
        "ginkgo biloba": ["ginkgo", "gingko", "biloba"],
        "bacopa monnieri": ["bacopa", "monnieri", "brahmi"]
    }

    edge_weights = Counter()
    print(f"Constructing topological network matrix across {len(corpus)} records...")

    for article in corpus:
        text_pool = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
        
        # Determine which core contexts are active in this specific paper
        active_contexts = []
        if "neuroinflam" in text_pool or "brain damage" in text_pool:
            active_contexts.append("neuroinflammation")
        if "hypothalam" in text_pool:
            active_contexts.append("hypothalamus")
            
        # Connect active contexts together if they co-occur
        if len(active_contexts) > 1:
            edge_weights[("neuroinflammation", "hypothalamus")] += 1

        # Link discovered alternative agents to the active biological contexts
        for agent_id, variants in mapping.items():
            for variant in variants:
                if variant in text_pool:
                    for ctx in active_contexts:
                        edge_weights[(agent_id, ctx)] += 1
                    break

    # Save out nodes spreadsheet
    nodes_csv = os.path.join(output_dir, "expanded_nodes.csv")
    with open(nodes_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Id", "Label", "Type"])
        writer.writeheader()
        writer.writerows(node_list)

    # Save out edges spreadsheet
    edges_csv = os.path.join(output_dir, "expanded_edges.csv")
    with open(edges_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight", "Type"])
        for (src, tgt), weight in edge_weights.items():
            writer.writerow([src, tgt, weight, "Undirected"])

    print("\n=== EXPANDED COMPILING SUCCEEDED ===")
    print(f"* Alternative nodes tracker list saved to: {nodes_csv}")
    print(f"* Alternative edges weight link list saved to: {edges_csv}")

if __name__ == "__main__":
    generate_expanded_compound_network()
import os
import json
import csv
from collections import Counter

def generate_expanded_compound_network(data_dir="data_payloads", output_dir="data_payloads"):
    """
    Parses the 50 newly discovered compound papers to map connections between alternative
    agents and the structural/inflammatory frameworks of the brain.
    """
    json_path = os.path.join(data_dir, "expanded_compounds_discovered.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Target data payload file missing at: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Establish the specialized node definitions
    alternative_agents = ["methylene blue", "vitamin c", "dmso", "magnesium", "ginkgo biloba", "bacopa monnieri"]
    contexts = ["neuroinflammation", "hypothalamus"]
    
    node_list = []
    for agent in alternative_agents:
        node_list.append({"Id": agent, "Label": agent.upper(), "Type": "Alternative Agent"})
    for ctx in contexts:
        node_list.append({"Id": ctx, "Label": ctx.capitalize(), "Type": "Biological Context"})

    # Specific mapping rules for text matching
    mapping = {
        "methylene blue": ["methylene blue", "methylthioninium"],
        "vitamin c": ["vitamin c", "ascorbic acid", "ascorbate"],
        "dmso": ["dmso", "dimethyl sulfoxide", "dimethylsulfoxide"],
        "magnesium": ["magnesium"],
        "ginkgo biloba": ["ginkgo", "gingko", "biloba"],
        "bacopa monnieri": ["bacopa", "monnieri", "brahmi"]
    }

    edge_weights = Counter()
    print(f"Constructing topological network matrix across {len(corpus)} records...")

    for article in corpus:
        text_pool = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
        
        # Determine which core contexts are active in this specific paper
        active_contexts = []
        if "neuroinflam" in text_pool or "brain damage" in text_pool:
            active_contexts.append("neuroinflammation")
        if "hypothalam" in text_pool:
            active_contexts.append("hypothalamus")
            
        # Connect active contexts together if they co-occur
        if len(active_contexts) > 1:
            edge_weights[("neuroinflammation", "hypothalamus")] += 1

        # Link discovered alternative agents to the active biological contexts
        for agent_id, variants in mapping.items():
            for variant in variants:
                if variant in text_pool:
                    for ctx in active_contexts:
                        edge_weights[(agent_id, ctx)] += 1
                    break

    # Save out nodes spreadsheet
    nodes_csv = os.path.join(output_dir, "expanded_nodes.csv")
    with open(nodes_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Id", "Label", "Type"])
        writer.writeheader()
        writer.writerows(node_list)

    # Save out edges spreadsheet
    edges_csv = os.path.join(output_dir, "expanded_edges.csv")
    with open(edges_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight", "Type"])
        for (src, tgt), weight in edge_weights.items():
            writer.writerow([src, tgt, weight, "Undirected"])

    print("\n=== EXPANDED COMPILING SUCCEEDED ===")
    print(f"* Alternative nodes tracker list saved to: {nodes_csv}")
    print(f"* Alternative edges weight link list saved to: {edges_csv}")

if __name__ == "__main__":
    generate_expanded_compound_network()
