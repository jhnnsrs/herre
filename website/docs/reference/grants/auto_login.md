---
sidebar_label: auto_login
title: grants.auto_login
---

## User Objects

```python
class User(BaseModel)
```

A user model

## StoredUser Objects

```python
class StoredUser(BaseModel)
```

A wrapping cl

## UserStore Objects

```python
@runtime_checkable
class UserStore(Protocol)
```

A protocol for a user store

This protocol is implemented by the user store.
It can be used to type hint a user store. This
is used by the AutoLoginGrant to store the user.

#### aget\_default\_user

```python
async def aget_default_user() -> Optional[StoredUser]
```

Gets the default user

Returns
-------
Optional[StoredUser]
    A stored user, with the token and the user

#### aput\_default\_user

```python
async def aput_default_user(user: Optional[StoredUser]) -> None
```

Stores the default user


Parameters
----------
user : Optional[StoredUser]
    A stored user, with the token and the user, if None, the user should
    be deleted

## AutoLoginWidget Objects

```python
@runtime_checkable
class AutoLoginWidget(Protocol)
```

A protocol for a login widget

This protocol is implemented by the login widget.
It can be used to type hint a login widget. This
is used by the AutoLoginGrant to show the login widget
and ask the user if they want to save the user.

#### ashould\_we\_save

```python
async def ashould_we_save(store: StoredUser) -> bool
```

Should ask the user if we should save the user

## AutoLoginGrant Objects

```python
class AutoLoginGrant(BaseGrant)
```

A grant that uses a Qt login screen to authenticate the user.

The user is presented with a login screen that allows them to select a user
from a list of previously logged in users. If the user is not in the list,
they can click a button to start the login flow.

#### store

this is the login widget (protocol)

#### widget

this is the login widget (protocol)

#### grant

The grant to use for the login flow.

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches the token

This function will only delegate to the grant if the user has not
previously logged in (aka there is no token in the storage) Or if the
force_refresh flag is set.

**Arguments**:

- `force_refresh` _bool, optional_ - _description_. Defaults to False.
  

**Raises**:

- `e` - _description_
  

**Returns**:

- `Token` - _description_

## Config Objects

```python
class Config()
```

Pydantic config

