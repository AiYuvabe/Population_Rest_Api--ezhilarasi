# import pandas as pd
# from fastapi import APIRouter, HTTPException

# router = APIRouter()

# # Load dataset
# df = pd.read_csv("data/world_population.csv")

# # Aggregate statistics by continent
# continent_stats = df.groupby("Continent").agg(
#     Total_Countries=('Country', 'count'),
#     Total_Population=('Population', 'sum'),
#     Average_Population=('Population', 'mean'),
#     Total_Area=('Area', 'sum'),
#     max_population=('Population', 'max'),
#     min_population=('Population', 'min'),
# ).reset_index()

# # Compute Population Density
# continent_stats["Population_Density"] = (
#     continent_stats["Total_Population"] / continent_stats["Total_Area"]
# )

# @router.get("/{continent}/")
# def get_continent_stats(continent: str):
#     result = continent_stats[continent_stats["Continent"] == continent].squeeze()

#     if result.empty:
#         raise HTTPException(status_code=404, detail="Continent not found")

#     return result.to_dict()

import logging
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, field_validator
import pandas as pd

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load Data
data_path = "data/world_population.csv"
try:
    df = pd.read_csv(data_path)
    logger.info("Dataset loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load dataset: {e}")
    raise

# Compute statistics per continent
continent_stats = df.groupby("Continent").agg(
    Total_Countries=("Country", "count"),
    Total_Population=("Population", "sum"),
    Average_Population=("Population", "mean"),
    Total_Area=("Area", "sum"),
    Max_Population=("Population", "max"),
    Min_Population=("Population", "min"),
).reset_index()
continent_stats["Population_Density"] = (
    continent_stats["Total_Population"] / continent_stats["Total_Area"]
)

# Pydantic Model for Response Validation
class ContinentStats(BaseModel):
    continent: str = Field(..., title="Continent Name")
    total_countries: int
    total_population: int
    average_population: float
    total_area: int
    max_population: int
    min_population: int
    population_density: float

    @field_validator("total_countries", "total_population", "total_area", "max_population", "min_population")
    def must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Value must be non-negative")
        return value

# FastAPI App Setup
app = FastAPI()
router = APIRouter()

@router.get("/continent/{continent}", response_model=ContinentStats)
def get_continent_stats(continent: str):
    logger.info(f"Fetching stats for continent: {continent}")
    result = continent_stats[continent_stats["Continent"] == continent]
    
    if result.empty:
        logger.warning("Continent not found")
        raise HTTPException(status_code=404, detail="Continent not found")
    
    return ContinentStats(
        continent=continent,
        total_countries=int(result["Total_Countries"].values[0]),
        total_population=int(result["Total_Population"].values[0]),
        average_population=float(result["Average_Population"].values[0]),
        total_area=int(result["Total_Area"].values[0]),
        max_population=int(result["Max_Population"].values[0]),
        min_population=int(result["Min_Population"].values[0]),
        population_density=float(result["Population_Density"].values[0])
    )


