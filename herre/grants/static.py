from herre.grants.base import BaseGrant
from herre.models import Token, TokenRequest


class StaticGrant(BaseGrant):
    """A grant that uses a static token

    THis grant will always return the same token.
    It is useful for testing.

    """

    token: Token

    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetches a token

        This function will return the token that was passed to the constructor.

        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token
        """
        return self.token
