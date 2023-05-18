from .base import BaseOauth2Grant
from aiohttp import web
import asyncio
import webbrowser
import logging
from .errors import Oauth2RedirectError


logger = logging.getLogger(__name__)


def build_authorize_url(grant: BaseOauth2Grant) -> str:
    return (
        f"{grant.base_url}/{grant.authorize_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.authorize_path}"
    )


def build_token_url(grant: BaseOauth2Grant) -> str:
    return (
        f"{grant.base_url}/{grant.token_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.token_path}"
    )


def build_refresh_url(grant: BaseOauth2Grant) -> str:
    return (
        f"{grant.base_url}/{grant.refresh_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.refresh_path}"
    )


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


def wrapped_qs_future(future):
    async def web_token_response(request):
        try:
            future.set_result(request.path_qs)
            return web.Response(text=success_full_return, content_type="text/html")
        except Exception as e:
            return web.Response(text=failure_return, content_type="text/html")

    return web_token_response


async def wait_for_redirect(
    starturl,
    redirect_host="localhost",
    redirect_port=6767,
    path="/",
    timeout=400,
    print_function=False,
    handle_signals=False,
) -> str:
    """A simple webserver that will listen for a redirect from the OSF and return the path"""

    token_future = asyncio.get_event_loop().create_future()

    app = web.Application()

    app.router.add_get(path, wrapped_qs_future(token_future))

    webserver_future = asyncio.wait_for(
        web._run_app(
            app,
            host=redirect_host,
            port=redirect_port,
            print=lambda x: logger.info(x),
            handle_signals=handle_signals,
        ),
        timeout,
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
            raise Oauth2RedirectError(f"Webserver ended unexpectedly {str(tf.exception())}")

    for task in pending:
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

    if not redirect_qs:
        raise Oauth2RedirectError("Webserver")

    return redirect_qs
