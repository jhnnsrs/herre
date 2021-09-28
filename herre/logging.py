from herre.config.logging import LoggingConfig
import logging
from rich.logging import RichHandler


def setLogging(config_path=None,**kwargs):

    if config_path:
        config = LoggingConfig.from_file(config_path, overrides=kwargs)
    else:
        config = LoggingConfig(**kwargs)    

    logger = logging.getLogger()
    logger.setLevel(config.level)

    if config.stream:
        stream = RichHandler(markup=True)
        logging.root.setLevel(config.level)
        stream.setLevel(config.level)

        logger.addHandler(stream)

    if config.file:
        file = logging.FileHandler("logs.txt")
        logging.root.setLevel(config.level)
        file.setLevel(config.level)

        logger.addHandler(file)


