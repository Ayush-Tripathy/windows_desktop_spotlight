import sys
import traceback
import utils.py_logger


def error_handler(exc_type, exc_value, exc_traceback):
    """
    Handles any unhandled exceptions
    logs error into stderr.log file and also prints to stdout
    """
    err_log = utils.py_logger.get_logger(__name__, "error")

    print("Unhandled exception\nFrom error handler: ")
    err_log.error(f"{exc_type.__name__}:"
                  f"{exc_value}\n"
                  f"{''.join(traceback.format_tb(exc_traceback))}")
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)


# Set error handler
# sys.excepthook = error_handler
