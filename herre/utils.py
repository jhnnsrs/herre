from enum import Enum
from urllib.parse import quote
from aiohttp import web
import asyncio
import webbrowser
import aiohttp_cors
import uuid
def wrapped_qs_future(future):

    async def web_token_response(request):
        future.set_result(request.path_qs)
        return web.Response(text="You can close me now !")

    return web_token_response


def wrapped_post_future(future, state):

    async def web_token_response(request):

        print(state) #TODO: Implement checking for state here
        future.set_result(await request.json())
        return web.json_response(data={"ok": True})

    return web_token_response


async def wait_for_server(app, host="localhost", port="6767", timeout=1):
    try:
        await asyncio.wait_for(web._run_app(app, host="localhost", port=6767, ), timeout)
    except asyncio.TimeoutError:
        return "no token"

class RedirectError(Exception):
    pass

async def wait_for_redirect(starturl, redirect_host="localhost", redirect_port=6767, path = "/", timeout=400, print_function= False, handle_signals=False):



    webbrowser.open(starturl)

    token_future = asyncio.get_event_loop().create_future()

    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    cors.add(app.router.add_get(path, wrapped_qs_future(token_future)), {
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    webserver_future = asyncio.wait_for(web._run_app(app, host=redirect_host, port=redirect_port, print=print_function,handle_signals=handle_signals), timeout)
    done, pending = await asyncio.wait([token_future, webserver_future], return_when=asyncio.FIRST_COMPLETED)

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

    if not redirect_qs: raise RedirectError("No redirect url provided")
    return redirect_qs


async def wait_for_post(starturl, redirect_host="localhost", redirect_port=6767, path = "/", timeout=400, print_function= False, handle_signals=False):
    

    state = uuid.uuid4()
    redirect_uri = quote(f"http://{redirect_host}:{redirect_port}{path}")

    webbrowser.open(starturl +f"?redirect_uri={redirect_uri}&state={state}")

    token_future = asyncio.get_event_loop().create_future()

    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_headers="*",
        )
    })
    cors.add(app.router.add_post(path, wrapped_post_future(token_future, state)))

    print("nanan")
    webserver_future = asyncio.wait_for(web._run_app(app, host=redirect_host, port=redirect_port, print=print_function,handle_signals=handle_signals), timeout)
    done, pending = await asyncio.wait([token_future, webserver_future], return_when=asyncio.FIRST_COMPLETED)

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

    if not redirect_qs: raise RedirectError("No redirect url provided")
    return redirect_qs
