##📄 Lead Generation Web Agent for Akash EU PrimeA sophisticated web agent for identifying, enriching, and ranking high-probability leads for 3D in-vitro models in toxicology and preclinical safety research.

---

##🎯 Features <h1>Lead Identification</h1> : Scan multiple sources for target roles (Director of Toxicology, Head of Preclinical Safety, etc.)
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

```

---





