"""
Configuration settings for the Lead Generation Agent
Centralized configuration management
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY", "")
    CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY", "")
    CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY", "")
    
    # App Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MAX_LEADS = int(os.getenv("MAX_LEADS", "1000"))
    RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
    
    # Scoring Weights (from requirements)
    SCORING_WEIGHTS = {
        "role_fit": 0.30,
        "company_intent": 0.20,
        "technographic": 0.15,
        "location": 0.10,
        "scientific_intent": 0.40
    }
    
    # Biotech hubs for location scoring
    BIOTECH_HUBS = [
        "Boston", "Bay Area", "Basel", "UK Triangle", "Cambridge MA",
        "San Diego", "Research Triangle Park", "Seattle", "New York"
    ]
    
    # Target roles and keywords
    TARGET_ROLES = [
        "Director of Toxicology",
        "Head of Preclinical Safety",
        "Senior Scientist - Hepatic Models",
        "Principal Investigator - 3D Cell Culture",
        "VP Drug Discovery",
        "Research Lead - In Vitro Models",
        "Toxicology Manager",
        "Senior Director of Safety Assessment",
        "Lab Head - Organ-on-Chip",
        "Associate Director - DILI"
    ]
    
    TARGET_COMPANIES = [
        "Biogen", "Moderna", "Novartis", "Pfizer", "Johnson & Johnson",
        "Merck", "GSK", "Roche", "Sanofi", "AstraZeneca",
        "Vertex Pharmaceuticals", "Regeneron", "Bristol Myers Squibb",
        "Genentech", "Amgen", "Biocoat", "Emulate Inc", "CN Bio",
        "Mimetas", "TissUse"
    ]
    
    # Scientific keywords
    SCIENTIFIC_KEYWORDS = [
        "3D cell culture", "Drug-Induced Liver Injury", "Hepatic spheroids",
        "Organ-on-chip", "in-vitro models", "toxicology", "preclinical safety",
        "NAMs", "hepatotoxicity", "microphysiological systems"
    ]
    
    @classmethod
    def get_api_status(cls) -> Dict[str, Dict[str, Any]]:
        """Get status of all configured APIs"""
        return {
            "hunter": {
                "enabled": bool(cls.HUNTER_API_KEY),
                "name": "Hunter.io",
                "purpose": "Email verification & enrichment"
            },
            "proxycurl": {
                "enabled": bool(cls.PROXYCURL_API_KEY),
                "name": "Proxycurl",
                "purpose": "LinkedIn profile data"
            },
            "pubmed": {
                "enabled": True,  # Public API always available
                "name": "PubMed",
                "purpose": "Scientific publications"
            },
            "clearbit": {
                "enabled": bool(cls.CLEARBIT_API_KEY),
                "name": "Clearbit",
                "purpose": "Company data enrichment"
            }
        }