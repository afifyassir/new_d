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

api_router = APIRouter()


@api_router.get("/health", response_model=Health, status_code=200)
def health() -> dict:

    health_info = Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    ).dict()

    return health_info


@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(input_data: MultipleDataInputs) -> Any:
    """
    Predicting customer churn
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
