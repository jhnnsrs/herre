from typing import Union
from rich.console import Console as RichConsole
import contextvars


console = contextvars.ContextVar("console", default=None)

def get_current_console() -> RichConsole:
    c = console.get()
    if not c:
        console.set(RichConsole())
    return console.get() 


class Console():

    def __init__(self) -> None:
        self.console = RichConsole()


    def __enter__(self):
        console.set(self)
        return self


    def __exit__(self,*args, **kwargs):
        pass
