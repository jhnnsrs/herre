---
sidebar_label: utils
title: grants.oauth2.utils
---

#### build\_authorize\_url

```python
def build_authorize_url(grant: BaseOauth2Grant) -> str
```

Builds the authorize url for the given grant.

Parameters
----------
grant : BaseOauth2Grant
    A BaseOauth2Grant

Returns
-------
str
    The authorize url

#### build\_token\_url

```python
def build_token_url(grant: BaseOauth2Grant) -> str
```

Builds the token url for the given grant.

Parameters
----------
grant : BaseOauth2Grant
    BaseOauth2Grant

Returns
-------
str
    The token url

#### build\_refresh\_url

```python
def build_refresh_url(grant: BaseOauth2Grant) -> str
```

Builds the token url for the given grant.

Parameters
----------
grant : BaseOauth2Grant
    BaseOauth2Grant

Returns
-------
str
    The token url

