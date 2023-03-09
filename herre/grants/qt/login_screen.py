import ssl
import certifi

from herre.grants.base import BaseGrant, BaseGrantProtocol
from herre.types import Token
from typing import List, Optional, Dict
import logging
from qtpy import QtWidgets, QtCore
from pydantic import BaseModel, Field
logger = logging.getLogger(__name__)
from koil.qt import QtCoro, QtFuture
from .errors import UserCancelledError
import asyncio
import aiohttp
from herre.grants.errors import GrantException
import json

class User(BaseModel):
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]
    sub: str
    id: str


class UserStore(BaseModel):
    user: User
    token: Token

class Storage(BaseModel):
    users: Dict[str,UserStore]


class UserWidget(QtWidgets.QWidget):
    login_clicked = QtCore.Signal(UserStore)
    logout_clicked = QtCore.Signal(UserStore)

    def __init__(self, store: UserStore, *args,  **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.store = store

        self.user_label = QtWidgets.QLabel(store.user.username)
        self.user_label.mousePressEvent = self.on_clicked

        self.logout_button = QtWidgets.QPushButton("Logout")
        self.logout_button.clicked.connect(self.on_logout_clicked)

        self.hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout)
        self.hlayout.addWidget(self.user_label)
        self.hlayout.addWidget(self.logout_button)

    def on_clicked(self, event):
        self.login_clicked.emit(self.store)

    def on_logout_clicked(self):
        self.logout_clicked.emit(self.store)



class LoginWidget(QtWidgets.QDialog):


    def __init__(self, identifier, version, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settings = QtCore.QSettings("Arkitekt", f"{identifier}:{version}")
        
        self.vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout)


        self.user_list_l = QtWidgets.QVBoxLayout()
        self.vlayout.addLayout(self.user_list_l)

        self.show_coro = QtCoro(self.show, autoresolve=True)
        self.hide_coro = QtCoro(self.hide, autoresolve=True)

        self.select_user_coro = QtCoro(self.start_select_user)
        self.store_user_coro = QtCoro(self.store_user, autoresolve=True)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.new_user_button = QtWidgets.QPushButton("New User")
        self.button_layout.addWidget(self.new_user_button)
        self.new_user_button.clicked.connect(self.on_new_user_clicked)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)


        self.vlayout.addLayout(self.button_layout)

        self.refresh_users()
        self._future: Optional[QtFuture] = None

    def start_select_user(self, future: QtFuture):
        self._future = future

    def store_user(self, userStore: UserStore) -> None:
        un_storage = self.settings.value("userstore", None)
        if un_storage:
            storage = Storage(**json.loads(un_storage))
        else:
            storage = Storage(users={})
        storage.users[userStore.user.id] = userStore

        self.settings.setValue("userstore", storage.json())
        self.refresh_users()

    def delete_user(self, userStore: UserStore) -> None:
        un_storage = self.settings.value("userstore", None)
        if un_storage:
            storage = Storage(**json.loads(un_storage))
        else:
            storage = Storage(users={})
        del storage.users[userStore.user.id]
        self.settings.setValue("userstore", storage.json())
        self.refresh_users()

    def get_user_stores(self) -> List[UserStore]:
        un_storage = self.settings.value("userstore", None)
        if not un_storage:
            return []
        storage = Storage(**json.loads(un_storage))
        return [userstore for userstore in storage.users.values()]

    def clearLayout(self, layout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_users(self):
        self.clearLayout(self.user_list_l)
        self.user_list_l.addWidget(QtWidgets.QLabel("Select User"))
        for userstore in self.get_user_stores():
            widget = UserWidget(userstore)
            self.user_list_l.addWidget(widget)
            widget.login_clicked.connect(self.on_user_clicked)
            widget.logout_clicked.connect(self.delete_user)

    def on_cancel_clicked(self):
        self.close()

    def close(self) -> bool:
        if self._future:
            self._future.reject(UserCancelledError("The user cancelled the login"))
        return super().close()

    def on_new_user_clicked(self) -> None:
        if self._future:
            self._future.resolve()

    def on_user_clicked(self, user: UserStore) -> None:
        if self._future:
            self._future.resolve(user)


    def retrieve_users(self) -> List[User]:
        return self.settings.value("user_list", [])


class FetchingUserException(GrantException):
    """A base exception for errors that occur while fetching a user.

    Args:
        GrantException (_type_): _description_
    """
    pass

class MalformedAnswerException(FetchingUserException):
    """Raised when the answer from the userinfo endpoint is malformed."""
    pass



class QtLoginScreen(BaseGrant):
    """A grant that uses a Qt login screen to authenticate the user.

    The user is presented with a login screen that allows them to select a user
    from a list of previously logged in users. If the user is not in the list,
    they can click a button to start the login flow.


    """

    grant: BaseGrantProtocol
    """The grant to use for the login flow."""
    userinfo_endpoint: str
    """The endpoint to use for fetching the user info."""
    widget: LoginWidget
    """The widget to use for the login screen."""
    auto_login: bool = False
    """If true, the user will be automatically logged in if there is only one user in the list."""
    ssl_context: ssl.SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where()),
        exclude=True,
    )
    """ An ssl context to use for the connection to the endpoint"""

    async def afetch_user(self, token: Token) -> User:
       async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            headers={"Authorization": f"Bearer {token.access_token}"},
        ) as session:
            async with session.get(
                f"{self.userinfo_endpoint}",
            ) as resp:
                data = await resp.json()

                if resp.status == 200:
                    data = await resp.json()
                    if "username" not in data:
                        logger.error(f"Malformed answer: {data}")
                        raise MalformedAnswerException("Malformed Answer")

                    return User(**data)

                else:
                    raise FetchingUserException("Error! Coud not retrieve on the endpoint")



    async def afetch_token(self, force_refresh: bool =False) -> Token:
        """Fetches the token

        This function will only delegate to the grant if the user has not
        previously logged in (aka there is no token in the storage) Or if the
        force_refresh flag is set.

        Args:
            force_refresh (bool, optional): _description_. Defaults to False.

        Raises:
            e: _description_

        Returns:
            Token: _description_
        """

        try:
            await self.widget.show_coro.acall()

            store: UserStore = await self.widget.select_user_coro.acall()
            if store and not force_refresh:
                await self.widget.hide_coro.acall()
                return store.token

            new_token = await self.grant.afetch_token(force_refresh=force_refresh)
            user = await self.afetch_user(new_token) 

            await self.widget.store_user_coro.acall(UserStore(user=user, token=new_token))


            await self.widget.hide_coro.acall()
            return new_token

        except asyncio.CancelledError as e:
            await self.widget.hide_coro.acall()
            raise e

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True



