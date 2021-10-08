from herre.config import GrantType
from herre.grants.base import BaseGrant
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session
from aiohttp import ClientSession
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import aiohttp
from aiohttp import web
import asyncio
import logging

from herre.grants.registry import register_grant


logger = logging.getLogger(__name__)







def wrapped_future(future):
    async def web_token_response(request):
        future.set_result(request.path_qs)
        return web.Response(text="You can close me now !")

    return web_token_response


async def wait_for_server(app, host="localhost", port="6767", timeout=1):
    try:
        await asyncio.wait_for(web._run_app(app, host="localhost", port=6767, ), timeout)
    except asyncio.TimeoutError:
        return "no token"



@register_grant(GrantType.AUTHORIZATION_CODE)
@register_grant(GrantType.AUTHORIZATION_CODE_SERVER)
class AuthorizationCodeServerGrant(BaseGrant):
    refreshable = True

    async def afetch_token(self, **kwargs):

        self.web_app_client = WebApplicationClient(self.config.client_id, scope=self.scope)

        # Create an OAuth2 session for the OSF
        self.session = OAuth2Session(
            self.config.client_id, 
            self.web_app_client,
            scope=self.scope, 
            redirect_uri=self.config.redirect_uri,
            
        )

        auth_url, state = self.session.authorization_url(self.auth_url)

        webbrowser.open(auth_url)

        token_future = asyncio.get_event_loop().create_future()

        app = web.Application()
        app.router.add_get("/", wrapped_future(token_future))
        webserver_future = asyncio.wait_for(web._run_app(app, host="localhost", port=6767, print=lambda x: logger.info(x),handle_signals=False), self.config.timeout)
        done, pending = await asyncio.wait([token_future, webserver_future], return_when=asyncio.FIRST_COMPLETED)

        for tf in done:
            if tf == token_future:
                path = tf.result()
                print(path)
            else:
                path = None

        for task in pending:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        if path:
            return self.session.fetch_token(self.token_url, client_secret=self.config.client_secret, authorization_response=path, state=state)

        return None
