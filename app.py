"""
Main Streamlit application for Lead Generation Agent
Clean and modular version
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from config.settings import Config
from agents.lead_agent import LeadGenerationAgent
from utils.data_generator import DataGenerator


# Page configuration
st.set_page_config(
    page_title="Akash EU Prime - Lead Generation Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-bottom: 1rem;
    }
    .api-status-connected {
        color: #10B981;
        font-weight: bold;
        padding: 2px 8px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 4px;
    }
    .api-status-disconnected {
        color: #EF4444;
        font-weight: bold;
        padding: 2px 8px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 4px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = LeadGenerationAgent()
    
    if 'leads_generated' not in st.session_state:
        st.session_state.leads_generated = False
    
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = {}


def render_header():
    """Render application header"""
    st.markdown("<h1 class='main-header'>🔬 Akash EU Prime - Lead Generation Web Agent</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>AI-powered lead identification, enrichment, and scoring for 3D in-vitro models</p>", 
                unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with controls and information"""
    with st.sidebar:
        st.markdown("### 🎯 Lead Criteria")
        
        # Input form for lead generation
        with st.form("criteria_form"):
            st.markdown("#### Target Roles")
            col1, col2 = st.columns(2)
            with col1:
                toxicology_role = st.checkbox("Toxicology", value=True)
                preclinical_role = st.checkbox("Preclinical Safety", value=True)
            with col2:
                hepatic_role = st.checkbox("Hepatic/3D Models", value=True)
            
            st.markdown("#### Data Sources")
            linkedin_source = st.checkbox("LinkedIn/Sales Navigator", value=True)
            pubmed_source = st.checkbox("PubMed/Google Scholar", value=True)
            conference_source = st.checkbox("Conference Lists", value=True)
            
            st.markdown("#### Generation Options")
            lead_count = st.slider("Number of leads", 10, 100, 50)
            
            generate_clicked = st.form_submit_button(
                "🚀 Generate Leads", 
                use_container_width=True,
                type="primary"
            )
        
        if generate_clicked:
            with st.spinner("Generating leads..."):
                st.session_state.agent.generate_leads(lead_count)
                st.session_state.leads_generated = True
                st.rerun()
        
        # API Status
        st.markdown("---")
        st.markdown("### 🔌 API Status")
        
        api_status = st.session_state.agent.get_api_status()
        for api_name, status in api_status.items():
            if status["enabled"]:
                st.markdown(f"**{status['name']}**: <span class='api-status-connected'>✅ Connected</span>", 
                          unsafe_allow_html=True)
            else:
                st.markdown(f"**{status['name']}**: <span class='api-status-disconnected'>❌ Not connected</span>", 
                          unsafe_allow_html=True)
            st.caption(status["purpose"])
        
        # Scoring Weights
        st.markdown("---")
        st.markdown("### 📊 Scoring Weights")
        
        weights = st.session_state.agent.get_scoring_weights()
        weights_df = pd.DataFrame({
            "Component": ["Role Fit", "Company Intent", "Technographic", "Location", "Scientific Intent"],
            "Weight": [f"{int(w*100)}%" for w in weights.values()]
        })
        st.dataframe(weights_df, use_container_width=True, hide_index=True)


def render_leads_dashboard():
    """Render main leads dashboard"""
    st.markdown("### 🎯 High-Probability Leads")
    
    # Quick stats
    stats = st.session_state.agent.get_lead_statistics()
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Leads", stats["total_leads"])
        with col2:
            st.metric("Avg Score", f"{stats['average_score']:.1f}")
        with col3:
            st.metric("High Probability", stats["high_probability_leads"])
        with col4:
            st.metric("Verified Emails", stats["verified_emails"])
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Search leads:",
            placeholder="Search by name, title, company, location...",
            key="search_input"
        )
    with col2:
        if st.button("🔄 Clear Filters", use_container_width=True):
            st.session_state.current_filters = {}
            st.rerun()
    
    # Apply search
    if search_query:
        filtered_leads = st.session_state.agent.search_leads(search_query)
    else:
        filtered_leads = st.session_state.agent.leads
    
    # Display leads table
    if filtered_leads.leads:
        df = filtered_leads.to_dataframe()
        
        # Configure columns for display
        column_config = {
            "rank": st.column_config.NumberColumn("Rank", width="small"),
            "name": st.column_config.TextColumn("Name"),
            "title": st.column_config.TextColumn("Title"),
            "company": st.column_config.TextColumn("Company"),
            "person_location": st.column_config.TextColumn("Person Location"),
            "company_hq": st.column_config.TextColumn("Company HQ"),
            "probability": st.column_config.ProgressColumn(
                "Probability",
                format="%d%%",
                min_value=0,
                max_value=100,
                width="medium"
            ),
            "email_confidence": st.column_config.ProgressColumn(
                "Email Confidence",
                format="%d%%",
                min_value=0,
                max_value=100,
                width="medium"
            ),
            "email": st.column_config.LinkColumn("Email", display_text="📧"),
            "linkedin": st.column_config.LinkColumn("LinkedIn", display_text="🔗")
        }
        
        # Select columns to display
        display_columns = [
            "rank", "name", "title", "company", "person_location", 
            "company_hq", "probability", "email_confidence", "email", "linkedin"
        ]
        
        st.dataframe(
            df[display_columns],
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
        
        # Export buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = st.session_state.agent.export_leads("csv")
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_data = st.session_state.agent.export_leads("json")
            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.session_state.agent.generate_leads(50)
                st.rerun()
    else:
        st.warning("No leads found. Generate some leads first!")
        
        # Show sample data if no leads
        if not st.session_state.leads_generated:
            data_gen = DataGenerator()
            sample_scores = data_gen.generate_sample_scores()
            
            st.info("### Sample Scoring Examples")
            for example in sample_scores:
                with st.expander(example["description"]):
                    col1, col2 = st.columns(2)
                    with col1:
                        for component, score in example["scores"].items():
                            st.metric(component.replace("_", " ").title(), score)
                    with col2:
                        st.metric("Total Score", example["total"])


def render_analytics_tab():
    """Render analytics tab"""
    st.markdown("### 📊 Lead Analytics")
    
    stats = st.session_state.agent.get_lead_statistics()
    
    if not stats:
        st.warning("No data available. Generate leads first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution chart
        st.markdown("#### Score Distribution")
        
        dist_data = pd.DataFrame({
            "Category": list(stats["score_distribution"].keys()),
            "Count": list(stats["score_distribution"].values())
        })
        
        fig = px.bar(
            dist_data, 
            x="Category", 
            y="Count",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top companies
        st.markdown("#### Top Companies")
        if stats["top_companies"]:
            companies_df = pd.DataFrame({
                "Company": list(stats["top_companies"].keys()),
                "Lead Count": list(stats["top_companies"].values())
            })
            st.dataframe(companies_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Component scores
        st.markdown("#### Scoring Components")
        
        # Get component averages
        df = st.session_state.agent.leads.to_dataframe()
        component_avgs = {
            "Role Fit": df["role_fit_score"].mean(),
            "Company Intent": df["company_intent_score"].mean(),
            "Technographic": df["technographic_score"].mean(),
            "Location": df["location_score"].mean(),
            "Scientific Intent": df["scientific_intent_score"].mean()
        }
        
        comp_df = pd.DataFrame({
            "Component": list(component_avgs.keys()),
            "Average Score": list(component_avgs.values())
        })
        
        fig = px.bar(
            comp_df,
            x="Component",
            y="Average Score",
            color="Component",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent publications
        st.markdown("#### Recent Publications")
        publications = st.session_state.agent.get_recent_publications()
        
        if publications:
            for pub in publications[:3]:  # Show first 3
                with st.expander(pub["title"][:50] + "..." if len(pub["title"]) > 50 else pub["title"]):
                    st.write(f"**Journal**: {pub['journal']}")
                    st.write(f"**Date**: {pub['pub_date']}")
                    if pub.get('url'):
                        st.markdown(f"[Read Paper]({pub['url']})")


def render_configuration_tab():
    """Render configuration tab"""
    st.markdown("### ⚙️ Configuration")
    
    # API Testing Section
    st.markdown("#### 🧪 API Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Hunter.io Test")
        test_email = st.text_input("Email to verify:", "test@company.com")
        
        if st.button("Test Email Verification", use_container_width=True):
            if Config.HUNTER_API_KEY:
                with st.spinner("Verifying..."):
                    from api.hunter_client import HunterClient
                    hunter = HunterClient()
                    result = hunter.verify_email(test_email)
                    
                    if result.get("success"):
                        st.success(f"✅ Status: {result.get('status', 'Unknown')}")
                        st.info(f"Score: {result.get('score', 0)}/100")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown')}")
            else:
                st.warning("Hunter.io API key not configured")
    
    with col2:
        st.markdown("##### PubMed Test")
        if st.button("Test PubMed Connection", use_container_width=True):
            with st.spinner("Searching recent publications..."):
                from api.pubmed_client import PubMedClient
                pubmed = PubMedClient()
                articles = pubmed.search_toxicology_articles(max_results=3)
                
                if articles:
                    st.success(f"✅ Found {len(articles)} recent articles")
                    for article in articles[:2]:
                        st.caption(f"• {article['title'][:60]}...")
                else:
                    st.error("❌ No articles found")
    
    # Environment Setup
    st.markdown("---")
    with st.expander("📁 Environment Setup", expanded=False):
        st.markdown("""
        ### `.env` File Configuration
        
        Create a `.env` file in your project root:
        
        ```env
        # Required for email verification
        HUNTER_API_KEY=your_key_here
        
        # Recommended for LinkedIn data
        PROXYCURL_API_KEY=your_key_here
        
        # Optional for enhanced features
        CLEARBIT_API_KEY=your_key_here
        PUBMED_API_KEY=your_key_here
        
        # App settings
        DEBUG=False
        MAX_LEADS=1000
        RATE_LIMIT_DELAY=1.0
        ```
        
        **Security Note**: Add `.env` to `.gitignore` to prevent exposing API keys.
        """)
    
    # Scoring Weights Configuration
    st.markdown("---")
    st.markdown("#### ⚖️ Scoring Weights Configuration")
    
    current_weights = st.session_state.agent.get_scoring_weights()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        role_weight = st.number_input("Role Fit %", 0, 100, 
                                     int(current_weights["role_fit"] * 100))
    with col2:
        company_weight = st.number_input("Company Intent %", 0, 100,
                                        int(current_weights["company_intent"] * 100))
    with col3:
        techno_weight = st.number_input("Technographic %", 0, 100,
                                       int(current_weights["technographic"] * 100))
    with col4:
        location_weight = st.number_input("Location %", 0, 100,
                                         int(current_weights["location"] * 100))
    with col5:
        scientific_weight = st.number_input("Scientific Intent %", 0, 100,
                                          int(current_weights["scientific_intent"] * 100))
    
    total = role_weight + company_weight + techno_weight + location_weight + scientific_weight
    
    if total != 100:
        st.error(f"⚠️ Weights must sum to 100% (Current: {total}%)")
    else:
        st.success("✅ Weights properly configured!")
    
    if st.button("💾 Save Configuration", use_container_width=True):
        st.success("Configuration saved! (Note: In production, this would update config file)")


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📋 Leads Dashboard", "📊 Analytics", "⚙️ Configuration"])
    
    # Render tabs
    with tab1:
        render_leads_dashboard()
    
    with tab2:
        render_analytics_tab()
    
    with tab3:
        render_configuration_tab()


if __name__ == "__main__":
    main()