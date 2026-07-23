from fastapi import FastAPI

from api.routes import companies
from api.routes import clusters
from api.routes import cluster_summary


app = FastAPI(
    title="N100 Financial Platform API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "N100 Financial Platform API running"
    }


app.include_router(
    companies.router
)

app.include_router(
    clusters.router
)

app.include_router(
    cluster_summary.router
)