# herre

[![codecov](https://codecov.io/gh/jhnnsrs/herre/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/herre)
[![PyPI version](https://badge.fury.io/py/herre.svg)](https://pypi.org/project/herre/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI status](https://img.shields.io/pypi/status/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI download month](https://img.shields.io/pypi/dm/herre.svg)](https://pypi.python.org/pypi/herre/)

#### DEVELOPMENT

## Idea

herre is an (asynchronous) client for token authentication through oauth2 (and potentially other protocols).

## Prerequisites

herre needs a oauth2/opendid server to connect to

## Supports

- Authorization Code Flow (PKCE)
  - Within a Qt app through a QtWebengine View
  - With a Redirect Server
- Client-Credentials Flow

## Usage

In order to initialize the Client you need to specify a specific grant to retrieve the code. A grant constitutes
a way of retrieving a Token in an asynchronous manner.

```python
from herre import Herre
from herre.grants.oauth2.authorization_code_server import AuthorizationCodeServer

client = Herre(
      grant=ClientCredentialsGrant(
          base_url="http://localhost:8000/o",
          client_id="YOUR_CLIENT_ID",
          client_secret="YOUR_CLIENT_SECRET",
      ),
  )

with client as c:
  c.get_token()

```

Async usage

```python

client = Herre(
    grant=ClientCredentialsGrant(
          base_url="http://localhost:8000/o",
          client_id="YOUR_CLIENT_ID",
          client_secret="YOUR_CLIENT_SECRET",
      ),

async with client as c:
    token = await c.get_token()

```

## Composability

Herre grants provide a simple interface to be composable and enable caching, or support for refresh tokens:

Enabling Caching the token until its expiration (or until the cache is cleared)

```python
client = Herre(
    grant=CacheGrant(
      grant=AuthorizationCodeServerGrant(base_url="https://your_server/oauth_path",
          client_id="$YOUR_CLIENT_ID",
          client_secret="$YOUR_CLIENT_SECRET",
          redirect_uri="http://localhost:6767")
))

async with client:
  await client.login()
```

Enabling refresh tokens:

```python
client = Herre(
    grant=RefreshGrant(
      grant=AuthorizationCodeServerGrant(base_url="https://your_server/oauth_path",
          client_id="$YOUR_CLIENT_ID",
          client_secret="$YOUR_CLIENT_SECRET",
          redirect_uri="http://localhost:6767")
))

async with client:
  await client.login()
```

Please check out the documentation for the meta grants to see how to enable custom logic.

## Intergration with Qt

herre fully supports qt-based applications (both PySide2 and PyQt5) as well as a a redirect_flow for authentication in a webengine powered qt window Authoriation Code Flow (needs pyqtwebengine as additional dependency) ( you can still use the authorization code server if so desired)

```python
class MainWindow(QtWidget)

    def __init__(self, *args, **kwargs):
        self.herre = Herre(
          grant=AuthorizationCodeQtGrant(
            base_url="https://your_server/oauth_path",
            client_id="$YOUR_CLIENT_ID",
            client_secret="$YOUR_CLIENT_SECRET",
            redirect_uri="about:blank,)
        )

        self.herre.enter() #programmatically enter context (make sure to call exit)


    def login()
        t = self.herre.get_token()


    def refresh_token():
        t = self.herre.refresh_token()
```

## Build with

- [koil](https://github.com/jhnnsrs/koil) - for pyqt event loop handling
- [oauthlib](https://github.com/oauthlib/oauthlib) - for oauth2 compliance
- [aiohttp](https://github.com/aio-libs/aiohttp) - transport layer (especially redirect server)
