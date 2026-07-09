import os
import json
import time
import http.client
import urllib.parse
import ssl
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

class NIHDeepBiomedicalScraper:
    """
    Advanced socket interface for the NIH/NCBI E-utilities API.
    Utilizes EFetch XML parsing to extract full abstract body text matrices.
    """
    def __init__(self, output_dir: str = "data_payloads", api_key: Optional[str] = None):
        self.output_dir = output_dir
        self.api_key = api_key
        self.ncbi_ip = "130.14.29.110"
        self.host_header = "eutils.ncbi.nlm.nih.gov"
        self.request_delay = 0.11 if api_key else 0.35
        os.makedirs(self.output_dir, exist_ok=True)

    def build_search_query(self) -> str:
        """
        Compiles the targeted Boolean cross-thematic terms.
        """
        neurological = '("narcolepsy"[Title/Abstract] OR "hypothalamus"[Title/Abstract] OR "parkinsons"[Title/Abstract])'
        immunological = '("auto-immune"[Title/Abstract] OR "inflammation"[Title/Abstract] OR "pneumonia"[Title/Abstract])'
        return f"{neurological} AND {immunological}"

    def execute_raw_request(self, endpoint: str, parameters: Dict[str, Any], retmode: str = "json") -> str:
        """
        Establishes raw connection sockets to stream raw textual bytes safely.
        """
        if self.api_key:
            parameters["api_key"] = self.api_key
        parameters["retmode"] = retmode
        
        uri_path = f"/entrez/eutils/{endpoint}?{urllib.parse.urlencode(parameters)}"
        time.sleep(self.request_delay)
        unverified_context = ssl._create_unverified_context()
        
        try:
            connection = http.client.HTTPSConnection(self.ncbi_ip, port=443, context=unverified_context, timeout=30)
            connection.request("GET", uri_path, headers={"User-Agent": "BiomedicalScraper/2.0", "Host": self.host_header})
            response = connection.getresponse()
            
            if response.status != 200:
                print(f"Server rejected raw data stream channel status: {response.status}")
                return ""
                
            raw_payload = response.read().decode("utf-8")
            connection.close()
            return raw_payload
        except Exception as e:
            print(f"Socket dropout encountered across execution pipeline loops: {e}")
            raise e

    def run_deep_pipeline(self, max_records: int = 400) -> None:
        """
        Queries and parses complete article information structures out of NCBI XML lines.
        """
        query = self.build_search_query()
        print("Initiating Deep NCBI Abstract Extraction Script Matrix...")
        
        # Phase 1: Search and allocate identifiers on the cloud history server
        search_params = {"db": "pubmed", "term": query, "usehistory": "y", "retmax": str(max_records)}
        search_raw = self.execute_raw_request("esearch.fcgi", search_params, retmode="json")
        
        if not search_raw:
            return
            
        search_data = json.loads(search_raw)
        search_result = search_data.get("esearchresult", {})
        id_list = search_result.get("idlist", [])
        webenv = search_result.get("webenv")
        query_key = search_result.get("querykey")
        
        print(f"Query matched {search_result.get('count', '0')} references. Pulling details via EFetch...")
        
        if not id_list:
            return

        extracted_corpus = []
        chunk_size = 100 # Keep fetching packages stable across network segments

        # Phase 2: Pull MEDLINE XML chunks via EFetch
        for start_idx in range(0, len(id_list), chunk_size):
            print(f"Downloading deep abstracts payload segment block indices: {start_idx} to {start_idx + chunk_size}...")
            
            fetch_params = {
                "db": "pubmed",
                "query_key": query_key,
                "WebEnv": webenv,
                "retstart": str(start_idx),
                "retmax": str(chunk_size),
                "retmode": "xml"
            }
            
            xml_raw = self.execute_raw_request("efetch.fcgi", fetch_params, retmode="xml")
            if not xml_raw:
                continue
                
            try:
                root = ET.fromstring(xml_raw)
                for article_node in root.findall(".//PubmedArticle"):
                    pmid = article_node.find(".//PMID").text if article_node.find(".//PMID") is not None else ""
                    title = article_node.find(".//ArticleTitle").text if article_node.find(".//ArticleTitle") is not None else ""
                    journal = article_node.find(".//Journal/Title").text if article_node.find(".//Journal/Title") is not None else ""
                    
                    # Programmatically compile nested abstract paragraphs matrices together
                    abstract_texts = []
                    for text_node in article_node.findall(".//AbstractText"):
                        if text_node.text:
                            abstract_texts.append(text_node.text)
                    full_abstract = " ".join(abstract_texts)
                    
                    record = {
                        "pmid": pmid,
                        "title": title or "",
                        "journal_source": journal or "",
                        "abstract": full_abstract
                    }
                    extracted_corpus.append(record)
            except Exception as xml_err:
                print(f"Skipping problematic structural package index boundary: {xml_err}")
                continue

        # Phase 3: Write complete deep text corpus files allocation matrix out to disk
        out_path = os.path.join(self.output_dir, "pubmed_narcolepsy_deep_corpus.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(extracted_corpus, f, ensure_ascii=False, indent=4)
            
        print(f"\nTask Done. Total complete abstract documents saved locally: {len(extracted_corpus)}")

if __name__ == "__main__":
    scraper = NIHDeepBiomedicalScraper()
    scraper.run_deep_pipeline(max_records=500)
