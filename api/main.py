from fastapi import FastAPI

from api.routes import companies
from api.routes import clusters
from api.routes import cluster_summary
from api.routes import cluster_profile
from api.routes import cluster_companies
from api.routes import screener
from api.routes import financial_metrics


app = FastAPI(
    title="N100 Financial Platform API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "N100 Financial Platform API running"
    }


# Company APIs
app.include_router(
    companies.router
)


# Cluster APIs
app.include_router(
    clusters.router
)


app.include_router(
    cluster_summary.router
)


app.include_router(
    cluster_profile.router
)


app.include_router(
    cluster_companies.router
)

app.include_router(
    screener.router
)

app.include_router(
    financial_metrics.router
)