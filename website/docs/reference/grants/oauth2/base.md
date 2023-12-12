---
sidebar_label: base
title: grants.oauth2.base
---

## BaseOauth2Grant Objects

```python
class BaseOauth2Grant(BaseGrant)
```

A base class for oauth2 grants.

#### base\_url

The base url to use for the grant

#### client\_id

The client id to use for the grant

#### client\_secret

The client secret to use for the grant

#### scopes

The scopes to use for the grant

#### authorize\_path

The authorize path to use for the grant (relative to the base url)

#### refresh\_path

The refresh path to use for the grant (relative to the base url)

#### token\_path

The token path to use for the grant (relative to the base url)

#### scope\_delimiter

The scope delimiter to use for the grant default is a space

#### allow\_insecure

Whether to allow insecure connections

#### append\_trailing\_slash

Whether to append a trailing slash to the base url

