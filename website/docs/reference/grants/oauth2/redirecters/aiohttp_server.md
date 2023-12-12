---
sidebar_label: aiohttp_server
title: grants.oauth2.redirecters.aiohttp_server
---

#### wrapped\_qs\_future

```python
def wrapped_qs_future(
        future: asyncio.Future, success_html: str,
        failure_html: str) -> Callable[[web.Request], Awaitable[web.Response]]
```

Wraps a future in a webserver

This is used to wrap a future in a webserver, so that the future can be resolved
when the webserver is called. It is similar to an async partial function.

Parameters
----------
future : Future
    The future to wrap
success_html : str
    The html to return when the future is resolved
failure_html : str
    The html to return when the future is rejected

## AioHttpServerRedirecter Objects

```python
class AioHttpServerRedirecter(BaseModel)
```

A simple webserver that will listen for a redirect from the OSF and return the path

#### aget\_redirect\_uri

```python
async def aget_redirect_uri(token_request: TokenRequest) -> str
```

Retrieves the redirect uri

This function will retrieve the redirect uri from the RedirectWaiter.
This function has to be implemented by the user.

#### astart

```python
async def astart(starturl: str) -> str
```

Awaits a redirect

This has to be implemented by a user

