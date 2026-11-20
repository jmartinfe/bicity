from fastapi import FastAPI
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from bicity.core.exceptions import AppError
from bicity.core.logging import init_logging, get_logger
from bicity.core.middleware import RateLimiter
from bicity.api.bike import router as bike_router


load_dotenv()  # Load environment variables from .env file
init_logging()
logger = get_logger(__name__) # Initialize the logger
rate_limiter = RateLimiter(max_requests=30, time_window=60) # Initialize the rate limiter

IS_PRODUCTION = os.getenv("ENVIRONMENT", "production").lower() == "production"
APP_TITLE = os.getenv("APP_TITLE", "Bicity API")

app = FastAPI(
    title=APP_TITLE,
    description="API for managing bicycle stations and their dock availability.",
    version="0.1.0",
    docs_url="/docs" if not IS_PRODUCTION else None,
    redoc_url="/redoc" if not IS_PRODUCTION else None
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        logger.warning("Rate limit exceeded for client IP: %s", client_ip)
        raise HTTPException(status_code=429, detail="Too many requests")
    return await call_next(request)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error("AppError handled: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Set up CORS middleware
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow specified origins from environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_referer(request: Request, call_next):
    referer = request.headers.get("referer")
    allowed_domains = origins  # Use the same allowed origins for referer check
    
    if referer:
        if not any(domain in referer for domain in allowed_domains):
            raise HTTPException(status_code=403, detail="Forbidden: Invalid referer")
    
    return await call_next(request)

app.include_router(bike_router)