import logging
from fastapi import FastAPI
from app.routers import scan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ra'can Waste Disposal Assistant API",
    description="API for determining proper waste disposal based on product barcodes.",
    version="1.0.0"
)

app.include_router(scan.router)

logger.info("Application has started.")

@app.get("/")
async def read_root():
    logger.info("Root endpoint was called.")
    return {"message": "Welcome to Ra'Can : the Waste Disposal Assistant API"}
