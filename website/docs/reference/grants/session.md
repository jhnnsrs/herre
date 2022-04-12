---
sidebar_label: session
title: grants.session
---

OAuth2Support for aiohttp.ClientSession.
Based on the requests_oauthlib class
https://github.com/requests/requests-oauthlib/blob/master/requests_oauthlib/oauth2_session.py

## TokenUpdated Objects

```python
class TokenUpdated(Warning)
```

Exception.

## OAuth2Session Objects

```python
class OAuth2Session(aiohttp.ClientSession)
```

Versatile OAuth 2 extension to :class:`requests.Session`.
Supports any grant type adhering to :class:`oauthlib.oauth2.Client` spec
including the four core OAuth 2 grants.
Can be used to create authorization urls, fetch tokens and access protected
resources using the :class:`requests.Session` interface you are used to.
- :class:`oauthlib.oauth2.WebApplicationClient` (default): Authorization Code Grant
- :class:`oauthlib.oauth2.MobileApplicationClient`: Implicit Grant
- :class:`oauthlib.oauth2.LegacyApplicationClient`: Password Credentials Grant
- :class:`oauthlib.oauth2.BackendApplicationClient`: Client Credentials Grant
Note that the only time you will be using Implicit Grant from python is if
you are driving a user agent able to obtain URL fragments.

#### \_\_init\_\_

```python
def __init__(client_id=None, client=None, auto_refresh_url=None, auto_refresh_kwargs=None, scope=None, redirect_uri=None, token=None, state=None, token_updater=None, **kwargs)
```

Construct a new OAuth 2 client session.

**Arguments**:

- `client_id`: Client id obtained during registration
- `client`: :class:`oauthlib.oauth2.Client` to be used. Default is
WebApplicationClient which is useful for any
hosted application but not mobile or desktop.
- `scope`: List of scopes you wish to request access to
- `redirect_uri`: Redirect URI you registered as callback
- `token`: Token dictionary, must include access_token
and token_type.
- `state`: State string used to prevent CSRF. This will be given
when creating the authorization url and must be supplied
when parsing the authorization response.
Can be either a string or a no argument callable.
- `kwargs`: Arguments to pass to the Session constructor.

#### new\_state

```python
def new_state()
```

Generates a state string to be used in authorizations.

#### client\_id

```python
@property
def client_id()
```

Get the client_id.

#### client\_id

```python
@client_id.setter
def client_id(value)
```

Set the client_id.

#### client\_id

```python
@client_id.deleter
def client_id()
```

Remove the client_id.

#### token

```python
@property
def token()
```

Get the token.

#### token

```python
@token.setter
def token(value)
```

Set the token.

#### access\_token

```python
@property
def access_token()
```

Get the access_token.

#### access\_token

```python
@access_token.setter
def access_token(value)
```

Set the access_token.

#### access\_token

```python
@access_token.deleter
def access_token()
```

Remove the access_token.

#### authorized

```python
@property
def authorized()
```

Boolean that indicates whether this session has an OAuth token
or not. If `self.authorized` is True, you can reasonably expect
OAuth-protected requests to the resource to succeed. If
`self.authorized` is False, you need the user to go through the OAuth
authentication dance before OAuth-protected requests to the resource
will succeed.

#### authorization\_url

```python
def authorization_url(url, state=None, **kwargs)
```

Form an authorization URL.

**Arguments**:

- `url`: Authorization endpoint url, must be HTTPS.
- `state`: An optional state string for CSRF protection. If not
given it will be generated for you.
- `kwargs`: Extra parameters to include.

**Returns**:

authorization_url, state

#### fetch\_token

```python
async def fetch_token(token_url, code=None, authorization_response=None, body="", auth=None, username=None, password=None, method="POST", force_querystring=False, timeout=None, headers=None, verify_ssl=True, proxies=None, include_client_id=None, client_id=None, client_secret=None, **kwargs)
```

Generic method for fetching an access token from the token endpoint.

If you are using the MobileApplicationClient you will want to use
`token_from_fragment` instead of `fetch_token`.
The current implementation enforces the RFC guidelines.

**Arguments**:

- `token_url`: Token endpoint URL, must use HTTPS.
- `code`: Authorization code (used by WebApplicationClients).
- `authorization_response`: Authorization response URL, the callback
URL of the request back to you. Used by
WebApplicationClients instead of code.
- `body`: Optional application/x-www-form-urlencoded body to add the
include in the token request. Prefer kwargs over body.
- `auth`: An auth tuple or method as accepted by `requests`.
- `username`: Username required by LegacyApplicationClients to appear
in the request body.
- `password`: Password required by LegacyApplicationClients to appear
in the request body.
- `method`: The HTTP method used to make the request. Defaults
to POST, but may also be GET. Other methods should
be added as needed.
- `force_querystring`: If True, force the request body to be sent
in the querystring instead.
- `timeout`: Timeout of the request in seconds.
- `headers`: Dict to default request headers with.
- `verify`: Verify SSL certificate.
- `proxies`: The `proxies` argument is passed onto `requests`.
- `include_client_id`: Should the request body include the
`client_id` parameter. Default is `None`,
which will attempt to autodetect. This can be
forced to always include (True) or never
include (False).
- `client_secret`: The `client_secret` paired to the `client_id`.
This is generally required unless provided in the
`auth` tuple. If the value is `None`, it will be
omitted from the request, however if the value is
an empty string, an empty string will be sent.
- `kwargs`: Extra parameters to include in the token request.

**Returns**:

A token dict

#### token\_from\_fragment

```python
def token_from_fragment(authorization_response)
```

Parse token from the URI fragment, used by MobileApplicationClients.

**Arguments**:

- `authorization_response`: The full URL of the redirect back to you

**Returns**:

A token dict

#### refresh\_token

```python
async def refresh_token(token_url, refresh_token=None, body="", auth=None, timeout=None, headers=None, verify_ssl=True, proxies=None, **kwargs)
```

Fetch a new access token using a refresh token.

**Arguments**:

- `token_url`: The token endpoint, must be HTTPS.
- `refresh_token`: The refresh_token to use.
- `body`: Optional application/x-www-form-urlencoded body to add the
include in the token request. Prefer kwargs over body.
- `auth`: An auth tuple or method as accepted by `requests`.
- `timeout`: Timeout of the request in seconds.
- `headers`: A dict of headers to be used by `requests`.
- `verify`: Verify SSL certificate.
- `proxies`: The `proxies` argument will be passed to `requests`.
- `kwargs`: Extra parameters to include in the token request.

**Returns**:

A token dict

#### register\_compliance\_hook

```python
def register_compliance_hook(hook_type, hook)
```

Register a hook for request/response tweaking.
Available hooks are:
    access_token_response invoked before token parsing.
    refresh_token_response invoked before refresh token parsing.
    protected_request invoked before making a request.
If you find a new hook is needed please send a GitHub PR request
or open an issue.

