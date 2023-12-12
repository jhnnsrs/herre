---
sidebar_label: builders
title: builders
---

#### github\_desktop

```python
def github_desktop(client_id: str,
                   client_secret: str,
                   scopes: Optional[List[str]] = None) -> Herre
```

Creates a Herre instance that can be used to login locally to github

This function will create a Herre instance that can be used to login locally to github.
It will use the authorization code grant, and a aiohttp server redirecter.

Parameters
----------
client_id : str
    The client id to use
client_secret : str
    The client secret to use
scopes : Optional[List[str]], optional
    The scopes to use, by default None

Returns
-------
Herre
    The Herre instance

