"""
PubMed API client for scientific publications
"""

import requests
import time
from typing import Dict, List, Optional
from config.settings import Config


class PubMedClient:
    """Client for PubMed API (free public API)"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.PUBMED_API_KEY
        self.last_call_time = 0
        self.rate_limit_delay = 0.34  # 3 requests per second limit
    
    def _apply_rate_limit(self):
        """Apply PubMed API rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_call_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_call_time = time.time()
    
    def search_articles(self, query: str, max_results: int = 10, 
                       reldate: int = 730) -> List[Dict]:
        """
        Search PubMed articles
        
        Args:
            query: Search query
            max_results: Maximum number of results
            reldate: Days back to search (default: 2 years)
            
        Returns:
            List of article dictionaries
        """
        self._apply_rate_limit()
        
        try:
            # Search endpoint
            search_endpoint = f"{self.BASE_URL}/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'date',
                'reldate': reldate,
                'datetype': 'pdat'
            }
            
            if self.api_key:
                search_params['api_key'] = self.api_key
            
            search_response = requests.get(search_endpoint, params=search_params, timeout=10)
            search_response.raise_for_status()
            search_data = search_response.json()
            
            if 'esearchresult' not in search_data or 'idlist' not in search_data['esearchresult']:
                return []
            
            article_ids = search_data['esearchresult']['idlist'][:5]  # Limit to 5 for demo
            
            if not article_ids:
                return []
            
            # Fetch article details
            return self._fetch_article_details(article_ids)
            
        except requests.exceptions.RequestException as e:
            print(f"PubMed search error: {e}")
            return self._mock_articles()
    
    def search_toxicology_articles(self, max_results: int = 10) -> List[Dict]:
        """
        Search for toxicology and 3D model related articles
        
        Args:
            max_results: Maximum number of results
            
        Returns:
            List of article dictionaries
        """
        query_parts = [
            '"3D cell culture"',
            '"drug-induced liver injury"',
            '"hepatic spheroids"',
            '"organ-on-chip"',
            '"in-vitro toxicology"',
            '"preclinical safety"',
            '"hepatotoxicity"',
            '"microphysiological systems"'
        ]
        
        query = " OR ".join(query_parts)
        return self.search_articles(query, max_results)
    
    def _fetch_article_details(self, article_ids: List[str]) -> List[Dict]:
        """Fetch details for specific article IDs"""
        try:
            detail_endpoint = f"{self.BASE_URL}/esummary.fcgi"
            detail_params = {
                'db': 'pubmed',
                'id': ','.join(article_ids),
                'retmode': 'json'
            }
            
            if self.api_key:
                detail_params['api_key'] = self.api_key
            
            detail_response = requests.get(detail_endpoint, params=detail_params, timeout=10)
            detail_response.raise_for_status()
            detail_data = detail_response.json()
            
            articles = []
            if 'result' in detail_data:
                for article_id, article_data in detail_data['result'].items():
                    if article_id != 'uids':
                        articles.append({
                            'pubmed_id': article_id,
                            'title': article_data.get('title', 'No title'),
                            'authors': article_data.get('authors', []),
                            'journal': article_data.get('source', 'Unknown'),
                            'pub_date': article_data.get('pubdate', ''),
                            'doi': article_data.get('elocationid', ''),
                            'url': f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                        })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"PubMed details error: {e}")
            return self._mock_articles()
    
    def _mock_articles(self) -> List[Dict]:
        """Generate mock articles for demo purposes"""
        journals = [
            "Toxicology in Vitro",
            "Drug Metabolism and Disposition",
            "Journal of Pharmacological and Toxicological Methods",
            "ALTEX - Alternatives to animal experimentation",
            "Toxicological Sciences"
        ]
        
        titles = [
            "3D Hepatic Spheroid Model for Drug-Induced Liver Injury Assessment",
            "Organ-on-Chip Technology for Preclinical Safety Evaluation",
            "Advanced In Vitro Models for Hepatotoxicity Prediction",
            "Microphysiological Systems in Toxicology: Current Status and Future Perspectives",
            "Integration of 3D Cell Culture Models in Drug Development Pipelines"
        ]
        
        articles = []
        for i in range(5):
            articles.append({
                'pubmed_id': f"1234567{i}",
                'title': titles[i],
                'authors': [{"name": "Researcher A"}, {"name": "Researcher B"}],
                'journal': journals[i],
                'pub_date': "2023",
                'doi': f"10.1234/tox.{i}",
                'url': f"https://pubmed.ncbi.nlm.nih.gov/1234567{i}/",
                'is_mock': True
            })
        
        return articles