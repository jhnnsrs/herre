---
sidebar_label: models
title: fetcher.models
---

## UserFetcher Objects

```python
@runtime_checkable
class UserFetcher(Protocol)
```

A protocol for fetching users.

A user fetcher is a class that is able to fetch a user from a token. It
can be a parameter to the Herre class. The Herre class will then use the
user fetcher to fetch the user from the token.

#### afetch\_user

```python
async def afetch_user(token: Token) -> BaseModel
```

Fetches the user from the token.


**Arguments**:

  ___________
- `token` - Token
  The token to use to fetch the user.
  

**Returns**:

  ________
  BaseModel
  The user as a pydantic model (will be userModel)

