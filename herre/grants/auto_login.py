from herre.fetcher.errors import UserFetchingError
from herre.grants.base import BaseGrant
from typing import Optional, runtime_checkable, Protocol
from pydantic import BaseModel
from herre.models import Token, TokenRequest
from herre.grants.base import BaseGrantProtocol
import logging
import asyncio
from herre.fetcher.models import UserFetcher

logger = logging.getLogger(__name__)


class User(BaseModel):
    """A user model"""

    id: str
    username: str


class StoredUser(BaseModel):
    """A wrapping cl"""

    user: User
    token: Token


@runtime_checkable
class UserStore(Protocol):
    """A protocol for a user store

    This protocol is implemented by the user store.
    It can be used to type hint a user store. This
    is used by the AutoLoginGrant to store the user.

    """

    async def aget_default_user(self) -> Optional[StoredUser]:
        """Gets the default user

        Returns
        -------
        Optional[StoredUser]
            A stored user, with the token and the user
        """
        ...

    async def aput_default_user(self, user: Optional[StoredUser]) -> None:
        """Stores the default user


        Parameters
        ----------
        user : Optional[StoredUser]
            A stored user, with the token and the user, if None, the user should
            be deleted

        """
        ...


@runtime_checkable
class AutoLoginWidget(Protocol):
    """A protocol for a login widget

    This protocol is implemented by the login widget.
    It can be used to type hint a login widget. This
    is used by the AutoLoginGrant to show the login widget
    and ask the user if they want to save the user.
    """

    async def ashould_we_save(self, store: StoredUser) -> bool:
        """Should ask the user if we should save the user"""
        ...


class AutoLoginGrant(BaseGrant):
    """A grant that uses a Qt login screen to authenticate the user.

    The user is presented with a login screen that allows them to select a user
    from a list of previously logged in users. If the user is not in the list,
    they can click a button to start the login flow.


    """

    store: UserStore
    """this is the login widget (protocol)"""

    fetcher: UserFetcher

    widget: AutoLoginWidget
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
            if request.context.get("delete_active", True):
                await self.store.aput_default_user(None)

            if request.context.get("allow_auto_login", True):
                stored_user = await self.store.aget_default_user()
                if stored_user:
                    # Lets check if the token is still valid

                    try:
                        user = await self.fetcher.afetch_user(stored_user.token)
                        await self.store.aput_default_user(
                            StoredUser(user=user.dict(), token=stored_user.token)  # type: ignore # we dict here to ensure the serialization works
                        )
                        return stored_user.token
                    except UserFetchingError:
                        # The token is not valid anymore
                        token = await self.grant.afetch_token(request)
                        user = await self.fetcher.afetch_user(token)
                        await self.store.aput_default_user(
                            StoredUser(
                                user=user.dict(), token=token  # type: ignore# we dict here to ensure the serialization works
                            )
                        )
                        return token

                    # This time with a refresh

            # We are skipping the widget and just fetching the token
            token = await self.grant.afetch_token(request)
            user = await self.fetcher.afetch_user(token)

            new_store = StoredUser(user=user.dict(), token=token)  # type: ignore # we dict here to ensure the serialization works
            should_we_save = await self.widget.ashould_we_save(new_store)
            if should_we_save:
                await self.store.aput_default_user(new_store)
            else:
                await self.store.aput_default_user(None)

            return token

        except asyncio.CancelledError as e:
            raise e

        except Exception as e:
            logger.error(e, exc_info=True)
            raise e

    class Config:
        """Pydantic config"""

        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
