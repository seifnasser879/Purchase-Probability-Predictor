# Purchase Probability Predictor API

A FastAPI-based machine learning service that predicts the probability of a customer making a purchase based on user behavior and item characteristics.

## Features

✨ **Core Features**
- 🎯 ML-powered purchase probability prediction
- ⚡ Fast inference with model caching
- 📊 Detailed prediction confidence metrics
- 🛡️ Input validation with meaningful error messages
- 📝 Automatic OpenAPI/Swagger documentation
- 🔄 CORS support for cross-origin requests
- 📋 Structured logging for debugging
- 🐳 Docker containerization support

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Local Installation

1. **Clone and navigate to the project**
   ```bash
   cd Purchase\ Probability\ Predictor
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t purchase-predictor:latest .
   ```

2. **Run with Docker**
   ```bash
   docker run -p 8000:8000 purchase-predictor:latest
   ```

3. **Using Docker Compose**
   ```bash
   docker-compose up
   ```

## API Documentation

### Interactive Documentation

Once the API is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Health Check
```http
GET /
```
Quick health check endpoint.

**Response:**
```json
{
  "message": "Purchase Probability Predictor API",
  "status": "healthy",
  "version": "2.0.0"
}
```

#### 2. Predict Purchase Probability
```http
POST /predict
```

**Request Body:**
```json
{
  "user_total_spent": 500.0,
  "user_transaction_count": 5,
  "user_unique_items": 10,
  "item_popularity": 150,
  "item_avg_quantity": 2.5,
  "item_unit_price": 15.0
}
```

**Field Descriptions:**
- `user_total_spent` (float): Total amount spent by the user (≥ 0)
- `user_transaction_count` (int): Number of transactions by the user (≥ 0)
- `user_unique_items` (int): Number of unique items purchased (≥ 0)
- `item_popularity` (int): Popularity score of the item (≥ 0)
- `item_avg_quantity` (float): Average quantity per transaction (≥ 0)
- `item_unit_price` (float): Unit price of the item (≥ 0)

**Response:**
```json
{
  "predicted_probability": 0.8234,
  "predicted_percentage": 82.34,
  "purchase_likely": true,
  "confidence": "high"
}
```

**Response Field Descriptions:**
- `predicted_probability`: Probability score between 0 and 1
- `predicted_percentage`: Probability as a percentage
- `purchase_likely`: Boolean indicating if probability > 50%
- `confidence`: "high" (>70% or <30%), "medium" (otherwise)

#### 3. Detailed Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

### Example Requests

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "user_total_spent": 500.0,
    "user_transaction_count": 5,
    "user_unique_items": 10,
    "item_popularity": 150,
    "item_avg_quantity": 2.5,
    "item_unit_price": 15.0
  }'
```

**Using Python requests:**
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "user_total_spent": 500.0,
    "user_transaction_count": 5,
    "user_unique_items": 10,
    "item_popularity": 150,
    "item_avg_quantity": 2.5,
    "item_unit_price": 15.0
}

response = requests.post(url, json=data)
print(response.json())
```

## Project Structure

```
Purchase Probability Predictor/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md             # This file
├── app/
│   ├── __init__.py
│   ├── model/
│   │   └── final_model.joblib  # Trained ML model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prediction_schema.py  # Pydantic models for validation
│   └── services/
│       ├── __init__.py
│       └── predict_service.py    # Prediction logic
└── notebook/
    └── training.ipynb      # Model training notebook
```

## Architecture

### Model Caching
The application loads the ML model once and caches it in memory for optimal performance. Subsequent requests reuse the cached model instead of loading from disk.

### Validation
All input data is validated using Pydantic models before prediction:
- Type validation
- Range validation (non-negative values)
- Required field validation

### Error Handling
- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: Server-side prediction errors

### Logging
The application uses Python's built-in logging module with:
- Timestamp, logger name, level, and message format
- INFO level for successful operations
- ERROR level for failures with stack traces

## Environment Variables

Configure the API using environment variables:

```bash
# Server configuration
API_HOST=0.0.0.0        # Default: 0.0.0.0
API_PORT=8000           # Default: 8000
API_RELOAD=False        # Default: False (set to True for development)
```

## Performance Considerations

- **Model Caching**: ML model is cached in memory after first load
- **Efficient Pandas Operations**: Single DataFrame creation per request
- **Connection Pooling**: CORS middleware reduces overhead
- **Async-ready**: Built on FastAPI's async foundation

## Development

### Running Tests (if added)
```bash
pytest
```

### Code Style (if using formatters)
```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy .
```

## Troubleshooting

### Model Not Found
If you get "Model file not found" error:
1. Ensure `app/model/final_model.joblib` exists
2. Check that the file path is correct
3. Verify file permissions

### Port Already in Use
If port 8000 is already in use:
```bash
# Use a different port
uvicorn main:app --port 8001

# Or with Docker
docker run -p 8001:8000 purchase-predictor:latest
```

### CORS Errors
If you're getting CORS errors when calling from another origin, the API is configured to accept all origins by default (development-friendly). For production, restrict allowed origins in `main.py`.

## Deployment

### Production Deployment with Gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Cloud Deployment
The Docker image can be deployed to:
- AWS ECS/ECR
- Google Cloud Run
- Azure Container Instances
- Heroku
- Any Kubernetes cluster

## Contributing

1. Create a new branch for your feature
2. Make changes and test thoroughly
3. Ensure code follows existing style
4. Submit a pull request

## License

MIT License - feel free to use this project as you wish.


