""" Fakts Contrib Package

This package contains contrib grants and the grant registry
that allows for the fakts grant to build the correct grant
from the fakts.
    
"""

from .grant import FaktsGrant, GrantRegistry

__all__ = ["FaktsGrant", "GrantRegistry"]
