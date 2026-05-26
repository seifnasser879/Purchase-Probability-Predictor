import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.prediction_schema import PurchaseData
from app.services.predict_service import predict


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Purchase Probability Predictor API",
    version="2.0.0",
    description="ML API to predict the probability of a customer making a purchase",

)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "message": "Purchase Probability Predictor API",
        "status": "healthy",
        "version": "2.0.0"
    }

@app.post("/predict", tags=["Prediction"], response_model=dict)
def predict_purchase(request: PurchaseData):
    """
    Predict the probability of a customer making a purchase.
    
    Returns a probability score between 0 and 1, where:
    - 0 = very unlikely to purchase
    - 1 = very likely to purchase
    """
    try:
        logger.info(f"Prediction request received: {request.model_dump()}")
        prediction = predict(request.model_dump())
        
        response = {
            "predicted_probability": round(prediction, 4),
            "predicted_percentage": round(prediction * 100, 2),
            "purchase_likely": prediction > 0.5,
            "confidence": "high" if prediction > 0.7 or prediction < 0.3 else "medium"
        }
        logger.info(f"Prediction response: {response}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prediction error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during prediction"
        )

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }