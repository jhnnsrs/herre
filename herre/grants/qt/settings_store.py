from pydantic import BaseModel
from qtpy import QtCore
import json
from typing import Dict, Any, List, Optional
from herre.grants.stored_login import StoredUser


class Storage(BaseModel):
    users: Dict[str, StoredUser] = {}


class QtSettingsUserStore(BaseModel):
    settings: QtCore.QSettings
    saved_users_key: str = "user_list"
    default_user_key: str = "default_user"

    async def aget_users(self) -> List[StoredUser]:
        un_storage = self.settings.value(self.saved_users_key, None)
        if not un_storage:
            return []
        storage = Storage(**json.loads(un_storage))
        return [userstore for userstore in storage.users.values()]

    async def adelete_user(self, user: StoredUser) -> None:
        un_storage = self.settings.value(self.saved_users_key, None)
        if un_storage:
            storage = Storage(**json.loads(un_storage))
        else:
            storage = Storage(users={})
        del storage.users[user.id]
        self.settings.setValue(self.saved_users_key, storage.json())

    async def aput_user(self, user: StoredUser) -> None:
        un_storage = self.settings.value(self.saved_users_key, None)
        if un_storage:
            storage = Storage(**json.loads(un_storage))
        else:
            storage = Storage(users={})
        storage.users[user.id] = user

        self.settings.setValue(self.saved_users_key, storage.json())

    async def aclear(self) -> None:
        self.settings.setValue(self.saved_users_key, None)

    async def aput_default_user(self, user: StoredUser | None) -> None:
        self.settings.setValue(self.default_user_key, user.json() if user else None)

    async def aget_default_user(self) -> Optional[StoredUser]:
        un_default_user = self.settings.value(self.default_user_key, None)
        if not un_default_user:
            return None
        return StoredUser.parse_raw(un_default_user)
