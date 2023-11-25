import sys
from pathlib import Path
from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.main import app  # noqa: E402
from model.config.core import config  # noqa: E402
from model.preprocessing.data_manager import load_dataset  # noqa: E402


@pytest.fixture(scope="module")
def test_data() -> pd.DataFrame:
    return pd.DataFrame(
        load_dataset(
            client_file_name=config.app_config.client_data_file,
            price_file_name=config.app_config.price_data_file,
        ).iloc[0]
    ).T


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
