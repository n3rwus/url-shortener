import logging
import sys
import colorlog


def setup_logger():
    """
    Set up a logger for the entire project with a consistent format and output,
    including colorized output for different log levels.
    """
    logger = logging.getLogger()  # Root logger
    logger.setLevel(logging.DEBUG)  # Set root logger to DEBUG to capture all levels

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)  # Set the logging level for the stream handler

    log_format = '%(log_color)s[%(asctime)s] [%(levelname)s] - %(message)s'

    formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'blue',  # Debug logs in blue
            'INFO': '',  # Info logs with no color
            'WARNING': 'yellow',  # Warning logs in yellow
            'ERROR': 'red',  # Error logs in red
            'CRITICAL': 'bold_red',  # Critical logs in bold red
        }
    )

    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
