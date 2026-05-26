import os
import logging

logger = logging.getLogger(__name__)

# Construct model path - works whether script is run from project root or app directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.getcwd()

# Try multiple paths to find the model
possible_paths = [
    os.path.join(project_root, "app", "model", "final_model.joblib"),
    os.path.join(current_dir, "app", "model", "final_model.joblib"),
    os.path.join(current_dir, "model", "final_model.joblib"),
]

model_path = None
for path in possible_paths:
    if os.path.exists(path):
        model_path = path
        logger.info(f"Model found at: {model_path}")
        break

if model_path is None:
    logger.warning(f"Model not found in expected locations. Using default path.")
    model_path = os.path.join(project_root, "app", "model", "final_model.joblib")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_RELOAD = os.getenv("API_RELOAD", "False").lower() == "true"