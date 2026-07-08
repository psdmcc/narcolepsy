import os
import json
import time
import http.client
import urllib.parse
import ssl
from typing import Dict, List, Any, Optional

class NIHBiomedicalScraper:
    """
    Interface for the NIH/NCBI E-utilities API using low-level sockets.
    Bypasses macOS DNS layers by sending raw HTTP packets directly to the NCBI server cluster.
    """
    def __init__(self, output_dir: str = "data_payloads", api_key: Optional[str] = None):
        self.output_dir = output_dir
        self.api_key = api_key
        
        # Target NCBI endpoint cluster values directly via public IP address
        self.ncbi_ip = "130.14.29.110"
        self.host_header = "eutils.ncbi.nlm.nih.gov"
        
        # Enforce rate-limits securely based on official NCBI guidelines
        self.request_delay = 0.11 if api_key else 0.35
        os.makedirs(self.output_dir, exist_ok=True)

    def build_search_query(self) -> str:
        """
        Compiles the strict Boolean target search terms.
        """
        neurological_terms = '("narcolepsy"[Title/Abstract] OR "hypothalamus"[Title/Abstract] OR "parkinsons"[Title/Abstract])'
        immunological_terms = '("auto-immune"[Title/Abstract] OR "inflammation"[Title/Abstract] OR "pneumonia"[Title/Abstract])'
        return f"{neurological_terms} AND {immunological_terms}"

    def execute_request(self, endpoint: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Constructs a direct socket connection to the target server to bypass DNS lookup failures.
        """
        if self.api_key:
            parameters["api_key"] = self.api_key
        parameters["retmode"] = "json"
        
        # Build the exact URI path allocation extension string
        uri_path = f"/entrez/eutils/{endpoint}?{urllib.parse.urlencode(parameters)}"
        
        time.sleep(self.request_delay)
        
        # Force a connection context that ignores validation chain roadblocks
        unverified_context = ssl._create_unverified_context()
        
        try:
            # Connect directly to the IP on port 443 (HTTPS)
            connection = http.client.HTTPSConnection(
                self.ncbi_ip, 
                port=443, 
                context=unverified_context, 
                timeout=15
            )
            
            # Send the request directly across the raw socket connection line
            connection.request(
                "GET", 
                uri_path, 
                headers={
                    "User-Agent": "Mozilla/5.0 (Python 3.11.15; BiomedicalScraper)",
                    "Host": self.host_header
                }
            )
            
            response = connection.getresponse()
            if response.status != 200:
                print(f"API Server rejected transaction stream profile. Status Code: {response.status}")
                return {}
                
            raw_data = response.read().decode("utf-8")
            connection.close()
            return json.loads(raw_data)
            
        except Exception as e:
            print(f"Socket drop tracking exception caught over raw line parameter connection: {e}")
            raise e

    def run_pipeline(self, max_records_to_fetch: int = 1000) -> None:
        """
        Executes the full cloud-cached text extraction sequence.
        """
        search_query = self.build_search_query()
        print(f"Initializing NCBI Pipeline for targeted keywords...")
        
        search_params = {
            "db": "pubmed",
            "term": search_query,
            "usehistory": "y",
            "retmax": str(max_records_to_fetch)
        }
        
        search_response = self.execute_request("esearch.fcgi", search_params)
        if not search_response:
            return
            
        search_results = search_response.get("esearchresult", {})
        id_list = search_results.get("idlist", [])
        total_found = search_results.get("count", "0")
        webenv = search_results.get("webenv")
        query_key = search_results.get("querykey")
        
        print(f"Query matched {total_found} absolute items. Commencing retrieval max of {len(id_list)} IDs.")
        
        if not id_list:
            print("Zero records found matching parameters. Pipeline halted.")
            return

        extracted_corpus = []
        page_chunk_size = 200  
        
        for start_idx in range(0, len(id_list), page_chunk_size):
            print(f"Streaming data page block indices: {start_idx} to {start_idx + page_chunk_size}...")
            
            summary_params = {
                "db": "pubmed",
                "query_key": query_key,
                "WebEnv": webenv,
                "retstart": str(start_idx),
                "retmax": str(page_chunk_size)
            }
            
            try:
                summary_response = self.execute_request("esummary.fcgi", summary_params)
                uid_records = summary_response.get("result", {})
                
                for uid in uid_records.get("uids", []):
                    article = uid_records.get(uid, {})
                    
                    record = {
                        "pmid": uid,
                        "title": article.get("title", ""),
                        "journal_source": article.get("source", ""),
                        "publication_date": article.get("pubdate", ""),
                        "author_list": [auth.get("name", "") for auth in article.get("authors", [])],
                        "document_language": article.get("lang", []),
                        "doi_string": ""
                    }
                    
                    for identifier in article.get("articleids", []):
                        if identifier.get("idtype") == "doi":
                            record["doi_string"] = identifier.get("value", "")
                            
                    extracted_corpus.append(record)
                    
            except Exception as e:
                print(f"Skipping corrupt batch partition trace frame at index {start_idx}. Error: {e}")
                continue

        output_file_name = "pubmed_narcolepsy_immune_corpus.json"
        final_file_path = os.path.join(self.output_dir, output_file_name)
        
        with open(final_file_path, "w", encoding="utf-8") as f:
            json.dump(extracted_corpus, f, ensure_ascii=False, indent=4)
            
        print(f"\nPipeline execution successfully completed.")
        print(f"Total extracted documents wrote to harddrive: {len(extracted_corpus)}")
        print(f"Target location: {final_file_path}")

if __name__ == "__main__":
    NCBI_API_KEY = None  
    
    scraper = NIHBiomedicalScraper(output_dir="data_payloads", api_key=NCBI_API_KEY)
    scraper.run_pipeline(max_records_to_fetch=500)
