import pandas as pd
from fastapi import FastAPI

app=FastAPI()

file_path="C:/Users/User/Desktop/Python/world_population.csv"
read_file=pd.read_csv(file_path)

@app.get("/{continent}/{stat}")
def get_max_and_min_country(continent:str,stat:str):
    read_data=read_file[read_file["Continent"]==continent]
    if stat=="max":
        index=read_data["Population"].idxmax()
    if stat=="min":
        index=read_data["Population"].idxmin()
    # else:
    #     return f"{stat}"

    country=read_data["Country"][index]
    population=read_data["Population"][index]
    area=read_data["Area"][index]
    continents=read_data["Continent"][index]
    return f"The continent is {continents},The Country is {country},The population is {population},The Area is {area}"

@app.get("/{continent}/average/close")           
def get_average_population(continent:str):
    group_of_data=read_file.groupby("Continent")["Population"].mean().round(1)
    return f"The average population is : {group_of_data[continent]}"
    


















    
