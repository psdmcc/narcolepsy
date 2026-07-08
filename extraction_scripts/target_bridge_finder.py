import os
import json
import time
import http.client
import urllib.parse
import ssl
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

class NIHTargetBridgeFinder:
    """
    Lower-level socket interface configured to run a precision query matching 
    direct Parkinson's disease links to hypothalamic structures.
    """
    def __init__(self, output_dir: str = "data_payloads"):
        self.output_dir = output_dir
        self.ncbi_ip = "130.14.29.110"
        self.host_header = "eutils.ncbi.nlm.nih.gov"
        os.makedirs(self.output_dir, exist_ok=True)

    def execute_raw_request(self, endpoint: str, parameters: Dict[str, Any]) -> str:
        parameters["retmode"] = "json" if "efetch" not in endpoint else "xml"
        uri_path = f"/entrez/eutils/{endpoint}?{urllib.parse.urlencode(parameters)}"
        
        time.sleep(0.35) # Safe rate-limiting delay
        unverified_context = ssl._create_unverified_context()
        
        try:
            connection = http.client.HTTPSConnection(self.ncbi_ip, port=443, context=unverified_context, timeout=30)
            connection.request("GET", uri_path, headers={"User-Agent": "BridgeFinder/1.0", "Host": self.host_header})
            response = connection.getresponse()
            
            if response.status != 200:
                return ""
                
            raw_payload = response.read().decode("utf-8")
            connection.close()
            return raw_payload
        except Exception as e:
            print(f"Network error over socket line: {e}")
            raise e

    def find_bridge_papers(self) -> None:
        # Cross-reference the exact overlapping domains you identified
        target_query = '("parkinson"[Title/Abstract] OR "parkinsons"[Title/Abstract]) AND ("hypothalamus"[Title/Abstract] OR "hypothalamic"[Title/Abstract])'
        print(f"Deploying targeted bridge query to NIH servers...")
        
        search_params = {"db": "pubmed", "term": target_query, "usehistory": "y", "retmax": "100"}
        search_raw = self.execute_raw_request("esearch.fcgi", search_params)
        
        if not search_raw:
            return
            
        search_data = json.loads(search_raw)
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        webenv = search_data.get("esearchresult", {}).get("webenv")
        query_key = search_data.get("esearchresult", {}).get("querykey")
        
        print(f"Identified {len(id_list)} hidden papers containing BOTH terms across title/abstract profiles.")
        
        if not id_list:
            print("Aborting. No overlapping items found.")
            return

        bridge_records = []
        fetch_params = {"db": "pubmed", "query_key": query_key, "WebEnv": webenv, "retmax": "100"}
        xml_raw = self.execute_raw_request("efetch.fcgi", fetch_params)
        
        if not xml_raw:
            return

        try:
            root = ET.fromstring(xml_raw)
            for article_node in root.findall(".//PubmedArticle"):
                pmid = article_node.find(".//PMID").text if article_node.find(".//PMID") is not None else ""
                title = article_node.find(".//ArticleTitle").text if article_node.find(".//ArticleTitle") is not None else ""
                journal = article_node.find(".//Journal/Title").text if article_node.find(".//Journal/Title") is not None else ""
                
                abstract_texts = []
                for text_node in article_node.findall(".//AbstractText"):
                    if text_node.text:
                        abstract_texts.append(text_node.text)
                full_abstract = " ".join(abstract_texts)
                
                # Check if inflammation or its structural roots appear inside this specific subset
                has_inflammation = "inflam" in (title + " " + full_abstract).lower()
                
                bridge_records.append({
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "contains_inflammation_context": has_inflammation,
                    "abstract_snippet": full_abstract[:250] + "..." if full_abstract else "No abstract content"
                })
        except Exception as e:
            print(f"Parsing error: {e}")
            return

        # Output targeted summaries straight to your console layout screen
        print("\n=== TARGETED BRIDGE BREAKDOWN ===")
        inflam_hits = 0
        for idx, paper in enumerate(bridge_records, start=1):
            if paper["contains_inflammation_context"]:
                inflam_hits += 1
                print(f"[{inflam_hits}] PMID: {paper['pmid']}")
                print(f"    Title: {paper['title']}")
                print(f"    Journal: {paper['journal']}\n")
                
        print(f"Total overlapping papers found with active inflammatory traits: {inflam_hits}")

        # Save out to distinct new target folder payload text tracking documents
        out_file = os.path.join(self.output_dir, "targeted_parkinsons_hypothalamus_bridge.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(bridge_records, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    finder = NIHTargetBridgeFinder()
    finder.find_bridge_papers()
