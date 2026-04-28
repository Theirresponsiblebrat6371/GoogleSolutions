from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database import Base, engine
from routers import dashboard_routes, reports, tasks, volunteers


settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Resource Allocation",
    description="NGO volunteer coordination and urgent need prioritization platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router)
app.include_router(volunteers.router)
app.include_router(tasks.router)
app.include_router(dashboard_routes.router)


@app.get("/")
def root():
    return {
        "message": "Smart Resource Allocation API is running",
        "city": settings.default_city,
        "docs": "/docs",
    }
