# google-play-dashboard
A live, deployed interactive dashboard built with Streamlit and Plotly that empowers stakeholders to explore Google Play Store application metrics and features live REST API integration.
Project Repository Structure
google-play-dashboard/
├── .streamlit/
│   └── Run app.py              # Streamlit visual theme configuration
├── data/
│   └── googleplaystore.csv     # Self-contained dataset
├── app.py                      # Main Streamlit dashboard code
├── requirements.txt            # Streamlit & deployment dependencies
└── README.md                   # Live URL, API explanation & setup guide


## 🔗 Live Public Dashboard URL

🚀 **Access the deployed dashboard here:**  
`https://app-play-dashboard.streamlit.app/`  


---

## 1. Dashboard Overview & Features

This interactive dashboard allows non-technical users to slice, filter, and visualize app store trends dynamically without writing SQL or Python.

### Interactive Components
* **Input Widgets:**
  1. `Category Selectbox`: Filter dashboard content by market category.
  2. `Rating Score Slider`: Dynamically filter apps based on a minimum rating boundary.
  3. `App Type Multiselect`: Toggle between `Free` and `Paid` application tiers.
* **Responsive Visualizations (Plotly):**
  1. **Horizontal Bar Chart:** Displays the top 10 most reviewed apps in the filtered selection.
  2. **Overlay Histogram:** Shows the distribution of user ratings broken down by free vs. paid tiers.
  3. **Bubble Scatter Plot:** Explores the relationship between app size (in KB) and rating, with bubble area scaled by installation counts.
* **Live Reactive Data Table:** Displays filtered rows and key columns in real-time.

---

## 2. External REST API Integration Details

* **Target Endpoint URL:**  
  `https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&current_weather=true`
* **HTTP Request Method:** `GET`
* **API Description:**  
  The dashboard issues an asynchronous `GET` request using Python's `requests` library to fetch current atmospheric and climate conditions for the primary tech hub sector (San Francisco / Silicon Valley).
* **Extracted JSON Response Fields Displayed:**
  * `temperature`: Current temperature reading in degrees Celsius (°C).
  * `windspeed`: Current wind speed in km/h.
  * `time`: Timestamp of the latest sensor update.



---

## 3. Local Setup & Execution Guide

Replicate the environment and run the app locally:

```bash
# 1. Clone the repository
git clone <your-public-github-link>
cd google-play-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit server
streamlit run app.py
