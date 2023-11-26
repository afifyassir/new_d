from pydantic import BaseModel
from typing import Optional, Sequence


# Configuration related to the application
class AppConfig(BaseModel):
    package_name: str
    pipeline_save_file: str
    client_data_file: str
    price_data_file: str


# Configuration related to the model
class ModelConfig(BaseModel):

    target: str
    features: Sequence[str]
    random_state: int
    numerical_vars: Sequence[str]
    categorical_vars: Sequence[str]
    test_size: float


# Wrapper for the two uration classes
class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig
