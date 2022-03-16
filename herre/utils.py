from enum import Enum
from urllib.parse import quote
from aiohttp import web
import asyncio
import webbrowser
import uuid
import logging

logger = logging.getLogger(__name__)


class RedirectError(Exception):
    pass


def wrapped_qs_future(future):
    async def web_token_response(request):
        future.set_result(request.path_qs)
        return web.Response(text="You can close me now !")

    return web_token_response


async def wait_for_redirect(
    starturl,
    redirect_host="localhost",
    redirect_port=6767,
    path="/",
    timeout=400,
    print_function=False,
    handle_signals=False,
):

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

    webbrowser.open(starturl)
    done, pending = await asyncio.wait(
        [token_future, webserver_future], return_when=asyncio.FIRST_COMPLETED
    )

    for tf in done:
        if tf == token_future:
            redirect_qs = tf.result()
        else:
            redirect_qs = None

    for task in pending:
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

    if not redirect_qs:
        raise RedirectError("No redirect path provided")

    return redirect_qs
