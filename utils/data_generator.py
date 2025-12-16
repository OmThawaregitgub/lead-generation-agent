"""
Mock data generation utilities
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
from config.settings import Config
from models.lead import Lead


class DataGenerator:
    """Generate mock lead data for demonstration"""
    
    FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", 
                   "Riley", "Drew", "Quinn", "Blake", "Hayden"]
    
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones",
                  "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    def __init__(self):
        self.hunter_client = None  # Will be set if API available
        self.scoring_agent = None  # Will be set by main agent
    
    def set_hunter_client(self, hunter_client):
        """Set Hunter.io client for email verification"""
        self.hunter_client = hunter_client
    
    def set_scoring_agent(self, scoring_agent):
        """Set scoring agent for lead scoring"""
        self.scoring_agent = scoring_agent
    
    def generate_leads(self, count: int = 50) -> List[Lead]:
        """
        Generate mock leads
        
        Args:
            count: Number of leads to generate
            
        Returns:
            List of Lead objects
        """
        leads = []
        
        for i in range(count):
            lead = self._generate_single_lead(i + 1)
            leads.append(lead)
        
        # Sort by score and assign ranks
        leads.sort(key=lambda x: x.total_score, reverse=True)
        for idx, lead in enumerate(leads):
            lead.rank = idx + 1
        
        return leads
    
    def _generate_single_lead(self, lead_id: int) -> Lead:
        """Generate a single lead with realistic data"""
        # Basic information
        first_name = random.choice(self.FIRST_NAMES)
        last_name = random.choice(self.LAST_NAMES)
        title = random.choice(Config.TARGET_ROLES)
        company = random.choice(Config.TARGET_COMPANIES)
        
        # Location
        person_location = random.choice(
            Config.BIOTECH_HUBS + ["Remote Colorado", "Remote Oregon", 
                                  "Remote Florida", "Remote Texas"]
        )
        company_hq = random.choice(Config.BIOTECH_HUBS)
        
        # Generate email
        email = self._generate_email(first_name, last_name, company)
        
        # Verify email if Hunter.io client is available
        email_verified = False
        email_confidence = random.randint(50, 100)
        
        if self.hunter_client and random.random() > 0.7:  # 30% chance to use API
            try:
                verification = self.hunter_client.verify_email(email)
                email_verified = verification.get("is_valid", False)
                email_confidence = verification.get("score", email_confidence)
            except:
                pass
        
        # Professional details
        recent_paper = random.choice([True, False])
        funding_round = random.choice(["Series A", "Series B", "Series C", "Seed", "None"])
        uses_tech = random.choice(["in-vitro models", "NAMs", "Organ-on-chip", "Hepatic spheroids"])
        
        # Calculate scores if scoring agent is available
        if self.scoring_agent:
            role_fit_score = self.scoring_agent.calculate_role_fit_score(title)
            company_intent_score = self.scoring_agent.calculate_company_intent_score(company)
            technographic_score = self.scoring_agent.calculate_technographic_score()
            location_score = self.scoring_agent.calculate_location_score(person_location)
            scientific_intent_score = self.scoring_agent.calculate_scientific_intent_score(recent_paper)
            
            scores = {
                "role_fit_score": role_fit_score,
                "company_intent_score": company_intent_score,
                "technographic_score": technographic_score,
                "location_score": location_score,
                "scientific_intent_score": scientific_intent_score
            }
            
            total_score = self.scoring_agent.calculate_total_score(scores)
        else:
            # Fallback scoring
            role_fit_score = random.randint(20, 100)
            company_intent_score = random.randint(20, 100)
            technographic_score = random.randint(20, 100)
            location_score = random.randint(20, 100)
            scientific_intent_score = random.randint(20, 100)
            
            total_score = round(
                role_fit_score * 0.30 +
                company_intent_score * 0.20 +
                technographic_score * 0.15 +
                location_score * 0.10 +
                scientific_intent_score * 0.40,
                1
            )
        
        # Create lead
        lead = Lead(
            id=lead_id,
            name=f"{first_name} {last_name}",
            title=title,
            company=company,
            email=email,
            email_verified=email_verified,
            email_confidence=email_confidence,
            phone=f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            linkedin=f"https://linkedin.com/in/{first_name.lower()}{last_name.lower()}",
            person_location=person_location,
            company_hq=company_hq,
            recent_paper=recent_paper,
            funding_round=funding_round,
            uses_tech=uses_tech,
            last_activity=(datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            role_fit_score=role_fit_score,
            company_intent_score=company_intent_score,
            technographic_score=technographic_score,
            location_score=location_score,
            scientific_intent_score=scientific_intent_score,
            total_score=total_score,
            probability=round(total_score),
            data_source="Mock Data" + (" + Hunter.io" if email_verified else "")
        )
        
        return lead
    
    def _generate_email(self, first_name: str, last_name: str, company: str) -> str:
        """Generate realistic email address"""
        company_domain = company.lower().replace(" ", "").replace("&", "").replace(".", "")
        
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{company_domain}.com",
            f"{first_name[0].lower()}{last_name.lower()}@{company_domain}.com",
            f"{first_name.lower()}{last_name[0].lower()}@{company_domain}.com",
            f"{first_name.lower()}_{last_name.lower()}@{company_domain}.com"
        ]
        
        return random.choice(formats)
    
    def generate_sample_scores(self) -> List[Dict]:
        """Generate sample scoring examples as per requirements"""
        return [
            {
                "description": "Junior scientist at non-funded startup",
                "scores": {
                    "role_fit": 20,
                    "company_intent": 10,
                    "technographic": 30,
                    "location": 20,
                    "scientific_intent": 15
                },
                "total": 15,
                "explanation": "Low scores across all criteria due to junior role and no funding"
            },
            {
                "description": "Senior scientist at growing biotech in hub location",
                "scores": {
                    "role_fit": 65,
                    "company_intent": 50,
                    "technographic": 70,
                    "location": 80,
                    "scientific_intent": 60
                },
                "total": 65,
                "explanation": "Good role fit and location, moderate scientific output"
            },
            {
                "description": "Director at Series B biotech in Cambridge with liver paper",
                "scores": {
                    "role_fit": 95,
                    "company_intent": 90,
                    "technographic": 85,
                    "location": 95,
                    "scientific_intent": 100
                },
                "total": 95,
                "explanation": "Perfect fit: senior role, funded company, hub location, recent publications"
            }
        ]