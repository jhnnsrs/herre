---
sidebar_label: mock
title: grants.oauth2.redirecters.mock
---

## MockRedirecter Objects

```python
class MockRedirecter(BaseModel)
```

A simple webserver that will listen for a redirect from the OSF and return the path

#### code

The code to return

#### aget\_redirect\_uri

```python
async def aget_redirect_uri(token_request: TokenRequest) -> str
```

Retrieves the redirect uri

This function will retrieve the redirect uri from the RedirectWaiter.
This function has to be implemented by the user.

#### astart

```python
async def astart(auth_url: str) -> str
```

Awaits a redirect

This has to be implemented by a user

