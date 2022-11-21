from herre.grants.base import BaseGrant
from herre.types import Token
import os
from typing import Any, Dict, List, Optional, Union
import pydantic
import datetime
import logging
import json

logger = logging.getLogger(__name__)


class CacheFile(pydantic.BaseModel):
    """Cache file model"""

    token: Token
    created: datetime.datetime
    hash: str = ""


class CacheGrant(BaseGrant):
    """Grant for caching data, caches the data of the its child grant in a file,
    if that file exists, and it is not expired, it will be used instead of delegating
    to the child grant."""

    grant: BaseGrant = pydantic.Field(..., description="The grant to cache")
    cache_file: str = ".fakts_cache.json"
    hash: str = pydantic.Field(
        default_factory=lambda: "",
        description="Validating against the hash of the config",
    )
    expires_in: Optional[int]

    async def afetch_token(self, force_refresh: bool = False) -> Token:

        cache = None

        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                x = json.load(f)
                try:
                    cache = CacheFile(**x)

                    if self.expires_in:
                        if (
                            cache.created + datetime.timedelta(seconds=self.expires_in)
                            < datetime.datetime.now()
                        ):
                            cache = None

                    if self.hash and cache.hash != self.hash:
                        cache = None

                except pydantic.ValidationError as e:
                    logger.error(f"Could not load cache file: {e}. Ignoring it")

        if cache is None or force_refresh:
            data = await self.grant.aload(force_refresh=force_refresh)
            cache = CacheFile(
                config=data,
                created=datetime.datetime.now(),
            )

        with open(self.cache_file, "w") as f:
            json.dump(json.loads(cache.json()), f)

        return cache.config
