import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

# =====================================================================
# PAGE CONFIGURATION & STYLING
# =====================================================================
st.set_page_config(
    page_title="Google Play Apps Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📱 Google Play Store Ecosystem Dashboard")
st.markdown("Explore application distribution, pricing structures, and ratings across market sectors.")

# =====================================================================
# DATA LOADING & CLEANING (Self-Contained)
# =====================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/googleplaystore.csv")
    df = df.drop_duplicates()

    # Remove corrupt row if present
    if '1.9' in df['Category'].values:
        df = df[df['Category'] != '1.9']

    # Clean numeric features
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    def clean_size(val):
        if pd.isna(val) or val == 'Varies with device':
            return np.nan
        val = str(val).upper().strip()
        if 'M' in val:
            return float(val.replace('M', '')) * 1024
        if 'K' in val:
            return float(val.replace('K', ''))
        return np.nan

    df['Size_KB'] = df['Size'].apply(clean_size)
    df['Installs_Clean'] = df['Installs'].astype(str).str.replace('+', '', regex=False).str.replace(',', '', regex=False)
    df['Installs_Clean'] = pd.to_numeric(df['Installs_Clean'], errors='coerce')
    df['Price_Clean'] = df['Price'].astype(str).str.replace('$', '', regex=False)
    df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')

    # Drop nulls in essential columns
    df = df.dropna(subset=['Rating', 'Type', 'Category'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# =====================================================================
# INTERACTIVE SIDEBAR WIDGETS (Requirement 1)
# =====================================================================
st.sidebar.header("🔍 Filter Options")

# Widget 1: Category Dropdown
all_categories = ["All"] + sorted(list(df['Category'].unique()))
selected_category = st.sidebar.selectbox("Select App Category", all_categories)

# Widget 2: Rating Threshold Slider
min_rating = st.sidebar.slider(
    "Minimum Rating Score",
    min_value=float(df['Rating'].min()),
    max_value=float(df['Rating'].max()),
    value=4.0,
    step=0.1
)

# Widget 3: App Type Multiselect
available_types = list(df['Type'].unique())
selected_types = st.sidebar.multiselect("Select App Type", available_types, default=available_types)

# Apply Reactive Filtering
filtered_df = df[
    (df['Rating'] >= min_rating) &
    (df['Type'].isin(selected_types))
]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Apps", f"{len(filtered_df):,}")
col2.metric("Avg Rating", f"{filtered_df['Rating'].mean():.2f}" if not filtered_df.empty else "N/A")
col3.metric("Avg Price ($)", f"${filtered_df['Price_Clean'].mean():.2f}" if not filtered_df.empty else "N/A")
col4.metric("Total Reviews", f"{filtered_df['Reviews'].sum():,.0f}" if not filtered_df.empty else "N/A")

st.divider()

# =====================================================================
# VISUALIZATIONS (3 Responsive Charts - Requirement 1)
# =====================================================================
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Top 10 Most Reviewed Applications")
    if not filtered_df.empty:
        top_reviewed = filtered_df.nlargest(10, 'Reviews')
        fig_bar = px.bar(
            top_reviewed,
            x='Reviews',
            y='App',
            orientation='h',
            color='Rating',
            color_continuous_scale='Viridis',
            title="Most Reviewed Apps in Filtered Selection"
        )
        fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data available for selected filters.")

with chart_col2:
    st.subheader("📈 Rating Distribution Density")
    if not filtered_df.empty:
        fig_hist = px.histogram(
            filtered_df,
            x='Rating',
            nbins=20,
            color='Type',
            barmode='overlay',
            title="Rating Frequency Spread by App Type"
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No data available for selected filters.")

st.subheader("🌌 App Footprint (Size) vs User Rating")
if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x='Size_KB',
        y='Rating',
        size='Installs_Clean',
        color='Type',
        hover_name='App',
        log_x=True,
        title="App Size (KB, Log Scale) vs Rating (Bubble Size = Installs)"
    )
    fig_scatter.update_layout(height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("No data available for selected filters.")

st.divider()

# =====================================================================
# LIVE REACTIVE DATA TABLE (Requirement 1)
# =====================================================================
st.subheader("📋 Reactive Data Table")
st.write(f"Displaying **{len(filtered_df)}** entries matching active filters.")

display_cols = ['App', 'Category', 'Rating', 'Reviews', 'Size_KB', 'Installs', 'Type', 'Price']
st.dataframe(filtered_df[display_cols].reset_index(drop=True), use_container_width=True)

st.divider()

# =====================================================================
# LIVE EXTERNAL REST API INTEGRATION (Requirement 2)
# =====================================================================
st.subheader("🌐 Live External API Feed: Tech Hub Climate Data")
st.markdown("Fetching real-time environmental data for Silicon Valley (San Francisco) via Open-Meteo REST API.")

@st.cache_data(ttl=600)  # Cache API call for 10 minutes
def fetch_live_weather():
    # Keyless, free Open-Meteo API for San Francisco (Lat: 37.7749, Lon: -122.4194)
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

weather_data = fetch_live_weather()

if "error" not in weather_data and "current_weather" in weather_data:
    current_weather = weather_data["current_weather"]

    # Extract fields from JSON payload
    temperature = current_weather.get("temperature")
    windspeed = current_weather.get("windspeed")
    weathercode = current_weather.get("weathercode")
    time_stamp = current_weather.get("time")

    api_col1, api_col2, api_col3, api_col4 = st.columns(4)
    api_col1.metric("Location", "San Francisco, CA")
    api_col2.metric("Temperature (°C)", f"{temperature} °C")
    api_col3.metric("Wind Speed (km/h)", f"{windspeed} km/h")
    api_col4.metric("Last Updated", time_stamp)

    st.caption("Weather data provided by [Open-Meteo.com](https://open-meteo.com/) (CC BY 4.0 Attribution).")
else:
    st.warning("Could not fetch live external API data at this time.")
    if "error" in weather_data:
        st.caption(f"Error details: {weather_data['error']}")
