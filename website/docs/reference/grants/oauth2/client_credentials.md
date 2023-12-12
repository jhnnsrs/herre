---
sidebar_label: client_credentials
title: grants.oauth2.client_credentials
---

## ClientCredentialsGrant Objects

```python
class ClientCredentialsGrant(BaseOauth2Grant)
```

A grant that uses the client credentials flow

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches a token

This function will fetch a token from the oauth2 provider,
using the client credentials flow.


Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

