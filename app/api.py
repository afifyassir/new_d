import json
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
    """
    Root Get
    """
    health = Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(input_data: MultipleDataInputs) -> Any:
    """
    Predicting customer churn
    """

    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = await make_prediction(input_data=input_df.replace({np.nan: None}))

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results
