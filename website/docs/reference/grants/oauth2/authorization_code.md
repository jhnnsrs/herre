---
sidebar_label: authorization_code
title: grants.oauth2.authorization_code
---

## Redirecter Objects

```python
@runtime_checkable
class Redirecter(Protocol)
```

A protocol for a from oauthlib.common import generate_tokenedirect waiter

#### aget\_redirect\_uri

```python
async def aget_redirect_uri(token_request: TokenRequest) -> str
```

Retrieves the redirect uri

This function will retrieve the redirect uri from the RedirectWaiter.
This function has to be implemented by the user.

#### astart

```python
def astart(starturl: str) -> Awaitable[str]
```

Awaits a redirect

This has to be implemented by a user, and should
return the path of the redirect (with the code)

Parameters
----------
starturl : str
    The url to start the redirect from

Returns
-------
Awaitable[str]
    The path of the redirect (with the code)

## AuthorizationCodeGrant Objects

```python
class AuthorizationCodeGrant(BaseOauth2Grant)
```

A grant that uses the authorization code flow

This grant will create an AuthorizationCodeGrant, and use it to fetch a token.

#### redirecter

A simple webserver that will listen for a redirect from the OSF and return the path

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetch Token

This function will fetch a token from the oauth2 provider,
using the authorization code flow. It will retrieve the redirect_uri from the redirecter,
and use that as the redirect_uri, it will then build an authorization url, and delegate the
redirect to the RedirectWaiter. When the redirecter has received the redirect, it will
return the code to this function, which will then use the code to fetch a token.


Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

