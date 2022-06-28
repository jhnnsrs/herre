class HerreError(Exception):
    pass


class NoHerreFound(HerreError):
    pass


class LoginException(HerreError):
    pass


class ConfigurationException(HerreError):
    pass
