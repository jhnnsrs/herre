---
sidebar_label: herre
title: herre
---

## Herre Objects

```python
class Herre(KoiledModel)
```

#### aget\_token

```python
async def aget_token(force_refresh=False)
```

Get an access token

This is a loop safe couroutine, that will return an access token if it is already available or
try to login depending on auto_login. The checking and potential retrieving will happen
in a lock ensuring that not multiple requests are happening at the same time.

**Arguments**:

- `auto_login` _bool, optional_ - Should we allow an automatic login. Defaults to True.
  

**Returns**:

- `str` - The access token

#### alogin

```python
async def alogin(force_refresh=False, retry=0)
```

Login Function

Login is a compount function that will try to ensure a login following the following steps:

1. Set the current state to none (if not already set)
2. Try to load the token from the token file (and check its validity)
3. If the token is not valid or force_refresh is true, try to refresh the token.
4. If the grant is a user grant (indicated on the grantclass) make a request to the userinfo endpoint and check update the state with user information
5. Returns the state

**Arguments**:

- `force_refresh` _bool, optional_ - [description]. Defaults to False.
- `retry` _int, optional_ - [description]. Defaults to 0.
  

**Raises**:

- `Exception` - [description]
- `Exception` - [description]

