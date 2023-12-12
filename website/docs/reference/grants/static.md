---
sidebar_label: static
title: grants.static
---

## StaticGrant Objects

```python
class StaticGrant(BaseGrant)
```

A grant that uses a static token

THis grant will always return the same token.
It is useful for testing.

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will return the token that was passed to the constructor.

Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

