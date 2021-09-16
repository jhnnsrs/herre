import logging
from rich.logging import RichHandler


def setLogging(log_level, log_stream=False):
    LOGFORMAT = "  s%(levelname)-8s%(reset)s | %(message)s%(reset)s"
    file = logging.FileHandler("logs.txt")
    logging.root.setLevel(log_level)
    file.setLevel(log_level)


    
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if log_stream:
        stream = RichHandler(markup=True)
        logging.root.setLevel(log_level)
        stream.setLevel(log_level)

        logger.addHandler(stream)

    logger.addHandler(file)


setLogging("INFO", log_stream=True)
