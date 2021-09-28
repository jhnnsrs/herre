
import asyncio
import threading





def loopify(potential_future, as_task=False):
    """Taks an Async Function and according
    to the current loop setting either returns over
    it synchronusly in the herre loop or returns
    a future

    Args:
        potential_future ([type]): [description]

    Returns:
        [type]: [description]
    """
    from herre.auth import get_current_herre

    loop = get_current_herre().loop

    if as_task:
        return loop.create_task(potential_future)

    if loop.is_running():
        print("Here")
        if loop._thread_id == threading.current_thread().ident: return potential_future
        return asyncio.run_coroutine_threadsafe(potential_future, loop).result()
    

    return loop.run_until_complete(potential_future)



def next_on_gen(potential_generator, loop):
    """Takes a Async Generator and iterates over it
    threadsafe in the provided loop and returns the result
    synchronously in another generator

    Args:
        potential_generator ([type]): [description]
        loop ([type]): [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """
    ait = potential_generator.__aiter__()

    async def next_on_ait():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
        
    while True:
        done, obj = asyncio.run_coroutine_threadsafe(next_on_ait(), loop).result()
        if done: 
            break
        yield obj


def loopify_gen(potential_generator):
    """Takes a Async Generator and iterates over it
    threadsafe in the herre loop providing a syncrhonus
    generator or returns an async generator in the current
    loop

    Args:
        potential_generator ([type]): [description]

    Returns:
        [type]: [description]
    """
    from herre.auth import get_current_herre

    loop = get_current_herre().loop
    if loop.is_running():
        if loop._thread_id == threading.current_thread().ident: return potential_generator
        return next_on_gen(potential_generator, loop)



