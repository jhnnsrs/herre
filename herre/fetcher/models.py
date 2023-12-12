from herre.models import Token
from typing import Protocol, runtime_checkable, Type
from pydantic import BaseModel


@runtime_checkable
class UserFetcher(Protocol):
    """A protocol for fetching users.

    A user fetcher is a class that is able to fetch a user from a token. It
    can be a parameter to the Herre class. The Herre class will then use the
    user fetcher to fetch the user from the token.


    """

    userModel: Type[BaseModel]

    async def afetch_user(self, token: Token) -> BaseModel:
        """Fetches the user from the token.


        Parameters:
        ___________
        token: Token
            The token to use to fetch the user.

        Returns:
        ________
        BaseModel
            The user as a pydantic model (will be userModel)

        """
        ...
