---
sidebar_label: refresh
title: grants.oauth2.refresh
---

#### arefresh

```python
async def arefresh(resfresh_url: str,
                   client_id: str,
                   client_secret: str,
                   refresh_token: str,
                   ssl_context: Optional[ssl.SSLContext] = None) -> Token
```

Refreshes a token on the given url with the given client_id and client_secret

**Arguments**:

- `resfresh_url` _str_ - The url to refresh the token on
- `client_id` _str_ - The client_id to use
- `client_secret` _str_ - The client_secret to use
- `refresh_token` _str_ - The refresh_token to use
- `ssl_context` _Optional[ssl.SSLContext], optional_ - Specific SSL token to use. Defaults to None.
  

**Returns**:

- `Oauth2Token` - The refreshed token

## RefreshGrant Objects

```python
class RefreshGrant(BaseGrant)
```

Tries to refresh the token (if it is not expired)
and a refresh token is available. When the token is expired
and no refresh token is available, it will try to fetch a new token.

This grant does not refresh the token automatically. Only when it is
implicitly called by the Herre api.

You can choose autofresh grant to refresh the token automatically.

**Arguments**:

- `BaseGrant` __type__ - _description_

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will get a token from the underlying grant,
once granted it will try to refresh the token if it is expired
and a refresh token is available. When the token is expired
and no refresh token is available, it will try to fetch a new token.

TokenRequest Context Parameters
-------------------------------
allow_refresh: bool
    Whether to allow refreshing the token. Defaults to True


Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

