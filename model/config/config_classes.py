from typing import Sequence

from pydantic import BaseModel


# The AppConfig and ModelConfig classes are used to define the structure of the configuration for the application and
# model respectively. They are subclasses of BaseModel from the pydantic library, which is a data validation library
# in Python.
# AppConfig and ModelConfig use type annotations to define what fields the configuration should have and what type those
# fields should be. This allows pydantic to automatically validate that the configuration matches the expected structure
# and convert the fields to the appropriate types.

# This class is used to define and validate the configuration related to the application. It includes fields like
# package_name, pipeline_save_file, client_data_file, and price_data_file.
class AppConfig(BaseModel):
    package_name: str
    pipeline_save_file: str
    client_data_file: str
    price_data_file: str


# This class is used to define and validate the configuration related to the model. It includes fields like target,
# features, random_state, numerical_vars, categorical_vars, and test_size.
class ModelConfig(BaseModel):

    target: str
    features: Sequence[str]
    random_state: int
    numerical_vars: Sequence[str]
    categorical_vars: Sequence[str]
    test_size: float


# The Config class is a wrapper for these two configuration classes. It has two fields, app_config and model_config,
# which are instances of AppConfig and ModelConfig respectively. This allows us to keep all of our configuration
# in one place.
class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig
