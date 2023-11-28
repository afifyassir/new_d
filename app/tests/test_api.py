from typing import Any, Union

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, test_data: pd.DataFrame) -> None:

    """ This is a test function for making predictions using a FastAPI application.
        This function is used to ensure that the prediction endpoint of the API is working as expected.
        It takes two arguments: client, which is an instance of TestClient, and test_data, which is
        a DataFrame containing the data to be used for testing."""

    def convert_timestamps(obj: Any) -> Union[str, Any]:

        """ This function takes an object obj as input and checks if it's
           an instance of pd.Timestamp. If it is, it converts the timestamp to an
           ISO format string. Otherwise, it returns the object as is.
           This function is used to convert any timestamps in the test
           data to a format that can be serialized to JSON."""

        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        else:
            return obj

    test_data = test_data.applymap(convert_timestamps)

    # The np.nan values in test_data are replaced with None to ensure compatibility with Pydantic,
    # and the DataFrame is converted to a list of dictionaries (records) to form the payload for the POST request.
    payload = {"inputs": test_data.replace({np.nan: None}).to_dict(orient="records")}

    # Make a POST request to the /api/v1/predict endpoint of the FastAPI application running on
    # localhost:8001 using the client.post method. Pass the payload as JSON in the request body.
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # The status code of the response is checked to ensure it's 200, indicating a successful request.
    assert response.status_code == 200
    # The response data is parsed from JSON.
    prediction_data = response.json()
    # Check that the predictions field is either 0 or 1.
    assert prediction_data["predictions"] in [0, 1]
    # Check that the errors field is None.
    assert prediction_data["errors"] is None
