---
sidebar_label: auto_login
title: grants.qt.auto_login
---

## ShouldWeSaveThisAsDefault Objects

```python
class ShouldWeSaveThisAsDefault(QtWidgets.QDialog)
```

A dialog that asks the user if they want to save the user as the default user.

#### \_\_init\_\_

```python
def __init__(stored: StoredUser, *args, **kwargs) -> None
```

Creates a new ShouldWeSaveThisAsDefault dialog

## AutoLoginWidget Objects

```python
class AutoLoginWidget(QtWidgets.QWidget)
```

A Qt widget for auto login.

This widget can be used by the AutoLoginGrant to show the login widget
and ask the user if they want to save the user.

#### \_\_init\_\_

```python
def __init__(*args, **kwargs) -> None
```

Creates a new AutoLoginWidget

#### ashould\_we\_save

```python
async def ashould_we_save(store: StoredUser) -> bool
```

Should ask the user if we should save the user

