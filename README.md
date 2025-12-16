
---

Lead Generation Web Agent for Akash EU PrimeA sophisticated web agent for identifying, enriching, and ranking high-probability leads for 3D in-vitro models in toxicology and preclinical safety research.

---

##🎯 Features###Core Capabilities* **Lead Identification**: Scan multiple sources for target roles (Director of Toxicology, Head of Preclinical Safety, etc.)
* **Data Enrichment**: Fetch business emails, phone numbers, locations using Hunter.io and other APIs
* **Intelligent Scoring**: Propensity-to-Buy score (0-100) with weighted criteria
* **Web Dashboard**: Interactive Streamlit app with filtering, search, and export

###Scoring Criteria (Exact Weights)| Signal Category | Weight | Example Criteria |
| --- | --- | --- |
| **Role Fit** | **30%** | Title has Toxicology/Safety/Hepatic/3D |
| **Scientific Intent** | **40%** | Recent paper on liver toxicity |
| **Company Intent** | **20%** | Recent Series A/B funding |
| **Technographic** | **15%** | Uses in-vitro/NAMs |
| **Location** | **10%** | Hub location (Boston, Bay Area, Basel, UK Triangle) |

> **Note:** The total weight of the listed categories is 30\% + 40\% + 20\% + 15\% + 10\% = 115\%. This should be reviewed to ensure it sums to 100\% for a proper weighted average (or adjust the definition of the final score).

---

##🚀 Quick Start###1. Installation```bash
git clone <repository-url>
cd lead-generation-agent
pip install -r requirements.txt

```

###2. ConfigurationCreate a `.env` file in the project root:

```env
# Required for email verification
HUNTER_API_KEY=your_hunter_api_key_here

# Recommended for LinkedIn data
PROXYCURL_API_KEY=your_proxycurl_api_key_here

# Optional for enhanced features
CLEARBIT_API_KEY=your_key_here
PUBMED_API_KEY=your_key_here

# App settings
DEBUG=False
MAX_LEADS=1000
RATE_LIMIT_DELAY=1.0

```

###3. Run Application```bash
streamlit run app.py

```

---

##📁 Project Structure```text
lead-generation-agent/
├── app.py                      # Main Streamlit application
├── config/
│   └── settings.py            # Configuration management
├── agents/
│   ├── lead_agent.py          # Main orchestration agent
│   └── scoring_agent.py       # Lead scoring logic
├── api/
│   ├── hunter_client.py       # Hunter.io API integration
│   ├── pubmed_client.py       # PubMed API integration
│   └── proxycurl_client.py    # LinkedIn data integration
├── models/
│   └── lead.py               # Data models and schemas
├── utils/
│   ├── data_generator.py     # Mock data generation
│   └── filters.py            # Filtering utilities
└── requirements.txt

```

> **Key Benefits of This Structure:**
> * **Modularity**: Each component in its own file
> * **Maintainability**: Easy to update individual parts
> * **Scalability**: Add new APIs or features easily
> * **Testability**: Each module can be tested independently
> 
> 

---

##🔌 API Integrations| API Name | Purpose | Tier/Cost | Key Link |
| --- | --- | --- | --- |
| **Hunter.io** (Required) | Email verification and enrichment | Free tier: 25 searches/month | [https://hunter.io](https://hunter.io) |
| **Proxycurl** (Recommended) | LinkedIn data | Free tier: 10 credits/day | [https://nubela.co/proxycurl](https://nubela.co/proxycurl) |
| Clearbit (Optional) | Company data enrichment | N/A | N/A |
| PubMed (Optional) | Scientific publications | Free public API | N/A |
| Crunchbase (Optional) | Company funding data | N/A | N/A |

---

##🎮 Usage###Generating Leads1. Open the Streamlit app
2. Configure target roles in the sidebar
3. Click "**Generate Leads**"
4. View ranked leads in the dashboard

###Filtering and Searching* Use the search bar for quick text search
* Apply advanced filters in the dashboard
* Sort by any column

###Exporting Data* Download CSV/JSON with one click
* Export filtered or all leads
* Automatic timestamp in filenames

---

##📊 Sample Scoring Examples| Scenario | Total Score | Explanation |
| --- | --- | --- |
| Junior scientist at non-funded startup | ~15/100 | Low scores across all criteria |
| Senior scientist at growing biotech | ~65/100 | Good role fit and location |
| Director at Series B biotech with liver paper | ~95/100 | Perfect fit across all criteria |

---

##🚀 Deployment###Streamlit Cloud1. Push to GitHub
2. Connect at [https://share.streamlit.io](https://share.streamlit.io)
3. Set secrets in `.streamlit/secrets.toml`

###Local Production```bash
# Run with production settings
STREAMLIT_SERVER_PORT=8501 streamlit run app.py --server.headless true

```

---

##🔒 Security & Ethics* **No real scraping without permission** - Demo uses mock data
* **API keys stored in `.env**` - Never committed to version control
* **Rate limiting implemented** - Prevents API abuse
* **GDPR-compliant data handling** - Email verification only with consent

---

##📝 LicenseMIT License - See `LICENSE` file for details

---

##🤝 Contributing1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

