# herre

[![codecov](https://codecov.io/gh/jhnnsrs/herre/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/herre)
[![PyPI version](https://badge.fury.io/py/herre.svg)](https://pypi.org/project/herre/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI status](https://img.shields.io/pypi/status/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI download month](https://img.shields.io/pypi/dm/herre.svg)](https://pypi.python.org/pypi/herre/)

#### DEVELOPMENT

## Idea

herre is an (asynchronous) oauth2/openid client, that provides sensible defaults for the python
ecosystem

## Prerequisites

herre needs a oauth2 server to connect to

## Supports

- Authorization Code Flow (PKCE)
- Client-Credentials Flow

## Usage

In order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance

```python

client = Herre(
    grant=AuthorizationCode()
    host="p-tnagerl-lab1",
    port=8000,
    client_id="$YOUR_CLIENT_ID",
    client_secret="$YOUR_CLIENT_SECRET",
    name="karl",
)

client.login()

```

## Intergration with Qt

herre fully supports qt-based applications (both PySide2 and PyQt5) and provides a convenient helper class 'QtHerre'
as well as a included windowed Authoriation Code Flow (needs pyqtwebengine as additional dependency) as well as browser based logins

```python
class MainWindow(QtWidget)

    def __init__(self, *args, **kwargs):
        self.herre = QtHerre(
          grant=QtWindowAuthorizationCode()
        )

```

## Build with

- [koil](https://github.com/jhnnsrs/koil) - for pyqt event loop handling
- [oauthlib](https://github.com/oauthlib/oauthlib) - for oauth2 compliance
- [aiohttp](https://github.com/aio-libs/aiohttp) - transport layer (especially redirect server)
