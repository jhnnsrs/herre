---
sidebar_label: fakts_qt_store
title: fakts.fakts_qt_store
---

## OrderDefaults Objects

```python
class OrderDefaults(BaseModel)
```

A model for the default user storage

It is used to store the default user for the fakts
key.

## FaktsQtStore Objects

```python
class FaktsQtStore(BaseModel)
```

Retrieves and stores users matching the currently
active fakts grant

#### aput\_default\_user

```python
async def aput_default_user(user: Optional[StoredUser]) -> None
```

Puts the default user

This method stores the user under a key that it retrieves from
the fakts. This is done to ensure that the user is only stored
for the correct fakts. (E.g. when the corresponding endpoint
server changes)


Parameters
----------
user : StoredUser | None
    A stored user, with the token and the user, if None is provided
    the user is deleted

#### aget\_default\_user

```python
async def aget_default_user() -> Optional[StoredUser]
```

Gets the default user

Gets the default user for the fakts key. If no user is stored
for the fakts key, None is returned.

Returns
-------
Optional[StoredUser]
    A stored user, with the token and the user

## Config Objects

```python
class Config()
```

pydantic config

