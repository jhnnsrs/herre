import logging
from rich.logging import RichHandler


def setLogging(config_path=None,**kwargs):

    logger = logging.getLogger()
    logger.setLevel("INFO")

    stream = RichHandler(markup=True)
    logging.root.setLevel("INFO")
    stream.setLevel("INFO")
    logger.addHandler(stream)


