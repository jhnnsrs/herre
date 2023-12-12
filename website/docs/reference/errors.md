---
sidebar_label: errors
title: errors
---

## HerreError Objects

```python
class HerreError(Exception)
```

Base class for Herre errors

## NoHerreFound Objects

```python
class NoHerreFound(HerreError)
```

Raised when no Herre instance is found in the context.

## LoginException Objects

```python
class LoginException(HerreError)
```

Raised when the login dfails.

## ConfigurationException Objects

```python
class ConfigurationException(HerreError)
```

Raised when the configuration is invalid.

