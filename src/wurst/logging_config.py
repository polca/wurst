# -*- coding: utf-8 -*-
"""Configure structlog logger for wurst package."""
import logging
import sys
from contextlib import contextmanager

import structlog


def configure_structlog(name: str = "wurst", level: int = logging.INFO):
    """Configure and return a named structlog logger.

    Args:
        name: Logger name (default: "wurst")
        level: Minimum log level (default: INFO, filters out DEBUG)

    Returns:
        Configured structlog logger bound to the given name
    """
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to output to STDOUT
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Get the standard library logger and configure it
    stdlib_logger = logging.getLogger(name)
    stdlib_logger.setLevel(level)
    stdlib_logger.handlers = []  # Clear any existing handlers
    stdlib_logger.addHandler(handler)
    stdlib_logger.propagate = False

    # Return the structlog logger bound to the name
    return structlog.get_logger(name)


@contextmanager
def debug_logging(name: str = "wurst"):
    """Context manager that temporarily enables DEBUG level logging to STDOUT.

    Args:
        name: Logger name (default: "wurst")

    Example:
        >>> from wurst.logging_config import debug_logging
        >>> with debug_logging():
        ...     logger.debug("This debug message will be printed")
    """
    stdlib_logger = logging.getLogger(name)
    handler = None

    # Find the StreamHandler that outputs to STDOUT
    for h in stdlib_logger.handlers:
        if isinstance(h, logging.StreamHandler) and h.stream == sys.stdout:
            handler = h
            break

    # Store original levels
    original_logger_level = stdlib_logger.level
    original_handler_level = handler.level if handler else logging.NOTSET

    try:
        # Set both logger and handler to DEBUG level
        stdlib_logger.setLevel(logging.DEBUG)
        if handler:
            handler.setLevel(logging.DEBUG)
        yield
    finally:
        # Restore original levels
        stdlib_logger.setLevel(original_logger_level)
        if handler:
            handler.setLevel(original_handler_level)
