---
sidebar_label: models
title: models
---

Basic types for the herre library

This module contains the basic types for the herre library.

## TokenRequest Objects

```python
class TokenRequest(BaseModel)
```

A token request

A token request is initiated by the client and contains all the information
needed to request a token from the server.

Grants can inspect the request and decide whether to handle it or not.
Additionailly, they can modify the request before it is sent to the next grant.

#### is\_refresh

Whether this is a refresh request

#### context

The context of the request

## Token Objects

```python
class Token(BaseModel)
```

A Token

A token object contains all the information about a token.
It mimics the oauthlib.oauth2.rfc6749.tokens.OAuthToken class.
However, you can use it with any grant, not just oauth2 grants.
As access_token is the only required field, you can use it as a simple
bearer token.

#### is\_expired

```python
def is_expired() -> bool
```

Checks if the token is expired

