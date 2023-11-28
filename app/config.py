import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings


# Set the logging level for the application. The logging level is an integer value that represents
# the severity level at which the logger should start reporting log messages.
# BaseSettings inherits from BaseModel and is specifically designed for application settings and
# configuration, with additional features for loading data from various sources.
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO


# Settings has several fields for various application settings, including the API
# version string, CORS origins, and project name. Settings also includes an instance of LoggingSettings.
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    logging: LoggingSettings = LoggingSettings()

    # This is a list of URLs that are allowed to make cross-origin requests to the API.
    # Cross-Origin Resource Sharing (CORS) is a mechanism that allows many resources
    # on a web page to be requested from another domain outside the domain from which the resource originated.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8000",  # type: ignore
    ]

    PROJECT_NAME: str = "Predicting customer churn API"

    # The nested Config class with a single attribute case_sensitive set to True. This means that the
    # environment variables used to set these settings must match the case of the field names.
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

        """
        The emit method is overridden to customize the handling of log records.
        This method is called whenever a log record needs to be processed.
        """

        # try to get the corresponding loguru level for the log record. If it doesn't exist,
        # fall back to the original level number from the log record.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        #  Find the frame and depth from where the logged message originated.
        #  This information is used to correctly attribute the log message in loguru.
        frame, depth = logging.currentframe(), 2

        # log the message using loguru with the determined level, depth, and
        # exception information from the log record.
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:

    """
    This function configures the application’s logging system to use loguru for outputting log messages,
    and to use the InterceptHandler to ensure that log messages from the standard logging library
    (used by uvicorn and potentially other libraries) are also handled by loguru. The logging level
    is configured based on the application settings.
    """

    # Configuring the loggers for uvicorn, which is the ASGI server running the application.
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
