import streamlit as st
import requests

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

# Sidebar for continent and function selection
st.sidebar.header("Options")
continent = st.sidebar.selectbox("Select Continent:", ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania'])
function = st.sidebar.selectbox("Choose statistic to display:", [
    "Total Countries", 
    "Total Population", 
    "Average Population", 
    "Total Area", 
    "Max Population", 
    "Min Population", 
    "Population Density"
])

# Fetch the data when a continent is selected
continent_data = get_continent_stats(continent)

if continent_data:
    # Display the statistics based on selected function
    st.subheader(f"{function} in {continent}")
    if function == "Total Countries":
        st.write(f"Total Countries: {continent_data['Total_Countries']}")
    elif function == "Total Population":
        st.write(f"Total Population: {continent_data['Total_Population']}")
    elif function == "Average Population":
        st.write(f"Average Population: {continent_data['Average_Population']}")
    elif function == "Total Area":
        st.write(f"Total Area (km²): {continent_data['Total_Area']}")
    elif function == "Max Population":
        st.write(f"Maximum Population: {continent_data['max_population']}")
    elif function == "Min Population":
        st.write(f"Minimum Population: {continent_data['min_population']}")
    elif function == "Population Density":
        st.write(f"Population Density (per km²): {continent_data['Population_Density']}")
