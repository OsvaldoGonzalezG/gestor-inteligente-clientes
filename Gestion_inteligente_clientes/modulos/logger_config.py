import logging
import os


def get_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("gic")
    if logger.handlers:
        return logger  # ya configurado

    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("logs/app.log", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt)

    logger.addHandler(fh)
    return logger
