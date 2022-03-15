from herre.grants.base import BaseGrant
from herre.grants.openid import OpenIdUser
from herre.grants.refreshable import Refreshable
from oauthlib.oauth2 import WebApplicationClient
from herre.grants.session import OAuth2Session
from herre.types import Token, User
import webbrowser
from aiohttp import web
import asyncio
import logging
from herre.grants.utils import build_authorize_url, build_token_url
from herre.herre import Herre

logger = logging.getLogger(__name__)
REDIRECT_PORT = 6767


def wrapped_future(future):
    async def web_token_response(request):
        future.set_result(request.path_qs)
        return web.Response(text="You can close me now !")

    return web_token_response


class AuthorizationCodeServerGrant(BaseGrant, Refreshable, OpenIdUser):
    def __init__(
        self,
        redirect_port=REDIRECT_PORT,
        redirect_timeout=40,
    ) -> None:
        self.redirect_port = redirect_port
        self.redirect_timeout = redirect_timeout
        self.redirect_uri = f"http://localhost:{redirect_port}/"

    async def afetch_token(self, herre: Herre) -> Token:

        web_app_client = WebApplicationClient(
            herre.client_id, scope=herre.scope_delimiter.join(herre.scopes + ["openid"])
        )

        # Create an OAuth2 session for the OSF
        async with OAuth2Session(
            herre.client_id,
            web_app_client,
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
            redirect_uri=self.redirect_uri,
        ) as session:

            auth_url, state = session.authorization_url(build_authorize_url(herre))
            print(auth_url)
            token_future = asyncio.get_event_loop().create_future()

            app = web.Application()
            app.router.add_get("/", wrapped_future(token_future))
            webserver_future = asyncio.wait_for(
                web._run_app(
                    app,
                    host="localhost",
                    port=self.redirect_port,
                    print=lambda x: logger.info(x),
                    handle_signals=False,
                ),
                self.redirect_timeout,
            )

            webbrowser.open(auth_url)
            done, pending = await asyncio.wait(
                [token_future, webserver_future], return_when=asyncio.FIRST_COMPLETED
            )

            for tf in done:
                if tf == token_future:
                    path = tf.result()
                else:
                    raise tf.exception()

            for task in pending:
                task.cancel()

                try:
                    await task
                except asyncio.CancelledError:
                    pass

            if path:
                print(path)

                token_dict = await session.fetch_token(
                    build_token_url(herre),
                    client_secret=herre.client_secret,
                    authorization_response=path,
                    state=state,
                )

                print(token_dict)
                return Token(**token_dict)

        raise Exception("Could not fetch token")
