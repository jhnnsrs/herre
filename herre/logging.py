import logging

try:
    from rich.logging import RichHandler
    StreamHandler = RichHandler
except ImportError as e:
    from logging import StreamHandler


def setLogging(log_level, log_stream=False, log_file=True):
    

    
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if log_stream:
        stream = StreamHandler()
        logging.root.setLevel(log_level)
        stream.setLevel(log_level)

        logger.addHandler(stream)

    if log_file:
        file = logging.FileHandler("logs.txt")
        logging.root.setLevel(log_level)
        file.setLevel(log_level)

        logger.addHandler(file)



setLogging("INFO", log_stream=True)
