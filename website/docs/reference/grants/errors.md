---
sidebar_label: errors
title: grants.errors
---

## GrantException Objects

```python
class GrantException(HerreError)
```

Base class for all grant exceptions

## RetriesExceededException Objects

```python
class RetriesExceededException(GrantException)
```

Raised when a grant exceeds the number of retries

