---
sidebar_label: settings_store
title: grants.qt.settings_store
---

## QtSettingsUserStore Objects

```python
class QtSettingsUserStore(BaseModel)
```

A user store that uses Qt settings to store the use

#### aput\_default\_user

```python
async def aput_default_user(user: Optional[StoredUser]) -> None
```

Puts the default user

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

Returns
-------
Optional[StoredUser]
    A stored user, with the token and the user

