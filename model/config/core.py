import os
import sys
from pathlib import Path
from typing import Optional

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from strictyaml import YAML, load  # noqa: E402

import model  # noqa: E402
from model.config.config_classes import AppConfig, Config, ModelConfig  # noqa: E402

PACKAGE_ROOT = os.path.dirname(os.path.abspath(model.__file__))
ROOT = os.path.dirname(PACKAGE_ROOT)
CONFIG_FILE_PATH = os.path.join(PACKAGE_ROOT, "config.yml")
DATASET_DIR = os.path.join(PACKAGE_ROOT, "datasets")
TRAINED_MODEL_DIR = os.path.join(PACKAGE_ROOT, "trained_models")


def yaml_config_file_location() -> str:
    """Find the location of the configuration file.
    Return the location if found, otherwise raise an exception."""

    try:
        assert os.path.isfile(CONFIG_FILE_PATH)
        return CONFIG_FILE_PATH
    except AssertionError:
        raise Exception(f"The config file does not exist at {CONFIG_FILE_PATH!r}")


def fetching_yaml_file(file_path: Optional[str] = None) -> YAML:
    """Parse YAML containing the package configuration."""

    try:
        if not file_path:
            file_path = yaml_config_file_location()

        with open(file_path, "r") as yml_file:
            parsed_config = load(yml_file.read())
            return parsed_config
    except FileNotFoundError:
        raise OSError("YAML file not found")


def validate_config(parsed_config: YAML = None) -> Config:
    """Validate values of our configuration."""
    parsed_config = parsed_config or fetching_yaml_file()

    # Validate the app_config and model_config separately.
    app_config = AppConfig(**parsed_config.data)

    model_config = ModelConfig(**parsed_config.data)

    # Combine the validated app_config and model_config into a single Config object.
    config = Config(app_config=app_config, model_config=model_config)

    return config


config = validate_config()
