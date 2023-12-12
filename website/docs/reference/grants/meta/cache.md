---
sidebar_label: cache
title: grants.meta.cache
---

## CacheFile Objects

```python
class CacheFile(pydantic.BaseModel)
```

Cache file model

## CacheGrant Objects

```python
class CacheGrant(BaseGrant)
```

Grant for caching data, caches the data of the its child grant in a file,
if that file exists, and it is not expired, it will be used instead of delegating
to the child grant.

#### grant

The grant to cache

#### cache\_file

The cache file to use

#### hash

The hash of the config to validate against

#### expires\_in

The expiration time of the cache

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will delegate to the child grant if the cache is expired or
does not exist.

Additionally, it will check the hash of the config, and the expiration data
if it does not match, it will delegate to the child grant.

Token Request Parameters:
-------------------------
allow_cache: bool
Whether to allow the cache to be used

Parameters
----------
request : TokenRequest
The token request to use

Returns
-------
Token
The token

