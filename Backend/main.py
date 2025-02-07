from fastapi import FastAPI
from routers import population  # Import router

app = FastAPI()

# Include routers
# app.include_router(population.router)

# @app.get("/")
# def home():
#     return {"message": "Welcome to the World Population API"}

@app.get("/")
def home():
    return {"message": "Welcome to the World Population API"}

app.include_router(population.router)