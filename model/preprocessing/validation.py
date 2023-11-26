import json
import sys
from pathlib import Path
from typing import Optional, Tuple

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pydantic import ValidationError  # noqa: E402

from model.config.core import config  # noqa: E402
from model.preprocessing.validation_classes import MultipleDataInputs  # noqa: E402


def check_inputs(*, data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """
    Validate model inputs.
    This function checks the inputs to the model for any unprocessable values,
    ensuring that the input data is clean and ready for processing.
    """

    # Copy the data for validation
    validated_data = data[config.model_config.features].copy()
    errors = None

    try:
        # Replace numpy NaNs so that Pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        # If validation fails, capture the error
        errors = json.loads(error.json())

    return validated_data, errors
