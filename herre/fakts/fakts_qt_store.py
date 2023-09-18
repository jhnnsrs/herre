from herre.grants.qt.login_screen import (
    StoredUser,
)
from fakts import Fakts
import logging
from qtpy import QtCore

logger = logging.getLogger(__name__)
from typing import List, Dict, Optional

import json
from pydantic import BaseModel, Field


class OrderFakts(BaseModel):
    saved_users: Dict[str, List[StoredUser]] = {}


class OrderDefaults(BaseModel):
    default_user: Dict[str, StoredUser] = {}


class FaktsQtStore(BaseModel):
    """Retrieves and stores users matching the currently
    active fakts grant"""

    settings: QtCore.QSettings
    saved_users_key: str = "saved_users_fakts"
    default_user_key: str = "default_user_fakts"
    auto_login_key: str = "auto_login_fakts"
    fakts: Fakts
    fakts_key: str

    async def aget_users(self) -> List[StoredUser]:
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.saved_users_key, None)
        if not un_storage:
            return []
        storage = OrderFakts(**json.loads(un_storage))
        if key in storage.saved_users:
            return storage.saved_users[key]

    async def adelete_user(self, user: StoredUser) -> None:
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.saved_users_key, None)
        if not un_storage:
            return None
        storage = OrderFakts(**json.loads(un_storage))
        if key in storage.saved_users:
            storage.saved_users[key].remove(user)

            self.settings.setValue(self.saved_users_key, storage.json())

    async def aput_user(self, user: StoredUser) -> None:
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.saved_users_key, None)
        if not un_storage:
            storage = OrderFakts()
        else:
            storage = OrderFakts(**json.loads(un_storage))

        print(storage.saved_users)

        if key not in storage.saved_users:
            storage.saved_users[key] = []

        new_users = []

        for u in storage.saved_users[key]:
            if u.user.id == user.user.id:
                new_users.append(user)
            else:
                new_users.append(u)

        if user not in new_users:
            new_users.append(user)

        storage.saved_users[key] = new_users
        print(storage.saved_users)
        self.settings.setValue(self.saved_users_key, storage.json())

    async def aclear(self) -> None:
        self.settings.setValue(self.saved_users_key, None)

    async def aput_default_user(self, user: Optional[StoredUser]) -> None:
        print(user)
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.default_user_key, None)
        if not un_storage:
            storage = OrderDefaults()
        else:
            try:
                storage = OrderDefaults(**json.loads(un_storage))
            except Exception as e:
                print(e)
                storage = OrderDefaults()

        if user is None:
            if key in storage.default_user:
                del storage.default_user[key]
        else:
            storage.default_user[key] = user

        print(storage)

        self.settings.setValue(self.default_user_key, storage.json())

    async def aget_default_user(self) -> Optional[StoredUser]:
        key = await self.fakts.aget(self.fakts_key)
        un_storage = self.settings.value(self.default_user_key, None)
        if not un_storage:
            return None
        try:
            storage = OrderDefaults(**json.loads(un_storage))
            if key in storage.default_user:
                return storage.default_user[key]
        except Exception as e:
            print(e)
            return None

        return None

    class Config:
        arbitrary_types_allowed = True
