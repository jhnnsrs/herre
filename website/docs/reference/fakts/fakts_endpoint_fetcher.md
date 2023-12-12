---
sidebar_label: fakts_endpoint_fetcher
title: fakts.fakts_endpoint_fetcher
---

## FaktsUserFetcher Objects

```python
class FaktsUserFetcher(BaseModel)
```

The endpoint to fetch the user from

#### fakts\_key

An ssl context to use for the connection to the endpoint

#### afetch\_user

```python
async def afetch_user(token: Token) -> BaseModel
```

Fetches the user from the endpoint

Parameters
----------
token : Token
    The token to use for the request

Returns
-------
BaseModel
    The userModel filled with the data from the endpoint

## Config Objects

```python
class Config()
```

pydantic config

