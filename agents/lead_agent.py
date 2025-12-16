"""
Main lead generation agent orchestrating all components
"""

from typing import List, Dict, Optional
import pandas as pd

from config.settings import Config
from models.lead import Lead, LeadCollection
from agents.scoring_agent import ScoringAgent
from api.hunter_client import HunterClient
from api.pubmed_client import PubMedClient
from utils.data_generator import DataGenerator
from utils.filters import LeadFilter


class LeadGenerationAgent:
    """Main agent orchestrating lead generation, enrichment, and scoring"""
    
    def __init__(self):
        """Initialize all components"""
        self.config = Config
        
        # Initialize clients
        self.hunter_client = HunterClient() if Config.HUNTER_API_KEY else None
        self.pubmed_client = PubMedClient()
        
        # Initialize agents
        self.scoring_agent = ScoringAgent()
        
        # Initialize utilities
        self.data_generator = DataGenerator()
        self.data_generator.set_scoring_agent(self.scoring_agent)
        
        if self.hunter_client:
            self.data_generator.set_hunter_client(self.hunter_client)
        
        # Data storage
        self.leads = LeadCollection()
        self.publications = []
    
    def generate_leads(self, count: int = 50) -> LeadCollection:
        """
        Generate new leads
        
        Args:
            count: Number of leads to generate
            
        Returns:
            LeadCollection of generated leads
        """
        # Generate mock leads
        self.leads = LeadCollection(self.data_generator.generate_leads(count))
        
        # Fetch recent publications (for enrichment)
        if self.pubmed_client:
            self.publications = self.pubmed_client.search_toxicology_articles(max_results=10)
        
        return self.leads
    
    def search_leads(self, search_query: str) -> LeadCollection:
        """
        Search leads by query
        
        Args:
            search_query: Search string
            
        Returns:
            Filtered LeadCollection
        """
        return LeadFilter.filter_by_search(self.leads, search_query)
    
    def filter_leads(self, **filters) -> LeadCollection:
        """
        Filter leads by multiple criteria
        
        Args:
            **filters: Filter criteria
            
        Returns:
            Filtered LeadCollection
        """
        return LeadFilter.apply_multiple_filters(self.leads, filters)
    
    def get_lead_statistics(self) -> Dict:
        """
        Get statistics about current leads
        
        Returns:
            Dictionary of statistics
        """
        if not self.leads.leads:
            return {}
        
        df = self.leads.to_dataframe()
        
        stats = {
            "total_leads": len(self.leads),
            "average_score": df["total_score"].mean(),
            "high_probability_leads": len(df[df["probability"] >= 80]),
            "with_papers": df["recent_paper"].sum(),
            "verified_emails": df["email_verified"].sum(),
            "in_hubs": len(df[df["location_score"] >= 80]),
            "top_companies": df["company"].value_counts().head(5).to_dict(),
            "score_distribution": {
                "low": len(df[df["probability"] < 30]),
                "medium": len(df[(df["probability"] >= 30) & (df["probability"] < 60)]),
                "high": len(df[(df["probability"] >= 60) & (df["probability"] < 80)]),
                "very_high": len(df[df["probability"] >= 80])
            }
        }
        
        return stats
    
    def get_api_status(self) -> Dict:
        """
        Get status of all APIs
        
        Returns:
            Dictionary of API statuses
        """
        api_status = Config.get_api_status()
        
        # Test Hunter.io connection if available
        if self.hunter_client:
            test_result = self.hunter_client.test_connection()
            api_status["hunter"]["test_result"] = test_result
        
        return api_status
    
    def enrich_lead_with_hunter(self, lead: Lead) -> Lead:
        """
        Enrich a lead with Hunter.io data
        
        Args:
            lead: Lead to enrich
            
        Returns:
            Enriched lead
        """
        if not self.hunter_client:
            return lead
        
        try:
            # Verify email
            verification = self.hunter_client.verify_email(lead.email)
            
            lead.email_verified = verification.get("is_valid", False)
            lead.email_confidence = verification.get("score", lead.email_confidence)
            
            # Update data source
            if not verification.get("is_mock", True):
                lead.data_source = "Hunter.io API"
            
        except Exception as e:
            print(f"Error enriching lead {lead.id}: {e}")
        
        return lead
    
    def get_recent_publications(self) -> List[Dict]:
        """
        Get recent publications related to toxicology and 3D models
        
        Returns:
            List of publication dictionaries
        """
        return self.publications
    
    def export_leads(self, format: str = "csv") -> bytes:
        """
        Export leads in specified format
        
        Args:
            format: Export format (csv, json)
            
        Returns:
            Bytes of exported data
        """
        df = self.leads.to_dataframe()
        
        if format.lower() == "csv":
            return df.to_csv(index=False).encode('utf-8')
        elif format.lower() == "json":
            return df.to_json(orient="records", indent=2).encode('utf-8')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_scoring_weights(self) -> Dict:
        """
        Get current scoring weights
        
        Returns:
            Dictionary of scoring weights
        """
        return self.scoring_agent.weights
    
    def get_filter_options(self) -> Dict:
        """
        Get available filter options
        
        Returns:
            Dictionary of filter options
        """
        return LeadFilter.get_filter_options(self.leads)