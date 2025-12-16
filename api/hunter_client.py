"""
Hunter.io API client for email verification and enrichment
"""

import requests
import time
from typing import Dict, Optional, List
from config.settings import Config
import random

class HunterClient:
    """Client for Hunter.io API"""
    
    BASE_URL = "https://api.hunter.io/v2"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.HUNTER_API_KEY
        self.last_call_time = 0
        self.rate_limit_delay = Config.RATE_LIMIT_DELAY
    
    def _apply_rate_limit(self):
        """Apply rate limiting between API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_call_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_call_time = time.time()
    
    def verify_email(self, email: str) -> Dict:
        """
        Verify an email address
        
        Args:
            email: Email address to verify
            
        Returns:
            Dictionary with verification results
        """
        if not self.api_key:
            return self._mock_verification(email)
        
        self._apply_rate_limit()
        
        try:
            endpoint = f"{self.BASE_URL}/email-verifier"
            params = {
                "email": email,
                "api_key": self.api_key
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "email": email,
                "status": data.get("data", {}).get("status"),
                "score": data.get("data", {}).get("score", 0),
                "result": data.get("data", {}).get("result"),
                "is_valid": data.get("data", {}).get("status") == "valid",
                "sources": data.get("data", {}).get("sources", []),
                "verification_date": data.get("data", {}).get("verification_date")
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Hunter.io verification failed for {email}: {e}")
            return self._mock_verification(email)
    
    def find_email(self, domain: str, first_name: str, last_name: str) -> Dict:
        """
        Find email for a person
        
        Args:
            domain: Company domain
            first_name: First name
            last_name: Last name
            
        Returns:
            Dictionary with email finding results
        """
        if not self.api_key:
            return self._mock_email_find(domain, first_name, last_name)
        
        self._apply_rate_limit()
        
        try:
            endpoint = f"{self.BASE_URL}/email-finder"
            params = {
                "domain": domain,
                "first_name": first_name,
                "last_name": last_name,
                "api_key": self.api_key
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("data", {}).get("email"):
                return {
                    "success": True,
                    "email": data["data"]["email"],
                    "score": data["data"].get("score", 0),
                    "sources": data["data"].get("sources", []),
                    "first_name": data["data"].get("first_name"),
                    "last_name": data["data"].get("last_name"),
                    "domain": data["data"].get("domain"),
                    "position": data["data"].get("position"),
                    "company": data["data"].get("company")
                }
            else:
                return {
                    "success": False,
                    "email": None,
                    "reason": data.get("errors", [{}])[0].get("details")
                }
                
        except requests.exceptions.RequestException as e:
            print(f"Hunter.io email finder failed: {e}")
            return self._mock_email_find(domain, first_name, last_name)
    
    def test_connection(self) -> Dict:
        """Test connection to Hunter.io API"""
        if not self.api_key:
            return {"success": False, "message": "No API key configured"}
        
        try:
            endpoint = f"{self.BASE_URL}/account"
            params = {"api_key": self.api_key}
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "message": f"Connected to Hunter.io. Plan: {data.get('data', {}).get('plan_name', 'Unknown')}",
                "credits_remaining": data.get("data", {}).get("calls", {}).get("remaining", 0),
                "plan": data.get("data", {}).get("plan_name", "Unknown"),
                "calls_used": data.get("data", {}).get("calls", {}).get("used", 0)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }

    def _mock_verification(self, email: str) -> Dict:
        """Mock verification for demo purposes"""
        return {
            "success": True,
            "email": email,
            "status": "valid" if "@" in email else "invalid",
            "score": random.randint(70, 100) if "@" in email else random.randint(10, 50),
            "is_valid": "@" in email,
            "result": "deliverable" if "@" in email else "undeliverable",
            "sources": [{"domain": "example.com", "uri": "https://example.com"}],
            "verification_date": time.strftime("%Y-%m-%d"),
            "is_mock": True
        }
    
    def _mock_email_find(self, domain: str, first_name: str, last_name: str) -> Dict:
        """Mock email finding for demo purposes"""
        return {
            "success": True,
            "email": f"{first_name.lower()}.{last_name.lower()}@{domain}",
            "score": random.randint(70, 100),
            "sources": [],
            "first_name": first_name,
            "last_name": last_name,
            "domain": domain,
            "position": "Senior Scientist",
            "company": domain.replace(".com", "").title(),
            "is_mock": True
        }