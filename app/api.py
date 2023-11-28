import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import __version__  # noqa: E402
from app.config import settings  # noqa: E402
from app.schemas.health import Health  # noqa: E402
from app.schemas.predict import MultipleDataInputs, PredictionResults  # noqa: E402
from model import __version__ as model_version  # noqa: E402
from model.predict import make_prediction  # noqa: E402

#  Create an instance of APIRouter. This will be used to define the API endpoints.
api_router = APIRouter()

# In FastAPI, the response_model parameter in the @api_router.get or @api_router.post decorator is used
#  to define the model for the data that the endpoint returns. This model is used for:
# - Output Data Conversion: The returned data will be converted into the defined model's structure.
#   If the data doesn't fit the model, an error will occur.
# - Data Validation: The returned data will be validated against the model. If the data is invalid, an error will occur.
# - Automatic API Documentation: The model will be used to generate interactive API documentation.

# The status_code parameter in FastAPI route decorators like @api_router.get or @api_router.post
# is used to specify the HTTP status code that should be returned when the request is successful.


@api_router.get("/health", response_model=Health, status_code=200)
def health() -> dict:

    """
    The API router decorator and this function will help us define a GET endpoint at /health, when accessed,
    it returns a Health object containing the project name, API version, and model version.
    This endpoint is typically used for monitoring and checking the status of the API.
    """

    health_info = Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    ).dict()

    return health_info


@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(input_data: MultipleDataInputs) -> Any:
    """
    It defines a POST endpoint at /predict. It takes an instance of MultipleDataInputs as input.
    Inside the endpoint, the input data is converted to a DataFrame and passed to
    the make_prediction function. If there are any errors in the prediction, an HTTP exception
    is raised. Otherwise, the prediction results are returned.
    """

    try:
        # Convert input data to DataFrame and replace NaN values with None
        input_df = pd.DataFrame(jsonable_encoder(input_data.inputs)).replace(
            {np.nan: None}
        )

        # Log the input data
        logger.info(f"Received input data: {input_data.inputs}")

        # Make predictions using the trained model
        predictions = await make_prediction(input_data=input_df)

        # Log and return the prediction results
        logger.info(f"Prediction results: {predictions.get('predictions')}")
        return predictions

    except Exception as e:  # Handle any exceptions during prediction
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
