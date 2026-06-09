"""Structured logging configuration for ResearchOps.

Call ``configure_logging()`` once at application startup (in the CLI
entry point or the API lifespan handler). After that, use the stdlib
``logging`` module everywhere — no direct dependency on this module
required.

Design decisions:
- Use ``logging.basicConfig`` with a structured format for simplicity.
- Rich handler for pretty terminal output in development mode.
- Plain stream handler for production / CI environments.
"""

import logging
import sys


def configure_logging(
    level: str | None = None,
    use_rich: bool = True,
) -> None:
    """Configure the root logger for the application.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR).
               Defaults to INFO if not provided.
        use_rich: Use Rich's pretty handler for development output.
                  Set to False in production or when capturing logs.
    """
    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)

    if use_rich:
        try:
            from rich.logging import RichHandler

            handler: logging.Handler = RichHandler(
                rich_tracebacks=True,
                show_path=False,
            )
            fmt = "%(message)s"
        except ImportError:
            handler = logging.StreamHandler(sys.stderr)
            fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    else:
        handler = logging.StreamHandler(sys.stderr)
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(
        level=log_level,
        format=fmt,
        handlers=[handler],
        force=True,  # override any existing configuration
    )

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.

    Usage:
        log = get_logger(__name__)
        log.info("Processing file: %s", path)
    """
    return logging.getLogger(name)
