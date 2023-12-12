from aiohttp import web
import asyncio
import webbrowser
import logging
from herre.grants.oauth2.errors import Oauth2RedirectError
from typing import Callable, Awaitable
from pydantic import BaseModel
from herre.models import TokenRequest


logger = logging.getLogger(__name__)

success_full_return = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>Sucessfull Login</title>
  <meta name="description" content="A success page for login">
  <meta name="author" content="SitePoint">

  <meta property="og:title" content="Sucessfull Login">
  <meta property="og:type" content="website">

</head>

<body>
    <h1>Successfull Login</h1>
    <p>You can close this window</p>
  <script type="text/javascript">
  window.close() ;
</script>
</body>
</html>
"""

failure_return = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>Sucessfull Login</title>
  <meta name="description" content="A success page for login">
  <meta name="author" content="SitePoint">

  <meta property="og:title" content="Sucessfull Login">
  <meta property="og:type" content="website">

</head>

<body>
    <h1>Unsucessfull login</h1>
    <p>You can close this window</p>
  <script type="text/javascript">
  window.close() ;
</script>
</body>
</html>
"""


def wrapped_qs_future(
    future: asyncio.Future, success_html: str, failure_html: str
) -> Callable[[web.Request], Awaitable[web.Response]]:
    """Wraps a future in a webserver

    This is used to wrap a future in a webserver, so that the future can be resolved
    when the webserver is called. It is similar to an async partial function.

    Parameters
    ----------
    future : Future
        The future to wrap
    success_html : str
        The html to return when the future is resolved
    failure_html : str
        The html to return when the future is rejected

    """

    async def web_token_response(request: web.Request) -> web.Response:
        """The webserver response

        This function will resolve the future when called, and return a response
        to the caller.
        """
        try:
            future.set_result(request.path_qs)
            return web.Response(text=success_html, content_type="text/html")
        except Exception:
            return web.Response(text=failure_html, content_type="text/html")

    return web_token_response


class AioHttpServerRedirecter(BaseModel):
    """A simple webserver that will listen for a redirect from the OSF and return the path"""

    redirect_port: int = 6767
    redirect_timeout: int = 40
    redirect_host: str = "127.0.0.1"
    redirect_protocol: str = "http"
    redirect_path: str = "/"
    success_html: str = success_full_return
    failure_html: str = failure_return

    async def aget_redirect_uri(self, token_request: TokenRequest) -> str:
        """Retrieves the redirect uri

        This function will retrieve the redirect uri from the RedirectWaiter.
        This function has to be implemented by the user.

        """

        return f"{self.redirect_protocol}://{self.redirect_host}:{self.redirect_port}{self.redirect_path}"

    async def astart(
        self,
        starturl: str,
    ) -> str:
        """Awaits a redirect

        This has to be implemented by a user

        """

        token_future = asyncio.get_event_loop().create_future()

        app = web.Application()

        app.router.add_get(
            "/",
            wrapped_qs_future(
                token_future,
                success_html=success_full_return,
                failure_html=failure_return,
            ),
        )

        webserver_future = asyncio.wait_for(
            web._run_app(
                app,
                host=self.redirect_host,
                port=self.redirect_port,
                print=lambda x: logger.info(x),
                handle_signals=False,
            ),
            self.redirect_timeout,
        )

        webserver_task = asyncio.create_task(webserver_future)

        webbrowser.open(starturl)
        done, pending = await asyncio.wait(
            [token_future, webserver_task], return_when=asyncio.FIRST_COMPLETED
        )

        for tf in done:
            if tf == token_future:
                redirect_qs = tf.result()
            else:
                raise Oauth2RedirectError(
                    f"Webserver ended unexpectedly {str(tf.exception())}"
                )

        for task in pending:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        if not redirect_qs:
            raise Oauth2RedirectError("Webserver")

        return redirect_qs
