import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "test_run.log"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers (critical with pytest-xdist)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Ensure log directory exists safely
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Absolute safety: never fail test collection due to logging
        pass

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler (safe)
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
            delay=True  # CRITICAL FIX
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # Never break test discovery
        pass

    # Console handler (always safe)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
