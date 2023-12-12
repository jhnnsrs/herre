---
sidebar_label: grant
title: fakts.grant
---

## HerreFakt Objects

```python
class HerreFakt(BaseModel)
```

A fakt for the herre grant

## FaktsGrant Objects

```python
class FaktsGrant(BaseOauth2Grant)
```

A grant that uses fakts to configure itself

Parameters
----------
fakts : Fakts
    The fakts instance to use
base_url : Optional[str], optional
    The base url to use for the grant, by default None
grant_registry : GrantRegistry, optional
    The grant registry to use, by default get_default_grant_registry()
fakts_group : str
    The fakts group to use for the grant

#### fakts

Fakts instance to use

#### grant\_registry

The grant registry to use

#### base\_url

The base url to use for the grant (overwrites the one from the fakt)

#### fakts\_group

The fakts group to use for the grant

#### allow\_reconfiguration\_on\_invalid\_client

Whether to allow reconfiguration on invalid client errors

#### configure

```python
def configure(fakt: HerreFakt) -> None
```

Configures the grant

Sets the active grant to the grant specified in the fakt.

Parameters
----------
fakt : HerreFakt
    The fakt to configure the grant with

Raises
------
ValueError
    If the grant_type is not supported

#### afetch\_token

```python
async def afetch_token(request: TokenRequest) -> Token
```

Fetches the token

This function will delegete to the active grant.
If the underlying fakts has changed, it will reconfigure the grant.

Parameters
----------
request : TokenRequest
    The token request to use

Returns
-------
Token
    The token

Raises
------
InvalidClientError
    If the client is invalid and allow_reconfiguration_on_invalid_client is False

