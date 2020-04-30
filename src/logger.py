import logging
import os

log = logging.getLogger()


def init_logging(filename):
    if hasattr(log, "initialized") and log.initialized:
        return

    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename=log_path)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(name)s:%(levelname)s:%(module)s:%(funcName)s] %(message)s")
    console_formatter = logging.Formatter(
        fmt="\n%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.setLevel(logging.DEBUG)
    log.initialized = True

