from herre.grants.base import BaseGrant
from typing import Any, Dict, List, Optional, Type, runtime_checkable, Protocol
from pydantic import BaseModel, Field, SecretStr
from herre.types import GrantType, Token, TokenRequest
from herre.grants.errors import GrantException
from herre.grants.base import BaseGrantProtocol
import ssl
import certifi
import aiohttp
import logging
import asyncio
from herre.fetcher.types import UserFetcher

logger = logging.getLogger(__name__)


class User(BaseModel):
    id: str
    username: str


class StoredUser(BaseModel):
    user: User
    token: Token


class FetchingUserException(GrantException):
    """A base exception for errors that occur while fetching a user.

    Args:
        GrantException (_type_): _description_
    """

    pass


class MalformedAnswerException(FetchingUserException):
    """Raised when the answer from the userinfo endpoint is malformed."""

    pass


@runtime_checkable
class UserStore(Protocol):
    async def aget_users(self) -> List[StoredUser]:
        ...

    async def aget_default_user(self) -> Optional[StoredUser]:
        ...

    async def aput_default_user(self, user: StoredUser) -> None:
        ...

    async def adelete_user(self, user: StoredUser) -> None:
        ...

    async def aput_user(self, user: StoredUser) -> None:
        ...

    async def aclear(self) -> None:
        ...


@runtime_checkable
class LoginWidget(Protocol):
    async def aselect_user(self, store: UserStore) -> Optional[StoredUser]:
        """SHould ask the user to select a user from the list provided by the store or return None
        if the user wants to create a new user"""
        ...

    async def ashould_we_save(self, store: StoredUser) -> bool:
        """Should ask the user if we should save the user"""
        ...

    async def adestroy(self) -> None:
        """Should destroy the widget.  Called when unsucessful"""
        ...

    async def aclose(self) -> None:
        """Should close the widget.  Called when sucessful"""
        ...

    async def ashowexpired(self) -> None:
        """SHould show a message that the token is expired"""
        ...

    async def ashow_welcome(self) -> None:
        """Will be called when the user is logged in"""
        ...


class StoredLoginGrant(BaseGrant):
    """A grant that uses a Qt login screen to authenticate the user.

    The user is presented with a login screen that allows them to select a user
    from a list of previously logged in users. If the user is not in the list,
    they can click a button to start the login flow.


    """

    store: UserStore
    """this is the login widget (protocol)"""

    fetcher: UserFetcher

    widget: LoginWidget
    """this is the login widget (protocol)"""

    grant: BaseGrantProtocol
    """The grant to use for the login flow."""

    async def afetch_token(self, request: TokenRequest) -> Token:
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
            print("afetch_token", request)
            if not request.context.get("allow_stored_user", True):
                store: StoredUser = await self.widget.aselect_user(self.store)
                print("store", store)
                if store:
                    # Lets check if the token is still valid

                    try:
                        user = await self.fetcher.afetch_user(store.token)
                        await self.store.aput_user(
                            StoredUser(user=user, token=store.token)
                        )  # We update the user in case it has changed
                        await self.widget.aclose()
                        return store.token
                    except FetchingUserException:
                        # The token is not valid anymore
                        await self.widget.ashowexpired()  # Show the indication that the token is expired and we need to refresh it
                        # If this is handled later on by a refresh token grant, this should not display anything but needs to
                        # if refresh grant is not available
                        token = await self.grant.afetch_token(request)
                        user = await self.fetcher.afetch_user(token)
                        await self.store.aput_user(
                            StoredUser(
                                user=user.dict(), token=token
                            )  # we dict here to ensure the serialization works
                        )  # We update the user in case it has changed
                        await self.widget.aclose()
                        return token

                    # This time with a refresh

            # We are skipping the widget and just fetching the token
            token = await self.grant.afetch_token(request)
            user = await self.fetcher.afetch_user(token)

            new_store = StoredUser(user=user.dict(), token=token)
            should_we_save = await self.widget.ashould_we_save(new_store)
            if should_we_save:
                await self.store.aput_user(new_store)
            await self.widget.aclose()

            return token

        except asyncio.CancelledError as e:
            await self.widget.aclose()
            raise e

        except Exception as e:
            await self.widget.adestroy()
            raise e

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
