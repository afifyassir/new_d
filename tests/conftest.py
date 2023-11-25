import logging
import sys
from pathlib import Path

import pytest
from sklearn.model_selection import train_test_split

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.config.core import config  # noqa: E402
from model.preprocessing.data_manager import load_dataset  # noqa: E402

logger = logging.getLogger(__name__)


@pytest.fixture
def sample_input_data():
    data = load_dataset(
        client_file_name=config.app_config.client_data_file,
        price_file_name=config.app_config.price_data_file,
    )

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    return (X_test, y_test)
