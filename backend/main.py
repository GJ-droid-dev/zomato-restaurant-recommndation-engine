import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers import recommend
from backend.services.data_loader import load_and_clean_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Zomato AI Recommendations API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application... Preloading dataset...")
    load_and_clean_data()
    logger.info("Application initialized successfully.")

# Include routers
app.include_router(recommend.router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Service is running."}

# Mount frontend for serving static UI files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
