import logging
import constants


def get_logger(name=__name__, level="debug") -> logging.Logger:

    logger = logging.getLogger(name)

    formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s")

    if level == "error":
        log_file = constants.STDERR_LOG_FILE
    else:
        log_file = constants.STDOUT_LOG_FILE

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logging_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "exception": logging.ERROR,
        "fatal": logging.FATAL,
        "critical": logging.CRITICAL
    }
    if level in logging_levels:
        logger.setLevel(logging_levels[level])
    else:
        raise Exception("Invalid level")

    return logger
