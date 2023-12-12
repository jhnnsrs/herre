from pydantic import BaseModel
from qtpy import QtCore
from typing import Optional
from herre.grants.stored_login import StoredUser


class QtSettingsUserStore(BaseModel):
    """A user store that uses Qt settings to store the use"""

    settings: QtCore.QSettings
    default_user_key: str = "default_user"

    async def aput_default_user(self, user: Optional[StoredUser]) -> None:
        """Puts the default user

        Parameters
        ----------
        user : StoredUser | None
            A stored user, with the token and the user, if None is provided
            the user is deleted
        """
        self.settings.setValue(self.default_user_key, user.json() if user else None)

    async def aget_default_user(self) -> Optional[StoredUser]:
        """Gets the default user

        Returns
        -------
        Optional[StoredUser]
            A stored user, with the token and the user
        """
        un_default_user = self.settings.value(self.default_user_key, None)
        if not un_default_user:
            return None
        return StoredUser.parse_raw(un_default_user)
