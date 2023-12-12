""" Herre

Herre is a Python Library for easy integration with Token Based Authentication
in Python Applications, (for example using OAuth2). It is designed to be
extensible, and easy to use, and is built for the async world, while maintaining
sync compatibility.

Herre is build on top of aiohttp, and uses pydantic for data validation.


"""


from .herre import Herre, current_herre
from .builders import github_desktop

__all__ = ["Herre", "current_herre", "github_desktop"]
