from fastapi import FastAPI
from bicity.api.bike import router as bike_router

def create_app() -> FastAPI:
    
    app = FastAPI(title="Bicity API",
                  description="API for managing bicycle stations and their dock availability.")

    app.include_router(bike_router)

    return app

app = create_app()