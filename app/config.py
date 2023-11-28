import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings

# LoggingSettings has a single field for the logging level
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are type int


# Settings has several fields for various application settings, including the API
# version string, CORS origins, and project name. Settings also includes an instance of LoggingSettings.
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8000",  # type: ignore
    ]

    PROJECT_NAME: str = "Predicting customer churn API"

    class Config:
        case_sensitive = True


# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa
class InterceptHandler(logging.Handler):

    """
        This is a custom logging handler. This handler intercepts log records from the
        standard logging module and redirects them to loguru. This allows us to use loguru's features
        with libraries that use the standard logging module.
    """
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:

    """
    This function sets up the application's logging using the provided settings.
    It replaces the handlers of the root logger and several other loggers with instances
    of InterceptHandler, and configures loguru with a handler that writes to sys.stderr.
    """

    # configuring the loggers for uvicorn, which is the ASGI server running the application.
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")

    # Setting the handler for the root logger to an instance of InterceptHandler
    logging.getLogger().handlers = [InterceptHandler()]

    # This for loop iterates over the LOGGERS tuple and sets the handler for each named
    # logger to an instance of InterceptHandler. This means that log messages from uvicorn.asgi and
    # uvicorn.access will also be passed to InterceptHandler.
    # In this for loop, we are not doing the same thing as the code in line 73, this line is a
    # catch-all for all logger in the application, while the for loop is specifically targeting the uvicorn loggers.
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]
    # Configuring the loguru's logger. The handlers parameter is a list of handlers, and
    # each handler is a dictionary that specifies a sink and a level. The sink is where
    # the log messages will be outputted, and in this case, it’s sys.stderr, meaning log messages
    # will be outputted to the standard error stream. The level is the minimum level of log
    # messages that the handler will handle, and it’s set to the logging level from the application settings.
    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )


settings = Settings()
