# 📊 Google Play Store Dashboard

A live, interactive dashboard built with **Streamlit** and **Plotly** that lets stakeholders explore Google Play Store app metrics — no SQL or Python required.

🔗 **Live Demo:** [app-play-dashboard.streamlit.app](https://app-play-dashboard.streamlit.app/)

---

## 📁 Project Structure

```
google-play-dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit visual theme configuration
├── data/
│   └── googleplaystore.csv  
├── app.py                   # Main Streamlit dashboard code
├── requirements.txt         # Dependencies
└── README.md                 # Project documentation
```

---

## ✨ Features

### Interactive Filters
| Widget | Function |
|---|---|
| **Category Selectbox** | Filter apps by market category |
| **Rating Slider** | Set a minimum rating threshold |
| **App Type Multiselect** | Toggle between Free and Paid apps |

### Visualizations (Plotly)
- **Top 10 Most Reviewed Apps** — horizontal bar chart
- **Rating Distribution** — overlay histogram, Free vs. Paid
- **Size vs. Rating** — bubble scatter plot, sized by install count

### Live Data Table
Reactively updates to show filtered rows and key columns in real time.

---

## 🌐 Live API Integration

The dashboard also demonstrates external API connectivity by fetching real-time weather data:

- **Endpoint:** `https://api.open-meteo.com/v1/forecast`
- **Method:** `GET`
- **Fields displayed:** temperature (°C), wind speed (km/h), timestamp

> *Included to showcase live REST API integration as part of the capstone requirements, independent of the core Play Store dataset.*

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/pramodj551-oss/google-play-dashboard.git
cd google-play-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

---

## 🛠️ Tech Stack

`Python` · `Streamlit` · `Plotly` · `Pandas` · `Requests`

---

## 📬 Contact

**Pramod Prakash Jadhav**
📧 pramodj551@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/pramod-prakash-jadhav-42ba2281)
