from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging
from contextlib import asynccontextmanager
from src.detector import ShopStatusDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Detector
detector = ShopStatusDetector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    logger.info("Starting up: Loading model...")
    detector.load_model()
    yield
    logger.info("Shutting down binary...")

app = FastAPI(
    title="Shop Status Detector API",
    description="VLM-powered API to detect if a shop is open or closed.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/detect-status")
async def detect_status(file: UploadFile = File(...)):
    """Upload an image to detect shop status."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        result = detector.classify(image)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """Service health check."""
    return {
        "status": "healthy",
        "device": detector.device,
        "model_loaded": detector.model is not None
    }
