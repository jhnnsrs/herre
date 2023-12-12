---
sidebar_label: herre
title: herre
---

## Herre Objects

```python
class Herre(KoiledModel)
```

Herre is a client for Token authentication.

It provides a unified, composable interface for token based authentication based on grant.
A grant is a class that is able to retrieve a token. Importantly grants do not have to
directly call the token endpoint. They can also use a cache or other means to retrieve the
token.

Herre is a context manager. This allows it both to provide itself as a singleton and handle
the asynchronous interface of the grant. As well as providing a lock to ensure that only one
request is happening at a time.

**Example**:

    ```python
    from herre import Herre,
    from herre.grants.oauth2.client_credentials import ClientCredentialsGrant

    herre = Herre(
        grant=ClientCredentialsGrant(
            client_id="my_client_id",
            client_secret="my_client
            base_url="https://my_token_url",
        )
    )

    with herre:
        token = herre.get_token()
    ```
  
  or aync
  
    ```python
    from herre import Herre,
    from herre.grants.oauth2.client_credentials import ClientCredentialsGrant

    herre = Herre(
        grant=ClientCredentialsGrant(
            client_id="my_client_id",
            client_secret="my_client
            base_url="https://my_token_url",
        )
    )

    async with herre:
        token = await herre.get_token()
    ```

#### token

```python
@property
def token() -> Token
```

The current token

#### aget\_token

```python
async def aget_token(**kwargs) -> str
```

Get an access token

Will return an access token if it is already available or
try to login depending on auto_login. The checking and potential retrieving will happen
in a lock ensuring that not multiple requests are happening at the same time.

**Arguments**:

- `auto_login` _bool, optional_ - Should we allow an automatic login. Defaults to True.
  

**Returns**:

- `str` - The access token

#### arefresh\_token

```python
async def arefresh_token(**kwargs) -> str
```

Refresh the token

Will cause the linked grant to refresh the token. Depending
on the link logic, this might cause another login.

#### arequest\_from\_grant

```python
async def arequest_from_grant(request: TokenRequest) -> Token
```

Request a token from the grant

You should not need to call this method directly. It is used internally
to request a token from the grant, and will not directly acquire a lock
(so multiple requests can happen at the same time, which is often not what
you want).

Parameters
----------
request : TokenRequest
    The token request (contains context and whether it is a refresh request)

Returns
-------
Token
    The token (with access_token, refresh_token, etc.)

#### get\_token

```python
def get_token(**kwargs) -> str
```

Get an access token

Will return an access token if it is already available or
try to login depending on auto_login. The checking and potential retrieving will happen
in a lock ensuring that not multiple requests are happening at the same time.

#### aget\_user

```python
async def aget_user(**kwargs) -> BaseModel
```

Get the current user

Will return the current user if a fetcher is available

#### \_\_aenter\_\_

```python
async def __aenter__() -> "Herre"
```

Enters the context and logs in if needed

#### \_\_aexit\_\_

```python
async def __aexit__(*args, **kwargs) -> None
```

Exits the context and logs out if needed

#### \_repr\_html\_inline\_

```python
def _repr_html_inline_() -> str
```

Jupyter inline representation

## Config Objects

```python
class Config()
```

Pydantic config

#### get\_current\_herre

```python
def get_current_herre() -> Herre
```

Get the current herre instance

