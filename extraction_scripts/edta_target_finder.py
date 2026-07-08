import os
import json
import time
import http.client
import urllib.parse
import ssl
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

class NIHTargetedEDTAFinder:
    """
    Direct socket interface configured to run a precision remediation query
    matching EDTA and chelation therapies directly to neuroinflammatory targets.
    """
    def __init__(self, output_dir: str = "data_payloads"):
        self.output_dir = output_dir
        self.ncbi_ip = "130.14.29.110"
        self.host_header = "eutils.ncbi.nlm.nih.gov"
        os.makedirs(self.output_dir, exist_ok=True)

    def execute_raw_request(self, endpoint: str, parameters: Dict[str, Any]) -> str:
        parameters["retmode"] = "json" if "efetch" not in endpoint else "xml"
        uri_path = f"/entrez/eutils/{endpoint}?{urllib.parse.urlencode(parameters)}"
        
        time.sleep(0.35)  # Safe NCBI rate limit delay
        unverified_context = ssl._create_unverified_context()
        
        try:
            connection = http.client.HTTPSConnection(self.ncbi_ip, port=443, context=unverified_context, timeout=30)
            connection.request("GET", uri_path, headers={"User-Agent": "EDTAFinder/1.0", "Host": self.host_header})
            response = connection.getresponse()
            
            if response.status != 200:
                return ""
                
            raw_payload = response.read().decode("utf-8")
            connection.close()
            return raw_payload
        except Exception as e:
            print(f"Network error over socket line: {e}")
            raise e

    def find_edta_papers(self) -> None:
        # Hyper-targeted query linking EDTA formulations and heavy metal chelation to your exact core tracks
        target_query = (
            '("edta" OR "ethylenediaminetetraacetic" OR "calcium disodium edta" OR "metal chelation") AND '
            '("neuroinflammation"[Title/Abstract] OR "hypothalamus"[Title/Abstract] OR "parkinsons"[Title/Abstract])'
        )
        print("Deploying targeted EDTA and Chelation remediation query to NIH servers...")
        
        search_params = {"db": "pubmed", "term": target_query, "usehistory": "y", "retmax": "50"}
        search_raw = self.execute_raw_request("esearch.fcgi", search_params)
        
        if not search_raw:
            print("Failed to get a response from the server.")
            return
            
        search_data = json.loads(search_raw)
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        webenv = search_data.get("esearchresult", {}).get("webenv")
        query_key = search_data.get("esearchresult", {}).get("querykey")
        
        print(f"Identified {len(id_list)} targeted papers matching EDTA/Chelation intersections.")
        
        if not id_list:
            print("Aborting. No overlapping records found.")
            return

        edta_records = []
        fetch_params = {"db": "pubmed", "query_key": query_key, "WebEnv": webenv, "retmax": "50"}
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
                
                edta_records.append({
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "abstract": full_abstract
                })
        except Exception as e:
            print(f"Parsing error: {e}")
            return

        print("\n=== TARGETED EDTA & CHELATION DISCOVERIES ===")
        for idx, paper in enumerate(edta_records[:10], start=1):
            print(f"[{idx}] PMID: {paper['pmid']}")
            print(f"    Title: {paper['title']}")
            print(f"    Journal: {paper['journal']}\n")

        # Save to its own dedicated tracking database payload file
        out_file = os.path.join(self.output_dir, "targeted_edta_discovered.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(edta_records, f, ensure_ascii=False, indent=4)
        print(f"Full dataset written locally to: {out_file}")

if __name__ == "__main__":
    finder = NIHTargetedEDTAFinder()
    finder.find_edta_papers()
