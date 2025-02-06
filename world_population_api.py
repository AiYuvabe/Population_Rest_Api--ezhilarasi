import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()
df = pd.read_csv("world_population.csv")

# Aggregate the data
continent_stats = df.groupby("Continent").agg(
    Total_Countries=('Country', 'count'),
    Total_Population=('Population', 'sum'),
    Average_Population=('Population', 'mean'),
    Total_Area=('Area', 'sum'),
    max_population=('Population', 'max'),
    min_population=('Population', 'min'),
   
).reset_index()

# Compute Population Density
continent_stats["Population_Density"] = (
    continent_stats["Total_Population"] / continent_stats["Total_Area"]
)


@app.get("/")
def home():
    return {"message": "Welcome to the home page"}


@app.get("/{continent}/")
def get_continent_stats(continent: str):
    # Filter the dataframe for the given continent
    result = continent_stats[continent_stats["Continent"] == continent].squeeze()
    
    #  Convert row to a dictionary
    result = result.to_dict()

    return result  

