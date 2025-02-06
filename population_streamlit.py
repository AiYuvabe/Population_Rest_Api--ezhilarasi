import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL (assuming it's running on localhost)
API_URL = "http://127.0.0.1:8000/"

# Define function to get continent stats from FastAPI backend
def get_continent_stats(continent):
    response = requests.get(f"{API_URL}{continent}/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data")
        return None

# Streamlit user interface
st.title("World Population and Statistics by Continent")

# Dropdown to select continent
continent = st.selectbox("Select Continent:", ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania'])

# Show data when a continent is selected
if continent:
    st.write(f"Fetching data for {continent}...")
    
    # Fetch the data from FastAPI
    continent_data = get_continent_stats(continent)

    if continent_data:
        # Display the statistics for the selected continent
        st.subheader(f"Statistics for {continent}")
        st.write(f"Total Countries: {continent_data['Total_Countries']}")
        st.write(f"Total Population: {continent_data['Total_Population']}")
        st.write(f"Average Population: {continent_data['Average_Population']}")
        st.write(f"Total Area (km²): {continent_data['Total_Area']}")
        st.write(f"Max Population: {continent_data['max_population']}")
        st.write(f"Min Population: {continent_data['min_population']}")
        st.write(f"Population Density (per km²): {continent_data['Population_Density']}")
