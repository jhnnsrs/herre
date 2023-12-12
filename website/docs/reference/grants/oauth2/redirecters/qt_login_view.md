---
sidebar_label: qt_login_view
title: grants.oauth2.redirecters.qt_login_view
---

## WebViewRedirecter Objects

```python
class WebViewRedirecter(QWebEngineView)
```

A qt webengine view that can be used to login to a oauth2 provider

This class is used to login to a oauth2 provider, when using the authorization code grant,
but without a webserver. This class will open a webview, and wait for the user to login.
When the user is logged in, the user will be redirected to the redirect_uri.
This redirect_uri will be intercepted, and the code will be returned to the caller.

#### \_\_init\_\_

```python
def __init__(*args,
             redirect_uri: str = "http://localhost:4893/",
             **kwargs) -> None
```

Creates a new WebViewRedirecter

This function will create a new LoginWrapper, and initialize the webview.

Parameters
----------
redirect_uri : str
    The redirect_uri to intercept (you shoud own this uri)

**kwargs
    The arguments to pass to the webview

#### initialize

```python
def initialize(future: QtFuture, auth_url: str) -> None
```

Initializes the LoginWrapper

This function will initialize the LoginWrapper, and open the webview.
It will also set the future to resolve when the user is logged in.

Parameters
----------
future : QtFuture
    The future to resolve when the user is logged in
auth_url : str
    The url to login to
redirect_uri : str
    The redirect_uri to intercept

#### astart

```python
async def astart(auth_url: str) -> str
```

Starts the LoginWrapper

This function will start the LoginWrapper, and return the code when the user is logged in.

Parameters
----------
auth_url : str
    The url to login to
redirect_uri : str
    The redirect_uri to intercept

Returns
-------
str
    The redirect_uri with the code

#### aget\_redirect\_uri

```python
async def aget_redirect_uri(token_request: TokenRequest) -> str
```

Retrieves the redirect uri

This function will retrieve the redirect uri from the RedirectWaiter.
This function has to be implemented by the user.

