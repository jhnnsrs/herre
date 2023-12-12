""" Redirecters for OAuth2. 

This module contains redirecters that can be used by the herre
authorization code grant to redirect the user to the authorization
server, and to receive the code from the redirect uri.

We provide a few redirecters, but you can also create your own
redirecter, by implementing the RedirecterProtocol.





"""


from .mock import MockRedirecter
from .aiohttp_server import AioHttpServerRedirecter

__all__ = ["MockRedirecter", "AioHttpServerRedirecter"]
