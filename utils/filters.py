"""
Filtering utilities for leads
"""

import re
from typing import List, Dict, Optional, Callable
from models.lead import Lead, LeadCollection


class LeadFilter:
    """Filter leads based on various criteria"""
    
    @staticmethod
    def filter_by_search(leads: LeadCollection, search_query: str) -> LeadCollection:
        """
        Filter leads by search query
        
        Args:
            leads: LeadCollection to filter
            search_query: Search string
            
        Returns:
            Filtered LeadCollection
        """
        if not search_query:
            return leads
        
        search_query = search_query.lower()
        filtered_leads = []
        
        for lead in leads.leads:
            # Search in multiple fields
            search_fields = [
                lead.name,
                lead.title,
                lead.company,
                lead.person_location,
                lead.company_hq,
                lead.uses_tech or ""
            ]
            
            if any(search_query in field.lower() for field in search_fields):
                filtered_leads.append(lead)
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_score_range(leads: LeadCollection, min_score: int = 0, 
                            max_score: int = 100) -> LeadCollection:
        """
        Filter leads by score range
        
        Args:
            leads: LeadCollection to filter
            min_score: Minimum score
            max_score: Maximum score
            
        Returns:
            Filtered LeadCollection
        """
        filtered_leads = [
            lead for lead in leads.leads
            if min_score <= lead.probability <= max_score
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_location(leads: LeadCollection, location: str) -> LeadCollection:
        """
        Filter leads by location
        
        Args:
            leads: LeadCollection to filter
            location: Location to filter by
            
        Returns:
            Filtered LeadCollection
        """
        if not location or location.lower() == "all":
            return leads
        
        location_lower = location.lower()
        filtered_leads = [
            lead for lead in leads.leads
            if location_lower in lead.person_location.lower() or 
               location_lower in lead.company_hq.lower()
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_company(leads: LeadCollection, company: str) -> LeadCollection:
        """
        Filter leads by company
        
        Args:
            leads: LeadCollection to filter
            company: Company name to filter by
            
        Returns:
            Filtered LeadCollection
        """
        if not company or company.lower() == "all":
            return leads
        
        company_lower = company.lower()
        filtered_leads = [
            lead for lead in leads.leads
            if company_lower in lead.company.lower()
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_funding(leads: LeadCollection, funding_round: str) -> LeadCollection:
        """
        Filter leads by funding round
        
        Args:
            leads: LeadCollection to filter
            funding_round: Funding round to filter by
            
        Returns:
            Filtered LeadCollection
        """
        if not funding_round or funding_round.lower() == "all":
            return leads
        
        filtered_leads = [
            lead for lead in leads.leads
            if lead.funding_round == funding_round
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_publications(leads: LeadCollection, has_paper: bool) -> LeadCollection:
        """
        Filter leads by publication status
        
        Args:
            leads: LeadCollection to filter
            has_paper: Whether to filter for leads with papers
            
        Returns:
            Filtered LeadCollection
        """
        filtered_leads = [
            lead for lead in leads.leads
            if lead.recent_paper == has_paper
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def filter_by_email_verification(leads: LeadCollection, verified_only: bool) -> LeadCollection:
        """
        Filter leads by email verification status
        
        Args:
            leads: LeadCollection to filter
            verified_only: Whether to filter for verified emails only
            
        Returns:
            Filtered LeadCollection
        """
        if not verified_only:
            return leads
        
        filtered_leads = [
            lead for lead in leads.leads
            if lead.email_verified
        ]
        
        return LeadCollection(filtered_leads)
    
    @staticmethod
    def apply_multiple_filters(leads: LeadCollection, filters: Dict) -> LeadCollection:
        """
        Apply multiple filters to leads
        
        Args:
            leads: LeadCollection to filter
            filters: Dictionary of filter criteria
            
        Returns:
            Filtered LeadCollection
        """
        filtered = leads
        
        # Apply filters in a specific order
        if filters.get("search_query"):
            filtered = LeadFilter.filter_by_search(filtered, filters["search_query"])
        
        if filters.get("min_score") is not None or filters.get("max_score") is not None:
            min_score = filters.get("min_score", 0)
            max_score = filters.get("max_score", 100)
            filtered = LeadFilter.filter_by_score_range(filtered, min_score, max_score)
        
        if filters.get("location"):
            filtered = LeadFilter.filter_by_location(filtered, filters["location"])
        
        if filters.get("company"):
            filtered = LeadFilter.filter_by_company(filtered, filters["company"])
        
        if filters.get("funding_round"):
            filtered = LeadFilter.filter_by_funding(filtered, filters["funding_round"])
        
        if filters.get("has_paper") is not None:
            filtered = LeadFilter.filter_by_publications(filtered, filters["has_paper"])
        
        if filters.get("verified_only"):
            filtered = LeadFilter.filter_by_email_verification(filtered, True)
        
        return filtered
    
    @staticmethod
    def get_filter_options(leads: LeadCollection) -> Dict:
        """
        Get available filter options from leads
        
        Args:
            leads: LeadCollection to analyze
            
        Returns:
            Dictionary of filter options
        """
        if not leads.leads:
            return {}
        
        locations = sorted(set(lead.person_location for lead in leads.leads))
        companies = sorted(set(lead.company for lead in leads.leads))
        funding_rounds = sorted(set(lead.funding_round for lead in leads.leads if lead.funding_round))
        
        return {
            "locations": ["All"] + locations,
            "companies": ["All"] + companies,
            "funding_rounds": ["All"] + funding_rounds,
            "min_score": 0,
            "max_score": 100,
            "has_papers_count": sum(1 for lead in leads.leads if lead.recent_paper),
            "verified_emails_count": sum(1 for lead in leads.leads if lead.email_verified)
        }