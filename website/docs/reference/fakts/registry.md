---
sidebar_label: registry
title: fakts.registry
---

## GrantType Objects

```python
class GrantType(str, Enum)
```

The grant type

#### CLIENT\_CREDENTIALS

The client credentials grant

#### AUTHORIZATION\_CODE

The authorization code grant

## GrantRegistry Objects

```python
class GrantRegistry(BaseModel)
```

A registry for grants.

This registry is used to register grants. It is used by the fakts
grant to build the correct grant from the fakts.

#### register\_grant

```python
def register_grant(grant_type: GrantType, grant: GrantBuilder) -> None
```

Registers a grant.

**Arguments**:

  ___________
- `type` - GrantType
  The type of the grant to register
- `grant` - Type[BaseGrant]
  The grant to register

#### get\_grant\_for\_type

```python
def get_grant_for_type(grant_type: GrantType) -> GrantBuilder
```

Gets the grant for a type.

**Arguments**:

  ___________
- `type` - GrantType
  The type of the grant to get
  

**Returns**:

  ________
  Type[BaseGrant]
  The grant for the type

## Config Objects

```python
class Config()
```

Pydantic config

