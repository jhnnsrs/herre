from typing import Union
import contextvars

try:
    from rich.console import Console as RichConsole
    console_instance = RichConsole()

except ImportError as e:
    console_instance = None


console = contextvars.ContextVar("console", default=console_instance)

def get_current_console():
    return console.get() 


class Console():

    def __init__(self) -> None:
        self.console = RichConsole()


    def __enter__(self):
        console.set(self)
        return self


    def __exit__(self,*args, **kwargs):
        pass
