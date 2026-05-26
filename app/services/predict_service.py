import logging
from config import model_path
import joblib
import pandas as pd 
from app.schemas.prediction_schema import PurchaseData

logger = logging.getLogger(__name__)

# Cache model in memory to avoid repeated loading
_cached_model = None

def get_model():
    """Load model once and cache it in memory for performance."""
    global _cached_model
    if _cached_model is None:
        try:
            _cached_model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
        except FileNotFoundError:
            logger.error(f"Model file not found at {model_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    return _cached_model

def predict(data: dict) -> float:
    """
    Predict purchase probability for given customer and item data.
    
    Args:
        data: Dictionary with prediction features
        
    Returns:
        float: Purchase probability between 0 and 1
        
    Raises:
        ValueError: If prediction fails
    """
    try:
        model = get_model()
        input_df = pd.DataFrame([data])
        prob = model.predict_proba(input_df)[:, 1][0]
        logger.info(f"Prediction successful: probability={prob:.4f}")
        return float(prob)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise ValueError(f"Prediction failed: {str(e)}")