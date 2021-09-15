from pydantic.main import BaseModel
import yaml
import os


class ConfigError(Exception):
    pass

class BaseConfig(BaseModel):
    """Container for the Configuration options
    parsed either from Env or from the yaml file

    Abstract:
        __group (str): Needs to implement for the Parsing

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """
    _group: str = None


    @classmethod
    def from_file(cls, file_path, **overrides):
        assert cls._group is not None, "Please specifiy your parent group in your Config Class to access it from a file "
        assert os.path.isfile(file_path), f"File {file_path} does not exist"
        
        with open(file_path,"r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

            try:
                for subgroup in cls._group.split("."):
                    config = config[subgroup]

                config.update(**overrides)
                return cls(**config)
            except KeyError as e:
                raise ConfigError(f"Couldn't load {cls._group} Group from {file_path}: Subgroup {subgroup} does not exist in {config}") from e