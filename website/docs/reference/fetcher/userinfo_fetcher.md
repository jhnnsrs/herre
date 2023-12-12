---
sidebar_label: userinfo_fetcher
title: fetcher.userinfo_fetcher
---

## UserinfoUserFetcher Objects

```python
class UserinfoUserFetcher(BaseModel)
```

A user fetcher that fetches the user from an userinfo endpoint.

This fetcher uses the userinfo endpoint to fetch the user. It uses the access token to
authenticate itself to the userinfo endpoint.

You can specify the model to use for the user. This model will be used to parse the answer
from the userinfo endpoint. The model should be a pydantic model.

#### userModel

The model to use for the user

#### userinfo\_endpoint

The endpoint to fetch the user from

#### ssl\_context

An ssl context to use for the connection to the endpoint

#### afetch\_user

```python
async def afetch_user(token: Token) -> BaseModel
```

Fetches the user from the userinfo endpoint.

**Arguments**:

  ___________
- `token` - Token
  The token to use to authenticate to the userinfo endpoint.
  

**Returns**:

  ________
  BaseModel
  The user as a pydantic model (will be userModel)

