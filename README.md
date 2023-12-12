# herre

[![codecov](https://codecov.io/gh/jhnnsrs/herre/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/herre)
[![PyPI version](https://badge.fury.io/py/herre.svg)](https://pypi.org/project/herre/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI status](https://img.shields.io/pypi/status/herre.svg)](https://pypi.python.org/pypi/herre/)
[![PyPI download month](https://img.shields.io/pypi/dm/herre.svg)](https://pypi.python.org/pypi/herre/)

#### DEVELOPMENT

## Idea

Herre is a Python Library for easy integration with Token Based Authentication
in Python Applications, (for example using OAuth2). It is designed to be
extensible, and easy to use, and is built for the async world, while maintaining
sync compatibility.

Herre is build on top of aiohttp, and uses pydantic for data validation.

## Usage

In order to initialize a herre client you need to specify a specific grant to retrieve the access_token. A grant constitutes a way of retrieving a Token in an asynchronous manner.

```python
from herre import Herre
from herre.grants.oauth2.client_credentials import ClientCredentialsGrant

client = Herre(
      grant=ClientCredentialsGrant(
          base_url="http://localhost:8000/o",
          client_id="YOUR_CLIENT_ID",
          client_secret="YOUR_CLIENT_SECRET",
      ),
  )

with client as c:
  print(c.get_token()) # gets access token
  # first time this is called it will retrieve a token from the server

```


## Features

Herre supports the following protocols and grants to retrieve tokens:


### Oauth2

- [x] Client Credentials Flow
- [x] Authorization Code Flow
  - [x] Authorization Code Flow with Redirect Server
  - [x] Authorization Code Flow with QtWebengine Redirect
- [x] Refresh Token Flow

### Others
- [x] Basic Auth


## Async First

Herre is fully async, and supports the async/await syntax. It is also fully compatible with the sync world, and can be used in sync applications.

##### Async Interface

```python

client = Herre(
    grant=ClientCredentialsGrant(
          base_url="http://localhost:8000/o",
          client_id="YOUR_CLIENT_ID",
          client_secret="YOUR_CLIENT_SECRET",
      ),

async with client as c:
    token = await c.aget_token()

```

## Composability

Herre grants provide a simple interface to be composable and enable features like
caching, refresh tokens, and custom logic.

#### Enabling Caching the token until its expiration (or until the cache is cleared)

```python
client = Herre(
    grant=CacheGrant(
      grant=AuthorizationCodeGrant(base_url="https://your_server/oauth_path",
          client_id="$YOUR_CLIENT_ID",
          client_secret="$YOUR_CLIENT_SECRET",
          redirecter=AioHttpServerRedirecter(port=6767)
    ))
)

async with client:
  await client.aget_token() 
  # This will first hit the cache and try to retrieve the token from there
  await client.arefresh_token()
   # This will bypass the cache and retrieve a new token from the server
```

#### Enabling refresh tokens:

```python
client = Herre(
    grant=RefreshGrant(
      grant=AuthorizationCodeGrant(base_url="https://your_server/oauth_path",
          client_id="$YOUR_CLIENT_ID",
          client_secret="$YOUR_CLIENT_SECRET",
          redirecter=AioHttpServerRedirecter(port=6767)
    ))
)

async with client:
  await client.aget_token() 
  # this will try to refresh the token if it is expired, before restarting the
  # authorization code flow
```

Please check out the documentation for the meta grants to see how to enable custom logic.

## Builders

Herre comes with a set of builders to make it easier to create a client for common use cases, especially for oauth2.

#### Example Github
```python
from herre import github_desktop

with github_desktop(
    client_id="dfdb2c594470db113659",  # This is a demo github oauth2 app
    client_secret="bc59f1e3bc1ed0dcfb3548b457588f3b6e324764",
) as g:
    print(g.get_token())


```
This will open a browser window and ask you to login to github, and then return the token. The builder will automatically create a redirect server for you, and use the github oauth2 api to retrieve the token. Builders are not magic, but simple provide convenience methods
around the herre api.





## Intergration with Qt

herre fully supports qt-based applications (both PySide2 and PyQt5) as well as a a redirect_flow for authentication in a webengine powered qt window Authoriation Code Flow (needs pyqtwebengine as additional dependency) ( you can still use the authorization code server if so desired, and actually recommended for production applications)

```python
from herre import Herre
from koil.qt import async_to_qt
from PyQt5 import QtWidgets
from herre.grants.oauth2.authorization_code import AuthorizationCodeGrant
from herre.grants.oauth2.redirecters.qt_login_view import WebViewRedirecter
import sys




class LoginWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grant = AuthorizationCodeGrant(
            base_url="https://github.com/login/oauth",
            token_path="access_token",
            client_id="dfdb2c594470db113659",
            scopes=[],
            append_trailing_slash=False,
            client_secret="bc59f1e3bc1ed0dcfb3548b457588f3b6e324764",
            redirecter=WebViewRedirecter(redirect_uri="http://127.0.0.1:6767/"),# this will open a
            # webview to display the login page
        )

        self.herre = Herre(
            grant=self.grant,
        )

        self.herre.enter() # herre requires to be entered before it can be used


        self.login_task = async_to_qt(self.herre.aget_token)
        self.login_task.returned.connect(self.on_login_finished)
        self.login_task.errored.connect(self.on_login_error)

        self.login_button = QtWidgets.QPushButton("Login")
        self.greet_label = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.greet_label)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.greet)

    def greet(self):
        self.login_task.run()

    def on_login_finished(self, token):
        self.greet_label.setText(f"Hello User")
        # do something with the token

    def on_login_error(self, error):
        self.greet_label.setText(f"Error: {error}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(['', '--no-sandbox']) # you need to pass --no-sandbox to the
    # application if you are running it on linux (otherwise qtwebengine will not work)
    main_window = LoginWidget()

    main_window.show()
    sys.exit(app.exec())


```

## Build with

- [koil](https://github.com/jhnnsrs/koil) - for event loop handling
- [oauthlib](https://github.com/oauthlib/oauthlib) - for oauth2 compliance
- [aiohttp](https://github.com/aio-libs/aiohttp) - transport layer (especially redirect server)
