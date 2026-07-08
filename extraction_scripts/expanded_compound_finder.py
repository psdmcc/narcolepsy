import os
import json
import time
import http.client
import urllib.parse
import ssl
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

class NIHExpandedCompoundFinder:
    """
    Direct socket interface optimized to bypass literature silos by pairing 
    your specific compound list directly with neuroinflammatory and hypothalamic tags.
    """
    def __init__(self, output_dir: str = "data_payloads"):
        self.output_dir = output_dir
        self.ncbi_ip = "130.14.29.110"
        self.host_header = "eutils.ncbi.nlm.nih.gov"
        os.makedirs(self.output_dir, exist_ok=True)

    def execute_raw_request(self, endpoint: str, parameters: Dict[str, Any]) -> str:
        parameters["retmode"] = "json" if "efetch" not in endpoint else "xml"
        uri_path = f"/entrez/eutils/{endpoint}?{urllib.parse.urlencode(parameters)}"
        
        time.sleep(0.35)
        unverified_context = ssl._create_unverified_context()
        
        try:
            connection = http.client.HTTPSConnection(self.ncbi_ip, port=443, context=unverified_context, timeout=30)
            connection.request("GET", uri_path, headers={"User-Agent": "CompoundFinder/1.0", "Host": self.host_header})
            response = connection.getresponse()
            return response.read().decode("utf-8") if response.status == 200 else ""
        except Exception as e:
            print(f"Network error: {e}")
            raise e

    def search_compounds(self) -> None:
        # Construct explicit terms including formal biochemical variations
        compounds = (
            '("methylene blue" OR "methylthioninium" OR "vitamin c" OR "ascorbic acid" '
            'OR "dmso" OR "dimethyl sulfoxide" OR "magnesium" OR "ginkgo" OR "biloba" '
            'OR "bacopa" OR "monnieri" OR "brahmi")'
        )
        context = 'AND ("neuroinflammation"[Title/Abstract] OR "hypothalamus"[Title/Abstract] OR "hypothalamic"[Title/Abstract])'
        full_query = f"{compounds} {context}"
        
        print("Deploying hyper-targeted alternative compound query to NIH servers...")
        
        search_params = {"db": "pubmed", "term": full_query, "usehistory": "y", "retmax": "50"}
        search_raw = self.execute_raw_request("esearch.fcgi", search_params)
        
        if not search_raw:
            return
            
        search_data = json.loads(search_raw)
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        webenv = search_data.get("esearchresult", {}).get("webenv")
        query_key = search_data.get("esearchresult", {}).get("querykey")
        
        print(f"Identified {len(id_list)} hidden papers connecting these specific agents to neuroinflammation/hypothalamus.")
        
        if not id_list:
            return

        fetch_params = {"db": "pubmed", "query_key": query_key, "WebEnv": webenv, "retmax": "50"}
        xml_raw = self.execute_raw_request("efetch.fcgi", fetch_params)
        
        if not xml_raw:
            return

        compound_records = []
        try:
            root = ET.fromstring(xml_raw)
            for article_node in root.findall(".//PubmedArticle"):
                pmid = article_node.find(".//PMID").text if article_node.find(".//PMID") is not None else ""
                title = article_node.find(".//ArticleTitle").text if article_node.find(".//ArticleTitle") is not None else ""
                journal = article_node.find(".//Journal/Title").text if article_node.find(".//Journal/Title") is not None else ""
                
                abstract_texts = [t.text for t in article_node.findall(".//AbstractText") if t.text]
                full_abstract = " ".join(abstract_texts)
                
                compound_records.append({
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "abstract": full_abstract
                })
        except Exception as e:
            print(f"Parsing error: {e}")
            return

        print("\n=== EXPANDED COMPOUND DISCOVERIES ===")
        for idx, paper in enumerate(compound_records[:15], start=1):
            print(f"[{idx}] PMID: {paper['pmid']}")
            print(f"    Title: {paper['title']}")
            print(f"    Journal: {paper['journal']}\n")

        out_file = os.path.join(self.output_dir, "expanded_compounds_discovered.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(compound_records, f, ensure_ascii=False, indent=4)
        print(f"Full dataset written locally to: {out_file}")

if __name__ == "__main__":
    finder = NIHExpandedCompoundFinder()
    finder.search_compounds()
