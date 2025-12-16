"""
Lead data models and schemas
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd


@dataclass
class Lead:
    """Lead data model"""
    
    # Basic Information
    id: int
    name: str
    title: str
    company: str
    
    # Contact Information
    email: str
    email_verified: bool = False
    email_confidence: int = 0
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    
    # Location Information
    person_location: str
    company_hq: str
    
    # Professional Details
    recent_paper: bool = False
    funding_round: Optional[str] = None
    uses_tech: Optional[str] = None
    last_activity: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    # Scoring Components
    role_fit_score: int = 0
    company_intent_score: int = 0
    technographic_score: int = 0
    location_score: int = 0
    scientific_intent_score: int = 0
    
    # Calculated Scores
    total_score: float = 0.0
    probability: int = 0
    rank: int = 0
    
    # Metadata
    data_source: str = "Mock Data"
    enrichment_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Lead':
        """Create Lead instance from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> Dict:
        """Convert Lead to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "company": self.company,
            "email": self.email,
            "email_verified": self.email_verified,
            "email_confidence": self.email_confidence,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "person_location": self.person_location,
            "company_hq": self.company_hq,
            "recent_paper": self.recent_paper,
            "funding_round": self.funding_round,
            "uses_tech": self.uses_tech,
            "last_activity": self.last_activity,
            "role_fit_score": self.role_fit_score,
            "company_intent_score": self.company_intent_score,
            "technographic_score": self.technographic_score,
            "location_score": self.location_score,
            "scientific_intent_score": self.scientific_intent_score,
            "total_score": self.total_score,
            "probability": self.probability,
            "rank": self.rank,
            "data_source": self.data_source
        }


class LeadCollection:
    """Collection of leads with utility methods"""
    
    def __init__(self, leads: List[Lead] = None):
        self.leads = leads or []
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert leads to pandas DataFrame"""
        if not self.leads:
            return pd.DataFrame()
        
        return pd.DataFrame([lead.to_dict() for lead in self.leads])
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'LeadCollection':
        """Create LeadCollection from DataFrame"""
        leads = []
        for _, row in df.iterrows():
            lead_data = row.to_dict()
            leads.append(Lead.from_dict(lead_data))
        return cls(leads)
    
    def filter(self, **kwargs) -> 'LeadCollection':
        """Filter leads based on criteria"""
        filtered_leads = []
        for lead in self.leads:
            include = True
            for key, value in kwargs.items():
                if hasattr(lead, key):
                    lead_value = getattr(lead, key)
                    if isinstance(value, (list, tuple)):
                        if lead_value not in value:
                            include = False
                            break
                    elif lead_value != value:
                        include = False
                        break
            if include:
                filtered_leads.append(lead)
        
        return LeadCollection(filtered_leads)
    
    def sort_by_score(self, ascending: bool = False) -> 'LeadCollection':
        """Sort leads by total score"""
        sorted_leads = sorted(self.leads, key=lambda x: x.total_score, reverse=not ascending)
        return LeadCollection(sorted_leads)
    
    def __len__(self) -> int:
        return len(self.leads)
    
    def __getitem__(self, idx) -> Lead:
        return self.leads[idx]