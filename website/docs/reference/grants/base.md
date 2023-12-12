---
sidebar_label: base
title: grants.base
---

## BaseGrantProtocol Objects

```python
@runtime_checkable
class BaseGrantProtocol(Protocol)
```

The base grant protocol

This protocol is implemented by all grants.
It can be used to type hint a grant.

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will fetch a token from the grant.
This function is async, and should be awaited

Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

## BaseGrant Objects

```python
class BaseGrant(BaseModel)
```

The base grant class

This class is the base class for all grants.
It is a pydantic model, and can be used as such.
It also implements the BaseGrantProtocol, which can be used to type hint
a grant.

#### afetch\_token

```python
@abstractmethod
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will fetch a token from the grant.
This function is async, and should be awaited

Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

## Config Objects

```python
class Config()
```

Config for the base grant

